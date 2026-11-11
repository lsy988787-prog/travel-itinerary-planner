#!/usr/bin/env python3
"""Validate the skill against the portable Agent Skills format and test the scripts.

    python scripts/check.py
"""
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "travel-itinerary-planner"
errors = []

text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
m = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
if not m:
    sys.exit("SKILL.md: missing YAML frontmatter")
fields = dict(re.findall(r"^([a-z-]+):\s*(.*)$", m.group(1), re.M))

name = fields.get("name", "")
if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
    errors.append(f"name '{name}' must be lowercase letters/digits/hyphens, ≤ 64 chars")
if name != SKILL.name:
    errors.append(f"name '{name}' must equal folder name '{SKILL.name}'")
desc = fields.get("description", "")
if not desc or len(desc) > 1024:
    errors.append(f"description must be 1–1024 chars (is {len(desc)})")
if len(fields.get("compatibility", "")) > 500:
    errors.append("compatibility must be ≤ 500 chars")
lines = text.count("\n")
if lines > 500:
    errors.append(f"SKILL.md has {lines} lines (keep under 500)")

for ref in re.findall(r"`((?:references|scripts|examples)/[^`*]+?)`", text):
    if not (SKILL / ref.split()[0]).exists():
        errors.append(f"SKILL.md references missing file: {ref}")

with tempfile.TemporaryDirectory() as tmp:
    csv_path = pathlib.Path(tmp, "bill.csv")
    csv_path.write_text(
        "date,item,category,where,amount,currency,status\n"
        "11/23,Flight,Flights,Jet2,38,GBP,paid\n"
        "11/28,Frecciarossa seat,Reservations,Trenitalia app,13,EUR,to book\n"
        "daily,Food,Food,on the spot,420-700,EUR,on the spot\n", encoding="utf-8")
    out = subprocess.run([sys.executable, str(SKILL / "scripts/bill.py"), str(csv_path),
                          "--home", "GBP", "--rate", "EUR:GBP=0.84"],
                         capture_output=True, text=True)
    if out.returncode or "**Total** | **402** | **637**" not in out.stdout:
        errors.append("bill.py: unexpected output\n" + out.stdout + out.stderr)

    try:
        docx = pathlib.Path(tmp, "t.docx")
        r = subprocess.run([sys.executable, str(SKILL / "scripts/md_to_docx.py"),
                            str(SKILL / "examples/rome-benevento-riviera-barcelona-2weeks.md"),
                            str(docx)], capture_output=True, text=True)
        if r.returncode or not docx.exists():
            errors.append("md_to_docx.py failed: " + r.stderr[-300:])
    except FileNotFoundError:
        print("skip: md_to_docx test (pandoc/python-docx missing)")

if errors:
    print("FAIL\n- " + "\n- ".join(errors))
    sys.exit(1)
print(f"OK: name={name}, description={len(desc)} chars, SKILL.md {lines} lines, scripts pass")
