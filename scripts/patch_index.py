#!/usr/bin/env python3
"""
Run from ~/jobs/site/:
  python3 patch_index.py

Patches index.html to add Robot Exposure as a 5th layer toggle.
"""

with open("index.html", "r") as f:
    html = f.read()

with open("index.html.backup", "w") as f:
    f.write(html)
print("Backed up index.html -> index.html.backup")

# PATCH 1: Add Robot Exposure button
html = html.replace(
    '<button data-mode="exposure">Digital AI Exposure</button>',
    '<button data-mode="exposure">Digital AI Exposure</button>\n        <button data-mode="robot">Robot Exposure</button>'
)
print("Patch 1: Added Robot Exposure button")

# PATCH 2: Add robotColor function
html = html.replace(
    'function exposureColor(v, a) {\n  if (v == null) return `rgba(128,128,128,${a})`;\n  return greenRedCSS(v / 10, a);\n}',
    'function exposureColor(v, a) {\n  if (v == null) return `rgba(128,128,128,${a})`;\n  return greenRedCSS(v / 10, a);\n}\n\nfunction robotColor(v, a) {\n  if (v == null) return `rgba(128,128,128,${a})`;\n  return greenRedCSS(v / 10, a);\n}'
)
print("Patch 2: Added robotColor function")

# PATCH 3: Add robot case to tileColorCSS
html = html.replace(
    'if (colorMode === "exposure") return exposureColor(d.exposure, alpha);',
    'if (colorMode === "exposure") return exposureColor(d.exposure, alpha);\n  if (colorMode === "robot") return robotColor(d.robot_exposure, alpha);'
)
print("Patch 3: Updated tileColorCSS")

# PATCH 4: Add robot case to tileSubInfo
html = html.replace(
    '''if (colorMode === "exposure") {
    return (r.exposure != null ? r.exposure + "/10" : "") +
           (r.jobs ? " \\u00b7 " + formatNumber(r.jobs) + " jobs" : "");
  }
  if (colorMode === "outlook")''',
    '''if (colorMode === "exposure") {
    return (r.exposure != null ? r.exposure + "/10" : "") +
           (r.jobs ? " \\u00b7 " + formatNumber(r.jobs) + " jobs" : "");
  }
  if (colorMode === "robot") {
    return (r.robot_exposure != null ? r.robot_exposure + "/10" : "") +
           (r.jobs ? " \\u00b7 " + formatNumber(r.jobs) + " jobs" : "");
  }
  if (colorMode === "outlook")'''
)
print("Patch 4: Updated tileSubInfo")

# PATCH 5: Add robot case to tooltipHighlight
# Insert robot block before the outlook block
html = html.replace(
    '} else if (colorMode === "outlook") {\n    const v = d.outlook;',
    '''} else if (colorMode === "robot") {
    const v = d.robot_exposure;
    if (v == null) return "";
    const color = robotColor(v, 1);
    return `<span style="color:${color};font-weight:600;">Robot Exposure: ${v}/10</span>` +
      `<div style="margin-top:3px;height:4px;background:rgba(255,255,255,0.08);border-radius:2px;">` +
      `<div style="height:100%;width:${v * 10}%;background:${color};border-radius:2px;"></div></div>`;
  } else if (colorMode === "outlook") {
    const v = d.outlook;''',
    1  # only first occurrence
)
print("Patch 5: Updated tooltipHighlight")

# PATCH 6: Update tooltip rationale
html = html.replace(
    'tt.querySelector(".tt-rationale").textContent = colorMode === "exposure" ? (d.exposure_rationale || "") : "";',
    'tt.querySelector(".tt-rationale").textContent = colorMode === "exposure" ? (d.exposure_rationale || "") : colorMode === "robot" ? (d.robot_rationale || "") : "";'
)
print("Patch 6: Updated tooltip rationale")

