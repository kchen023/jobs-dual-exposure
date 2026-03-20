#!/usr/bin/env python3
"""
Run from ~/jobs/site/:
  python3 add_robot_prompt.py

Adds a collapsible "View the Robot Exposure scoring prompt" section
after the existing AI Exposure prompt section.
"""

with open("index.html", "r") as f:
    html = f.read()

with open("index.html.before_prompt_patch", "w") as f:
    f.write(html)
print("Backed up -> index.html.before_prompt_patch")

robot_prompt_block = '''    <details>
      <summary>View the Robot Exposure scoring prompt</summary>
      <div class="prompt-box">You are an expert analyst evaluating how exposed different occupations are to replacement by humanoid robots. You will be given a detailed description of an occupation from the Bureau of Labor Statistics.

Rate the occupation's overall Humanoid Robot Replacement Risk on a scale from 0 to 10.

This measures: how much could general-purpose humanoid robots (e.g. Tesla Optimus, Figure 02, Boston Dynamics Atlas) replace the core physical tasks of this occupation within 10 years?

The key evaluation axis is physical task automation, NOT digital/cognitive task automation. Focus on:
- The controllability and predictability of the physical environment (factory > warehouse > indoor service > outdoor construction > unstructured wilderness)
- The repetitiveness and standardization of physical tasks
- The required level of fine motor dexterity
- The need for real-time human interpersonal interaction

Use these anchors to calibrate your score:

- 0-1: Minimal risk. The work is entirely performed on a computer with no physical labor component. A humanoid robot provides zero advantage. Examples: software developer, data scientist, writer.

- 2-3: Low risk. The work requires extremely high-precision manual skills or occurs in complex, unstructured physical environments that challenge current robot capabilities. Examples: surgeon, dentist, electrician, plumber.

- 4-5: Moderate risk. A mix of physical and cognitive/social tasks. Some physical components could be assisted by robots, but interpersonal or judgment-heavy aspects remain human-centric. Examples: registered nurse, cook, retail salesperson.

- 6-7: High risk. Repetitive physical work in structured environments. Robots can handle most core physical tasks, though some variability remains. Examples: warehouse stocker, mail carrier, security guard on patrol.

- 8-9: Very high risk. Highly repetitive physical labor in controlled, predictable environments. The work involves standardized motions with minimal judgment. Examples: janitor (indoor cleaning), hand laborer/material mover, food processing worker.

- 10: Maximum risk. Pure repetitive physical operation at a fixed workstation with completely predictable environment and zero judgment required. Examples: assembly line worker.

Important: This dimension is complementary to, not overlapping with, AI Exposure. A software developer (AI Exposure 9/10) has Robot Exposure 0/10. A janitor (AI Exposure 1/10) has Robot Exposure 8/10.

Respond with ONLY a JSON object in this exact format, no other text:
{"score": &lt;0-10&gt;, "rationale": "&lt;2-3 sentences explaining the key physical task characteristics and environment controllability&gt;"}</div>
    </details>'''

# Find the closing </details> of the AI Exposure prompt and insert after it
# The AI prompt details block ends, then there's the Caveat paragraph
target = '''    </details>
    <p><b>Caveat on Digital AI Exposure scores:</b>'''

replacement = '''    </details>
''' + robot_prompt_block + '''
    <p><b>Caveat on Digital AI Exposure scores:</b>'''

if target in html:
    html = html.replace(target, replacement)
    print("Added Robot Exposure prompt section")
else:
    print("WARNING: Could not find insertion point. Trying alternate...")
    # Try without leading spaces
    target2 = '</details>\n    <p><b>Caveat'
    if target2 in html:
        html = html.replace(target2, '</details>\n' + robot_prompt_block + '\n    <p><b>Caveat', 1)
        print("Added Robot Exposure prompt section (alternate match)")
    else:
        print("ERROR: Could not find insertion point. No changes made.")
        exit(1)

with open("index.html", "w") as f:
    f.write(html)

print("\nDone!")
print("Preview: python3 -m http.server 8000")
print("Revert: cp index.html.before_prompt_patch index.html")
