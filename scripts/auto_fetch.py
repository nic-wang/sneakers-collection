#!/usr/bin/env python3
"""Auto-fetch missing images for any model in sneakers.json.
Reads current JSON, finds colorways without img, queries DDG, downloads,
dedups by MD5, writes to assets/img/ with slug filenames.
"""
import urllib.request, urllib.parse, json, re, os, time, hashlib, sys

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT_DIR = os.path.join(ROOT, "assets", "img")
JSON_PATH = os.path.join(ROOT, "data", "sneakers.json")
os.makedirs(OUT_DIR, exist_ok=True)

SLUG_MAP = {
    "bred (banned)": "bred", "bred (playoffs)": "bred", "bred og": "bred", "bred": "bred",
    "chicago og": "chicago", "chicago": "chicago",
    "royal": "royal", "shadow": "shadow",
    "black toe": "black-toe",
    "unc (powder blue)": "unc", "powder blue": "powder-blue",
    "shattered backboard": "sbb",
    "off-white \u00d7 chicago": "offwhite", "off-white \u00d7 black": "offwhite",
    "white cement": "white-cement", "black cement": "black-cement",
    "fire red": "fire-red", "military blue": "military-blue",
    "eminem \u00d7 carhartt": "eminem",
    "metallic silver": "metallic", "grape": "grape", "psg": "psg",
    "infrared": "infrared", "carmine": "carmine",
    "sport blue (olympic)": "sport-blue", "travis scott \u00d7 olive": "travis-scott",
    "bordeaux": "bordeaux", "olympic": "olympic", "raptor": "raptor",
    "playoffs": "playoffs", "aqua": "aqua", "bugs bunny": "bugs-bunny",
    "statue (charcoal)": "statue",
    "venom green": "venom-green",
    "concord": "concord", "space jam": "space-jam", "cool grey": "cool-grey",
    "flu game": "flu-game", "taxi": "taxi",
    "he got game": "he-got-game", "flint": "flint",
    "last shot": "last-shot", "indiglo": "indiglo", "candy cane": "candy-cane",
    # Kobe series
    "81 point game": "81pt",
    "close out": "close-out",
    "mamba rage (protro)": "mamba-rage",
    "lakers home": "lakers-home", "lakers (home)": "lakers-home", "lakers": "lakers",
    "lightning": "lightning",
    "all-star": "all-star",
    "del sol": "del-sol", "carpe diem": "carpe-diem",
    "undefeated \u00d7 gold (protro)": "undefeated",
    "chaos (joker)": "chaos",
    "bruce lee (protro)": "bruce-lee",
    "grinch": "grinch", "venice beach": "venice-beach",
    "mambacita sweet 16 (protro)": "mambacita",
    "predator": "predator", "cheetah": "cheetah",
    "venomenon": "venomenon", "mambacurial": "mambacurial",
    "masterpiece": "masterpiece", "htm black mamba": "htm-black-mamba", "beethoven (low)": "beethoven",
    "fade to black (elite)": "fade-to-black", "htm": "htm",
    "achilles heel": "achilles", "red horse": "red-horse", "bhm": "bhm",
    "mambacita (protro)": "mambacita",
    # Step-3 additions
    "wing it": "wing-it",
    "just don beach": "just-don",
    "quai 54": "quai-54",
    "mocha": "mocha", "true blue": "true-blue",
    "toro bravo": "toro-bravo", "thunder": "thunder",
    "travis scott cactus jack": "travis-cj",
    "laney": "laney", "tokyo 23": "tokyo-23", "what the": "what-the",
    "maroon": "maroon", "dmp (defining moments)": "dmp",
    "hare": "hare", "cardinal": "cardinal", "french blue": "french-blue",
    "three peat": "three-peat", "chrome": "chrome",
    "olive": "olive", "photo blue": "photo-blue",
    "steel": "steel", "stealth": "stealth", "westbrook pe": "westbrook",
    "72-10": "72-10", "win like '96": "win-like-96",
    "jubilee (25th anniversary)": "jubilee",
    "master": "master", "cny (chinese new year)": "cny",
    "reverse flu game": "reverse-flu", "reverse he got game": "reverse-hgg",
    "brave blue": "brave-blue",
    "ferrari yellow": "ferrari", "hyper royal": "hyper-royal",
    "black mamba": "black-mamba", "final game (protro)": "final-game",
    "ftb fade to black": "ftb", "strength white": "strength",
    "houston (all-star pack)": "houston",
    "year of the mamba (protro)": "year-mamba",
    "5 rings": "5-rings", "aces": "aces", "big stage": "big-stage",
    "3d": "3d", "helicopter": "helicopter",
    "reverse grinch (protro)": "reverse-grinch",
    "year of the dragon": "yotd", "christmas": "christmas",
    "olympic galaxy": "olympic-galaxy",
    "sulfur yellow": "sulfur", "christmas (easter)": "easter",
    "all-star (galaxy)": "all-star-galaxy",
    "independence day": "independence", "birds of prey": "birds-of-prey",
    "vino": "vino", "drew league": "drew",
    "eulogy": "eulogy", "tinker hatfield (4kb)": "tinker",
    "ftb (fade to black final)": "ftb-final",
}