# PATCH 7: Route robot mode in updateStats
html = html.replace(
    '  else updateExposureStats(totalJobs);',
    '  else if (colorMode === "robot") updateRobotStats(totalJobs);\n  else updateExposureStats(totalJobs);'
)
print("Patch 7: Updated updateStats routing")

# PATCH 8: Add updateRobotStats function
robot_fn = '''

function updateRobotStats(totalJobs) {
  let wS = 0, wC = 0;
  for (const d of data) { if (d.robot_exposure != null && d.jobs) { wS += d.robot_exposure * d.jobs; wC += d.jobs; } }
  const avg = wC > 0 ? wS / wC : 0;
  document.getElementById("block2").innerHTML = `<h3>Avg. robot exposure</h3>
    <div class="stat-big"><span style="color:${robotColor(avg, 1)}">${avg.toFixed(1)}</span></div>
    <div class="stat-label">job-weighted, 0\\u201310</div>`;

  const histogram = new Array(11).fill(0);
  for (const d of data) { if (d.robot_exposure != null && d.jobs) histogram[d.robot_exposure] += d.jobs; }
  const maxH = Math.max(...histogram);
  document.getElementById("block3").innerHTML = `<h3>Jobs by robot exposure</h3>
    <div class="histogram">${histogram.map((c, i) => `<div class="bar" style="height:${Math.max(2, maxH > 0 ? c / maxH * 100 : 0)}%;background:${robotColor(i, 0.7)}"></div>`).join("")}</div>
    <div class="hist-labels"><span>0</span><span>5</span><span>10</span></div>`;

  const tierDefs = [
    { label: "Minimal (0\\u20131)", lo: 0, hi: 1, mid: 0.5 },
    { label: "Low (2\\u20133)", lo: 2, hi: 3, mid: 2.5 },
    { label: "Moderate (4\\u20135)", lo: 4, hi: 5, mid: 4.5 },
    { label: "High (6\\u20137)", lo: 6, hi: 7, mid: 6.5 },
    { label: "Very high (8\\u201310)", lo: 8, hi: 10, mid: 9 },
  ];
  const tiers = tierDefs.map(t => {
    let jobs = 0;
    for (const d of data) { if (d.robot_exposure != null && d.jobs && d.robot_exposure >= t.lo && d.robot_exposure <= t.hi) jobs += d.jobs; }
    return { ...t, jobs, color: robotColor(t.mid, 1) };
  });
  document.getElementById("block4").innerHTML = `<h3>Robot exposure tiers</h3><div class="tier-bar">${renderTiers(tiers, totalJobs)}</div>`;

  const byPay = weightedAvgByGroups(PAY_BANDS, (d, g) => d.pay != null && d.pay >= g.min && d.pay < g.max, d => d.robot_exposure);
  document.getElementById("block5").innerHTML = `<h3>Robot exp. by pay</h3><div class="hbar-chart">${renderHbars(byPay.map(g => ({
    label: g.label, val: g.avg.toFixed(1), pct: g.avg / 10 * 100, color: robotColor(g.avg, 0.8)
  })))}</div>`;

  const byEdu = weightedAvgByGroups(EDU_GROUPS, (d, g) => g.match.includes(d.education), d => d.robot_exposure);
  document.getElementById("block6").innerHTML = `<h3>Robot exp. by education</h3><div class="hbar-chart">${renderHbars(byEdu.map(g => ({
    label: g.label, val: g.avg.toFixed(1), pct: g.avg / 10 * 100, color: robotColor(g.avg, 0.8)
  })))}</div>`;

  const aiTiers = [
    { label: "AI 0\\u20133", lo: 0, hi: 3 },
    { label: "AI 4\\u20136", lo: 4, hi: 6 },
    { label: "AI 7\\u201310", lo: 7, hi: 10 },
  ];
  const byAI = weightedAvgByGroups(aiTiers, (d, g) => d.exposure != null && d.exposure >= g.lo && d.exposure <= g.hi, d => d.robot_exposure);
  document.getElementById("block7").innerHTML = `<h3>Robot exp. by AI exp.</h3><div class="hbar-chart">${renderHbars(byAI.map(g => ({
    label: g.label, val: g.avg.toFixed(1), pct: g.avg / 10 * 100, color: robotColor(g.avg, 0.8)
  })))}</div>`;

  let wagesExposed = 0;
  for (const d of data) { if (d.robot_exposure != null && d.robot_exposure >= 5 && d.jobs && d.pay) wagesExposed += d.jobs * d.pay; }
  document.getElementById("block8").innerHTML = `<h3>Wages at risk</h3>
    <div class="stat-big" style="color:${robotColor(7, 1)}">$${(wagesExposed / 1e12).toFixed(1)}T</div>
    <div class="stat-label">annual, robot score 5+</div>`;
}

'''

