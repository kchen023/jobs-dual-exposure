#!/usr/bin/env python3
"""
Run from ~/jobs/:
  python3 inject_dual_scores_v2.py

Merges robot exposure scores into data.json, with slug mapping fixes.
"""
import json, os, shutil, subprocess, sys

os.chdir(os.path.expanduser("~/jobs"))

# Step 1: Restore original AI exposure scores
print("Step 1: Restoring original AI exposure scores...")
shutil.copy2("scores_backup_original.json", "scores.json")
print("  Done")

# Step 2: Rebuild data.json
print("Step 2: Rebuilding data.json...")
result = subprocess.run(["uv", "run", "python", "build_site_data.py"], capture_output=True, text=True)
if result.returncode != 0:
    print(f"ERROR:\n{result.stderr}")
    sys.exit(1)
print(f"  {result.stdout.strip()}")

# Step 3: Load data.json
print("Step 3: Loading data.json...")
with open("site/data.json") as f:
    data = json.load(f)
print(f"  {len(data)} occupations")

# Step 4: Load robot scores
print("Step 4: Loading robot scores...")
for path in ["scores_case1_robot.json", os.path.expanduser("~/Downloads/scores_case1_robot.json")]:
    if os.path.exists(path):
        with open(path) as f:
            robot_data = json.load(f)
        print(f"  Loaded {len(robot_data)} from {path}")
        break
else:
    print("ERROR: scores_case1_robot.json not found"); sys.exit(1)

# Build robot lookup by slug
robot_by_slug = {e["slug"]: e for e in robot_data}

# Manual mapping: original_slug -> robot_slug
# These are the 53 cases where BLS uses a different slug than our generated one
SLUG_MAP = {
    "administrative-services-managers": "administrative-services-and-facilities-managers",
    "adult-literacy-and-ged-teachers": "adult-basic-and-secondary-education-and-esl-teachers",
    "aerospace-engineering-and-operations-technicians": "aerospace-engineering-and-operations-technologists-and-technicians",
    "announcers": "announcers-and-djs",
    "curators-museum-technicians-and-conservators": "archivists-curators-and-museum-workers",
    "biomedical-engineers": "bioengineers-and-biomedical-engineers",
    "broadcast-and-sound-engineering-technicians": "broadcast-sound-and-video-technicians",
    "butchers-and-meat-cutters": "butchers",
    "civil-engineering-technicians": "civil-engineering-technologists-and-technicians",
    "conservation-scientists": "conservation-scientists-and-foresters",
    "correctional-officers": "correctional-officers-and-bailiffs",
    "court-reporters": "court-reporters-and-simultaneous-captioners",
    "database-administrators": "database-administrators-and-architects",
    "delivery-truck-drivers-and-driver-sales-workers": "delivery-truck-drivers-and-driversales-workers",
    "drywall-and-ceiling-tile-installers-and-tapers": "drywall-installers-ceiling-tile-installers-and-tapers",
    "electrical-and-electronics-engineering-technicians": "electrical-and-electronic-engineering-technologists-and-technicians",
    "line-installers-and-repairers": "electrical-power-line-installers-and-repairers",
    "electro-mechanical-technicians": "electro-mechanical-and-mechatronics-technologists-and-technicians",
    "elevator-installers-and-repairers": "elevator-and-escalator-installers-and-repairers",
    "environmental-engineering-technicians": "environmental-engineering-technologists-and-technicians",
    "fire-inspectors-and-investigators": "fire-inspectors",
    "fishers-and-related-fishing-workers": "fishing-and-hunting-workers",
    "tile-and-marble-setters": "flooring-installers-and-tile-and-stone-setters",
    "food-and-tobacco-processing-workers": "food-processing-equipment-workers",
    "funeral-service-occupations": "funeral-service-workers",
    "gaming-services-occupations": "gambling-services-workers",
    "geological-and-petroleum-technicians": "geological-and-hydrologic-technicians",
    "health-educators": "health-education-specialists",
    "home-health-aides-and-personal-care-aides": "home-health-and-personal-care-aides",
    "industrial-engineering-technicians": "industrial-engineering-technologists-and-technicians",
    "industrial-machinery-mechanics-and-maintenance-workers-and-millwrights": "industrial-machinery-mechanics-machinery-maintenance-workers-and-millwrights",
    "structural-iron-and-steel-workers": "ironworkers",
    "librarians": "librarians-and-library-media-specialists",
    "brickmasons-blockmasons-and-stonemasons": "masonry-workers",
    "mechanical-engineering-technicians": "mechanical-engineering-technologists-and-technicians",
    "medical-records-and-health-information-technicians": "health-information-technologists-and-medical-registrars",
    "reporters-correspondents-and-broadcast-news-analysts": "news-analysts-reporters-and-journalists",
    "nursing-assistants": "nursing-assistants-and-orderlies",
    "opticians-dispensing": "opticians",
    "appraisers-and-assessors-of-real-estate": "property-appraisers-and-assessors",
    "public-relations-managers": "public-relations-and-fundraising-managers",
    "police-fire-and-ambulance-dispatchers": "public-safety-telecommunicators",
    "radiologic-technologists": "radiologic-and-mri-technologists",
    "railroad-occupations": "railroad-workers",
    "school-and-career-counselors": "school-and-career-counselors-and-advisors",
    "security-guards": "security-guards-and-gambling-surveillance-officers",
    "software-developers": "software-developers-quality-assurance-analysts-and-testers",
    "multimedia-artists-and-animators": "special-effects-artists-and-animators",
    "surgical-technologists": "surgical-assistants-and-technologists",
    "taxi-drivers-and-chauffeurs": "taxi-drivers-shuttle-drivers-and-chauffeurs",
    "telecommunications-equipment-installers-and-repairers-except-line-installers": "telecommunications-technicians",
    "water-transportation-occupations": "water-transportation-workers",
    "web-developers": "web-developers-and-digital-designers",
}

# Step 5: Merge
print("Step 5: Merging...")
matched = 0
still_unmatched = []

for occ in data:
    slug = occ.get("slug", "")
    
    # Direct match
    if slug in robot_by_slug:
        r = robot_by_slug[slug]
        occ["robot_exposure"] = r["exposure"]
        occ["robot_rationale"] = r["rationale"]
        matched += 1
    # Mapped match
    elif slug in SLUG_MAP and SLUG_MAP[slug] in robot_by_slug:
        r = robot_by_slug[SLUG_MAP[slug]]
        occ["robot_exposure"] = r["exposure"]
        occ["robot_rationale"] = r["rationale"]
        matched += 1
    else:
        still_unmatched.append(slug)
        occ["robot_exposure"] = None
        occ["robot_rationale"] = ""

print(f"  Matched: {matched}/{len(data)}")
if still_unmatched:
    print(f"  Still unmatched ({len(still_unmatched)}): {still_unmatched}")

# Step 6: Write
print("Step 6: Writing data.json...")
with open("site/data.json", "w") as f:
    json.dump(data, f, separators=(",", ":"), ensure_ascii=False)

with open("site/data.json") as f:
    verify = json.load(f)
has_robot = sum(1 for d in verify if d.get("robot_exposure") is not None)
has_ai = sum(1 for d in verify if d.get("exposure") is not None)
print(f"  AI exposure: {has_ai}/342")
print(f"  Robot exposure: {has_robot}/342")

if has_robot == 342:
    print("\nPerfect! All 342 occupations have both scores.")
else:
    print(f"\nWARNING: {342 - has_robot} occupations missing robot scores.")

print("Done! Next: cd site && python3 patch_index.py")
