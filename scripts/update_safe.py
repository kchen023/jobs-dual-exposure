#!/usr/bin/env python3
"""
Run from ~/jobs/site/:
  python3 update_safe.py

3 changes: title, light theme, robot labels.
Each replacement is surgically targeted to avoid breaking JS.
"""

with open("index.html", "r") as f:
    html = f.read()

with open("index.html.safe_backup", "w") as f:
    f.write(html)
print("Backed up -> index.html.safe_backup")

changes = 0

# ═══════════════════════════════════════════════════
# 1. TITLE
# ═══════════════════════════════════════════════════
old = "<title>US Job Market Visualizer — AI + Robot Exposure</title>"
new = "<title>US Job Market Visualizer - Replication + Robot Exposure Dimension</title>"
if old in html:
    html = html.replace(old, new); changes += 1
else:
    old2 = "<title>US Job Market Visualizer</title>"
    if old2 in html:
        html = html.replace(old2, new); changes += 1

old = ">US Job Market Visualizer <a"
new = ">US Job Market Visualizer - Replication + Robot Exposure Dimension <a"
if old in html:
    html = html.replace(old, new); changes += 1
print(f"1. Title: {changes} replacements")

# ═══════════════════════════════════════════════════
# 2. LIGHT THEME — CSS variables only
# ═══════════════════════════════════════════════════
theme_changes = 0

# 2a. Root CSS variables (these are unique and safe)
for old, new in [
    ("--bg: #0a0a0f;", "--bg: #ffffff;"),
    ("--bg2: #12121a;", "--bg2: #f5f5f7;"),
    ("--fg: #e0e0e8;", "--fg: #1d1d1f;"),
    ("--fg2: #888894;", "--fg2: #6e6e73;"),
]:
    if old in html:
        html = html.replace(old, new); theme_changes += 1

# 2b. Canvas background (unique line in draw function)
old = 'ctx.fillStyle = "#0a0a0f";'
new = 'ctx.fillStyle = "#ffffff";'
if old in html:
    html = html.replace(old, new); theme_changes += 1

# 2c. Tooltip background — target the exact CSS rule
old = '''#tooltip {
  position: fixed;
  pointer-events: none;
  background: var(--bg2);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 8px;
  padding: 12px 16px;
  font-size: 13px;
  line-height: 1.5;
  max-width: 340px;
  opacity: 0;
  transition: opacity 0.12s;
  z-index: 20;
  box-shadow: 0 8px 32px rgba(0,0,0,0.6);
}'''
new = '''#tooltip {
  position: fixed;
  pointer-events: none;
  background: #ffffff;
  border: 1px solid rgba(0,0,0,0.12);
  border-radius: 8px;
  padding: 12px 16px;
  font-size: 13px;
  line-height: 1.5;
  max-width: 340px;
  opacity: 0;
  transition: opacity 0.12s;
  z-index: 20;
  box-shadow: 0 8px 32px rgba(0,0,0,0.12);
}'''
if old in html:
    html = html.replace(old, new); theme_changes += 1

# 2d. Tooltip title color — exact CSS rule
old = ".tt-title { font-weight: 600; font-size: 14px; margin-bottom: 6px; color: #fff; }"
new = ".tt-title { font-weight: 600; font-size: 14px; margin-bottom: 6px; color: #1d1d1f; }"
if old in html:
    html = html.replace(old, new); theme_changes += 1

# 2e. Tile text on canvas — exact JS lines
old = 'ctx.fillStyle = isHovered ? "#fff" : "rgba(255,255,255,0.85)";'
new = 'ctx.fillStyle = isHovered ? "#111" : "rgba(0,0,0,0.8)";'
if old in html:
    html = html.replace(old, new); theme_changes += 1

old = 'ctx.fillStyle = "rgba(255,255,255,0.5)";'
new = 'ctx.fillStyle = "rgba(0,0,0,0.5)";'
if old in html:
    html = html.replace(old, new); theme_changes += 1

# 2f. Hover stroke
old = 'ctx.strokeStyle = "#fff";'
new = 'ctx.strokeStyle = "#333";'
if old in html:
    html = html.replace(old, new); theme_changes += 1

# 2g. Color toggle button CSS — exact rules
old = '''.color-toggle button.active {
  background: rgba(255,255,255,0.08);
  color: var(--fg);
  border-color: rgba(255,255,255,0.2);
}
.color-toggle button:hover:not(.active) {
  background: rgba(255,255,255,0.04);
}'''
new = '''.color-toggle button.active {
  background: rgba(0,0,0,0.06);
  color: var(--fg);
  border-color: rgba(0,0,0,0.2);
}
.color-toggle button:hover:not(.active) {
  background: rgba(0,0,0,0.03);
}'''
if old in html:
    html = html.replace(old, new); theme_changes += 1

# 2h. Color toggle button border CSS
old = "border: 1px solid rgba(255,255,255,0.1);"
new = "border: 1px solid rgba(0,0,0,0.1);"
if old in html:
    html = html.replace(old, new); theme_changes += 1

# 2i. Prompt box
old = '''  background: rgba(0,0,0,0.3);
  border: 1px solid rgba(255,255,255,0.06);'''
new = '''  background: rgba(0,0,0,0.03);
  border: 1px solid rgba(0,0,0,0.1);'''
if old in html:
    html = html.replace(old, new); theme_changes += 1

# 2j. Tooltip rationale border
old = "border-top: 1px solid rgba(255,255,255,0.06);"
new = "border-top: 1px solid rgba(0,0,0,0.08);"
if old in html:
    html = html.replace(old, new); theme_changes += 1

# 2k. Histogram bar track
old = "background: rgba(255,255,255,0.04);"
new = "background: rgba(0,0,0,0.04);"
if old in html:
    html = html.replace(old, new); theme_changes += 1

print(f"2. Light theme: {theme_changes} replacements")

# ═══════════════════════════════════════════════════
# 3. ROBOT LABELS — match AI Exposure style
# ═══════════════════════════════════════════════════
label_changes = 0
for old, new in [
    ("Avg. robot exposure", "Avg. exposure"),
    ("Jobs by robot exposure", "Jobs by exposure"),
    ("Robot exposure tiers", "Exposure tiers"),
    ("Robot exp. by pay", "Exposure by pay"),
    ("Robot exp. by education", "Exposure by education"),
    ("Robot exp. by AI exp.", "Exposure by AI tier"),
    ("Wages at risk", "Wages exposed"),
    ("annual, robot score 5+", "annual, in jobs scoring 5+"),
]:
    if old in html:
        html = html.replace(old, new); label_changes += 1

print(f"3. Robot labels: {label_changes} replacements")

with open("index.html", "w") as f:
    f.write(html)

print(f"\nDone! Total replacements: {changes + theme_changes + label_changes}")
print("Preview: python3 -m http.server 8000")
print("Revert if broken: cp index.html.safe_backup index.html")
