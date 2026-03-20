# AI & Robotics: A 2D Exposure Visualizer (Extended from Karpathy/Jobs)

**Live site:** [kchen023.github.io/jobs-dual-exposure](https://kchen023.github.io/jobs-dual-exposure/)

An interactive treemap visualizing **342 US occupations** (143M jobs) from the Bureau of Labor Statistics, with **dual-dimension** automation exposure scoring.

## What this is

This project replicates and extends [Andrej Karpathy's Jobs Visualizer](https://karpathy.ai/jobs/) ([source](https://github.com/karpathy/jobs)). The original project scores occupations on a single **Digital AI Exposure** axis. This version adds a second axis: **Humanoid Robot Replacement Risk**.

### Two dimensions of automation - impact on occupations

| Dimension | Scored by | Measures |
|-----------|-----------|----------|
| **Digital AI Exposure** (original) | Gemini Flash | How much will software AI reshape this occupation? |
| **Robot Exposure** (added) | Claude | How much could humanoid robots physically replace this occupation within 10 years? |

These two dimensions are complementary, not overlapping:
- A **software developer** has AI Exposure 9/10 but Robot Exposure 0/10 (pure digital work)
- A **janitor** has AI Exposure 1/10 but Robot Exposure 8/10 (repetitive physical work)
- A **cashier** has AI Exposure 7/10 and Robot Exposure 6/10 (exposed on both fronts)

### Five visualization layers

Toggle between: **BLS Outlook** · **Median Pay** · **Education** · **Digital AI Exposure** · **Robot Exposure**

## LLM scoring methodology

### Digital AI Exposure (original, by Karpathy)

Each occupation was scored 0–10 by Gemini Flash via OpenRouter, measuring how much AI will reshape that occupation. The full scoring prompt is available in the [original repository](https://github.com/karpathy/jobs/blob/master/prompt.md).

**What "AI Exposure" is NOT** (from the original project):
1. It does not predict that a job will disappear. Software developers score 9/10 because AI is transforming their work — but demand for software could easily grow as each developer becomes more productive.
2. It does not account for demand elasticity, latent demand, regulatory barriers, or social preferences for human workers.
3. The scores are rough LLM estimates (Gemini Flash via OpenRouter), not rigorous predictions. Many high-exposure jobs will be reshaped, not replaced.

### Robot Exposure (added dimension)

Each occupation was scored 0–10 by Claude (Anthropic), measuring how much general-purpose humanoid robots could replace the core physical tasks of each occupation within 10 years. The full scoring prompt, methodology, and aggregate statistics are available in our [prompt.md](prompt.md).

**What "Robot Exposure" is NOT:**
1. It does not predict that a job will be fully automated by robots. Janitors score 8/10 because their core tasks (mopping, vacuuming, surface cleaning) are repetitive and occur in semi-structured environments — but navigating cluttered spaces, handling unexpected messes, and working around people remain significant challenges for current-generation robots.
2. It does not account for the cost-effectiveness of deploying humanoid robots vs. human labor. A job may be physically automatable in theory but economically unviable to automate in practice — humanoid robots currently cost far more than the hourly wages of many physical-labor occupations.
3. It does not account for regulatory barriers (e.g. food safety, healthcare licensing), union protections, or public acceptance of robots in human-facing roles (e.g. childcare, elder care).
4. The scores focus exclusively on **physical task replacement** by humanoid robots, not on software AI or specialized industrial automation that already exists (e.g. robotic welding arms, automated conveyor systems). A factory that already uses robotic arms is not what this dimension measures — it measures whether a general-purpose humanoid robot could replace the *human worker* at that factory.
5. The scores are rough LLM estimates (Claude), not engineering assessments. Real-world deployment timelines depend on hardware maturity, sensor capabilities, battery life, and regulatory approval that no LLM can reliably predict.

### Key insight: AI and Robot Exposure are inversely correlated

| AI Exposure tier | Avg Robot Exposure | Interpretation |
|------------------|--------------------|----------------|
| AI 0–3 (low AI risk) | 4.4 | Physical labor — faces robot disruption |
| AI 4–6 (moderate AI risk) | 2.7 | Hybrid roles — moderate on both axes |
| AI 7–10 (high AI risk) | 1.1 | Knowledge work — faces AI disruption |

Low-paying, less-educated, physical jobs face **robot** disruption. High-paying, educated, digital jobs face **AI** disruption. Very few occupations face both simultaneously.

## How the Robot Exposure scores were generated

1. Used Karpathy's `make_prompt.py` to package all 342 occupations into a single prompt file
2. Submitted to Claude with a custom scoring rubric (see [prompt.md](prompt.md) for the full prompt and methodology)
3. Validated all 342 occupation names against the original dataset
4. Merged robot scores into the existing `data.json` alongside the original AI exposure scores
5. Patched `index.html` to add Robot Exposure as a 5th visualization layer with full statistics panel

## Project structure

```
index.html                   # Single-file web app (HTML + CSS + JS)
data.json                    # 342 occupations with all metrics + dual exposure scores
prompt.md                    # Robot Exposure scoring prompt, methodology, and aggregate stats
README.md                    # This file
scripts/                     # Build and patch scripts used during development
  inject_dual_scores_v2.py   # Merges robot scores into data.json
  patch_index.py             # Adds Robot Exposure layer to the UI
  update_safe.py             # Theme and label updates
  add_robot_prompt.py        # Adds robot prompt disclosure section
scores/                      # Score data files
  scores_case1_robot.json    # Robot Exposure scores (342 occupations)
```

## Credits

- **Original project:** [Andrej Karpathy](https://github.com/karpathy/jobs) — data pipeline, treemap visualization, Digital AI Exposure scoring
- **Robot Exposure extension:** Kai Chen — scoring methodology, prompt engineering, UI integration, dual-dimension visualization
- **Data source:** [Bureau of Labor Statistics Occupational Outlook Handbook](https://www.bls.gov/ooh/)
- **LLM scoring:** Gemini Flash (AI Exposure, original), Claude (Robot Exposure, added)

## License

This project builds on [karpathy/jobs](https://github.com/karpathy/jobs). The original project's license applies to the base code and data pipeline. The Robot Exposure scoring and UI extensions are by Kai Chen.
