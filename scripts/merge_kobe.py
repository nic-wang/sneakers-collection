#!/usr/bin/env python3
"""Replace kobe.models placeholder with full kobe-full.json data."""
import json, os
ROOT = os.path.join(os.path.dirname(__file__), "..")
main_path = os.path.join(ROOT, "data", "sneakers.json")
extra_path = os.path.join(ROOT, "data", "kobe-full.json")

with open(main_path, "r", encoding="utf-8") as f:
    main = json.load(f)
with open(extra_path, "r", encoding="utf-8") as f:
    extra = json.load(f)

main["kobe"]["cover_palette"] = extra["cover_palette"]
main["kobe"]["models"] = extra["models"]

with open(main_path, "w", encoding="utf-8") as f:
    json.dump(main, f, ensure_ascii=False, indent=2)

total_cw = sum(len(m.get("colorways", [])) for m in main["kobe"]["models"])
print(f"Kobe merged: {len(main['kobe']['models'])} models, {total_cw} colorways")
