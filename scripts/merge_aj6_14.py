#!/usr/bin/env python3
"""Merge aj6-14.json into sneakers.json (append to jordan.models)."""
import json, os
ROOT = os.path.join(os.path.dirname(__file__), "..")
main_path = os.path.join(ROOT, "data", "sneakers.json")
extra_path = os.path.join(ROOT, "data", "aj6-14.json")

with open(main_path, "r", encoding="utf-8") as f:
    main = json.load(f)
with open(extra_path, "r", encoding="utf-8") as f:
    extra = json.load(f)

existing_ids = {m["id"] for m in main["jordan"]["models"]}
added = 0
for m in extra["models"]:
    if m["id"] not in existing_ids:
        main["jordan"]["models"].append(m)
        added += 1

# sort by numeric id
def numid(m):
    try: return int(m["id"].replace("aj", "").replace("placeholder", "999"))
    except: return 999
main["jordan"]["models"].sort(key=numid)

with open(main_path, "w", encoding="utf-8") as f:
    json.dump(main, f, ensure_ascii=False, indent=2)

print(f"Merged {added} models. Total Jordan models: {len([m for m in main['jordan']['models'] if m['id'] != 'placeholder'])}")
