#!/usr/bin/env python3
"""Merge _additions.json into sneakers.json (append by model.id, dedup by colorway name)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "data", "sneakers.json")
A = os.path.join(ROOT, "data", "_additions.json")

with open(P) as f: d = json.load(f)
with open(A) as f: add = json.load(f)["additions"]

# build model index
idx = {}
for series in ("jordan", "kobe"):
    for m in d[series]["models"]:
        idx[m["id"]] = m

added = 0
for mid, new_cws in add.items():
    if mid not in idx:
        print(f"WARN unknown model id: {mid}"); continue
    m = idx[mid]
    existing = {cw["name"] for cw in m.get("colorways", [])}
    for cw in new_cws:
        if cw["name"] in existing:
            print(f"  skip dup: {mid} / {cw['name']}")
            continue
        m["colorways"].append(cw)
        added += 1

with open(P, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

# stats
total_cw = sum(len(m.get("colorways", [])) for s in ("jordan","kobe") for m in d[s]["models"] if m.get("id")!="placeholder")
total_models = sum(1 for s in ("jordan","kobe") for m in d[s]["models"] if m.get("id")!="placeholder")
print(f"\nAdded {added} new colorways. Total: {total_models} models, {total_cw} colorways")