html = html.replace('// \u2500\u2500 Events', robot_fn + '// \u2500\u2500 Events')
print("Patch 8: Added updateRobotStats function")

# PATCH 9: Update LEGEND_CONFIG
html = html.replace(
    '''const LEGEND_CONFIG = {
  exposure:  { low: "Low", high: "High" },
  outlook:   { low: "Declining", high: "Growing" },''',
    '''const LEGEND_CONFIG = {
  exposure:  { low: "Low", high: "High" },
  robot:     { low: "Low", high: "High" },
  outlook:   { low: "Declining", high: "Growing" },'''
)
print("Patch 9: Updated LEGEND_CONFIG")

# PATCH 10: Update gradient legend for robot mode
html = html.replace(
    'gctx.fillStyle = colorMode === "exposure" ? greenRedCSS(t, 1) : greenRedCSS(1 - t, 1);',
    'gctx.fillStyle = (colorMode === "exposure" || colorMode === "robot") ? greenRedCSS(t, 1) : greenRedCSS(1 - t, 1);'
)
print("Patch 10: Updated gradient legend")

# PATCH 11: Update intro text
html = html.replace(
    '<p><b>LLM-powered coloring:</b> The <a href="https://github.com/karpathy/jobs">source code</a> includes scrapers, parsers, and a pipeline for writing custom LLM prompts to score and color occupations by any criteria. You write a prompt, the LLM scores each occupation, and the treemap colors accordingly. The &ldquo;Digital AI Exposure&rdquo; option is one example &mdash; it estimates how much current AI (which is primarily digital) will reshape each occupation. But you could write a different prompt for any question &mdash; e.g. exposure to humanoid robotics, offshoring risk, climate impact &mdash; and re-run the pipeline to get a different coloring.</p>',
    '<p><b>Dual-dimension exposure:</b> This version includes two LLM-scored layers. <b>Digital AI Exposure</b> (original, by Gemini Flash) estimates how much current AI will reshape each occupation. <b>Robot Exposure</b> (added layer, by Claude) estimates how much humanoid robots (Tesla Optimus, Figure, Atlas) could physically replace each occupation within 10 years. Toggle between them to see how different automation types affect different jobs.</p>'
)
# Also try the straight-quote version
html = html.replace(
    '<p><b>LLM-powered coloring:</b> The <a href="https://github.com/karpathy/jobs">source code</a> includes scrapers, parsers, and a pipeline for writing custom LLM prompts to score and color occupations by any criteria. You write a prompt, the LLM scores each occupation, and the treemap colors accordingly. The "Digital AI Exposure" option is one example',
    '<p><b>Dual-dimension exposure:</b> This version includes two LLM-scored layers. <b>Digital AI Exposure</b> (original, by Gemini Flash) estimates how much current AI will reshape each occupation. <b>Robot Exposure</b> (added layer, by Claude) estimates how much humanoid robots could physically replace each occupation within 10 years. Toggle between them to see how different automation types affect different jobs.'
)
print("Patch 11: Updated intro text")

with open("index.html", "w") as f:
    f.write(html)

print("\nAll patches applied! Restart server to see changes.")
