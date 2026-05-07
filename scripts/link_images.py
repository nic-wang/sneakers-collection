#!/usr/bin/env python3
"""Auto-link downloaded images into sneakers.json."""
import json, os, glob

ROOT = os.path.join(os.path.dirname(__file__), "..")
JSON_PATH = os.path.join(ROOT, "data", "sneakers.json")
IMG_DIR = os.path.join(ROOT, "assets", "img")

# Build filename index: slug -> relative path
def find(slug):
    for ext in (".jpg", ".png", ".webp", ".jpeg"):
        p = os.path.join(IMG_DIR, slug + ext)
        if os.path.exists(p):
            return f"assets/img/{slug}{ext}"
    return None

# slug conventions per colorway.name
def slugify(model_id, cw_name):
    name = cw_name.lower()
    map_table = {
        "bred (banned)": "bred",
        "bred og": "bred",
        "bred": "bred",
        "chicago og": "chicago",
        "chicago": "chicago",
        "royal": "royal",
        "shadow": "shadow",
        "black toe": "black-toe",
        "unc (powder blue)": "unc",
        "shattered backboard": "sbb",
        "off-white × chicago": "offwhite",
        "off-white × black": "offwhite",
        "white cement": "white-cement",
        "black cement": "black-cement",
        "fire red": "fire-red",
        "military blue": "military-blue",
        "eminem × carhartt": "eminem",
        "metallic silver": "metallic",
        "grape": "grape",
        "psg": "psg",
    }
    suffix = map_table.get(name, name.replace(" ", "-").replace("×", "x"))
    return f"{model_id}-{suffix}"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

touched = 0
for m in data["jordan"]["models"]:
    if m.get("id") == "placeholder":
        continue
    hero = find(f"{m['id']}-hero")
    if hero:
        m["hero_img"] = hero
        touched += 1
    for cw in m.get("colorways", []):
        slug = slugify(m["id"], cw["name"])
        path = find(slug)
        if path:
            cw["img"] = path
            touched += 1
        else:
            print(f"  missing: {m['id']} / {cw['name']} → {slug}")

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nLinked {touched} images into sneakers.json")