def slug(model_id, name):
    s = SLUG_MAP.get(name.lower())
    if s: return f"{model_id}-{s}"
    clean = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return f"{model_id}-{clean}"

def find_existing(base):
    for ext in (".jpg", ".png", ".webp", ".jpeg"):
        p = os.path.join(OUT_DIR, base + ext)
        if os.path.exists(p): return f"assets/img/{base}{ext}"
    return None

def ddg_token(q):
    url = f"https://duckduckgo.com/?q={urllib.parse.quote(q)}&iax=images&ia=images"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
    m = re.search(r"vqd=([\d-]+)", html)
    return m.group(1) if m else None

def ddg_images(q, n=15):
    tok = ddg_token(q)
    if not tok: return []
    url = f"https://duckduckgo.com/i.js?l=us-en&o=json&q={urllib.parse.quote(q)}&vqd={tok}&f=,,,,,&p=1"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://duckduckgo.com/"})
    try:
        data = json.loads(urllib.request.urlopen(req, timeout=12).read())
    except Exception as e:
        print(f"  search fail: {e}"); return []
    return [r["image"] for r in data.get("results", [])[:n]]

def download(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Referer": "https://www.google.com/",
        "Accept": "image/avif,image/webp,image/png,image/jpeg,*/*;q=0.8",
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        c = r.read()
    if len(c) < 15000:
        raise ValueError(f"too small ({len(c)})")
    return c, hashlib.md5(c).hexdigest()

def existing_hashes():
    hashes = set()
    for f in os.listdir(OUT_DIR):
        p = os.path.join(OUT_DIR, f)
        if os.path.isfile(p):
            with open(p, "rb") as fp:
                hashes.add(hashlib.md5(fp.read()).hexdigest())
    return hashes

def fetch_one(base, query, used):
    candidates = ddg_images(query, 15)
    if not candidates:
        print(f"  [{base}] no candidates"); return None
    pri = ["images.stockx.com", "image.goat.com", "sneakerbardetroit.com", "dunkhype.com", "sneakernews.com", "modernnotoriety.com"]
    def score(u):
        for i,h in enumerate(pri):
            if h in u: return i
        return len(pri)
    candidates.sort(key=score)
    for u in candidates:
        try:
            tail = u.lower().split("?")[0][-8:]
            ext = ".png" if ".png" in tail else (".webp" if ".webp" in tail else ".jpg")
            content, h = download(u)
            if h in used:
                print(f"  [{base}] dup {u[:60]}"); continue
            dst = os.path.join(OUT_DIR, base + ext)
            with open(dst, "wb") as f: f.write(content)
            used.add(h)
            print(f"  [{base}] OK {len(content)//1024}KB  \u2190 {u[:70]}")
            return f"assets/img/{base}{ext}"
        except Exception as e:
            print(f"  [{base}] fail {u[:60]}: {e}")
    return None

def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    used = existing_hashes()
    todo = []
    for series_key, brand_prefix in (("jordan", ""), ("kobe", "")):
        models = [m for m in data[series_key]["models"] if m.get("id") != "placeholder"]
        for m in models:
            if not m.get("hero_img"):
                exists = find_existing(f"{m['id']}-hero")
                if exists: m["hero_img"] = exists
                else:
                    q = f'StockX "{m["name"]}" OG side product photo'
                    todo.append((f"{m['id']}-hero", q, "hero_img", m))
            for cw in m.get("colorways", []):
                if cw.get("img"): continue
                base = slug(m["id"], cw["name"])
                exists = find_existing(base)
                if exists:
                    cw["img"] = exists; continue
                q = f'StockX "{m["name"]}" "{cw["name"]}" product photo'
                todo.append((base, q, "img", cw))
    print(f"TODO: {len(todo)} items")
    for base, q, field, target in todo:
        print(f"[{base}] query: {q}")
        path = fetch_one(base, q, used)
        if path:
            target[field] = path
        time.sleep(0.8)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\nDone. JSON updated.")

if __name__ == "__main__":
    main()
