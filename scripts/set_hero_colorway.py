#!/usr/bin/env python3
"""Step 2: write hero_colorway field per model + drop old hero_img/hero_palette/hero_image
so resolveImage will pick the colorway's image as hero."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "data", "sneakers.json")

HERO_CHOICE = {
    # AJ
    "aj1": "Chicago",
    "aj2": "Chicago OG",
    "aj3": "White Cement",
    "aj4": "White Cement",
    "aj5": "Fire Red",
    "aj6": "Infrared",
    "aj7": "Bordeaux",
    "aj8": "Playoffs",
    "aj9": "Statue (Charcoal)",
    "aj10": "Chicago",
    "aj11": "Concord",
    "aj12": "Flu Game",
    "aj13": "Bred",
    "aj14": "Last Shot",
    # Kobe
    "kobe1": "81 Point Game",
    "kobe2": "Lightning",
    "kobe3": "All-Star",
    "kobe4": "Del Sol",
    "kobe5": "Chaos (Joker)",
    "kobe6": "Grinch",
    "kobe7": "Predator",
    "kobe8": "Venomenon",
    "kobe9": "Masterpiece",
    "kobe10": "Fade to Black (Elite)",
    "kobe11": "Achilles Heel",
}

with open(P, "r", encoding="utf-8") as f:
    d = json.load(f)

for series in ("jordan", "kobe"):
    for m in d[series]["models"]:
        if m.get("id") == "placeholder": continue
        if m["id"] in HERO_CHOICE:
            m["hero_colorway"] = HERO_CHOICE[m["id"]]
            # remove stale hero_img: let resolveImage pick from colorway
            m.pop("hero_img", None)
            m.pop("hero_image", None)
            # keep hero_palette as ultimate fallback
        # validate the named colorway exists
        names = [cw["name"] for cw in m.get("colorways", [])]
        if m.get("hero_colorway") not in names:
            print(f"WARN {m['id']}: hero_colorway '{m.get('hero_colorway')}' not in colorways {names}")

# Set top-level cover_img from hero of AJ1 / Kobe11 via colorway's img
def colorway_img(series, model_id, cw_name):
    for m in d[series]["models"]:
        if m["id"] == model_id:
            for cw in m["colorways"]:
                if cw["name"] == cw_name:
                    return cw.get("img")
    return None

j_cover = colorway_img("jordan", "aj1", "Chicago")
k_cover = colorway_img("kobe", "kobe11", "Achilles Heel")
if j_cover: d["jordan"]["cover_img"] = j_cover
if k_cover: d["kobe"]["cover_img"] = k_cover

with open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f"hero_colorway set for {len(HERO_CHOICE)} models. cover_jordan={j_cover}, cover_kobe={k_cover}")
