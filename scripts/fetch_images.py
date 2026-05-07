#!/usr/bin/env python3
"""Batch-fetch sneaker product photos via DuckDuckGo image search.
Saves into assets/img/ with predictable filenames.
Usage: python3 scripts/fetch_images.py
"""
import urllib.request, urllib.parse, json, re, os, sys, time, hashlib

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "img")
os.makedirs(OUT_DIR, exist_ok=True)

# (filename, search query)  —— 首项是保存名（不含扩展名），次项是搜索词
TARGETS = [
    # AJ 1
    ("aj1-bred",        "Air Jordan 1 Bred Banned OG 1985 product white bg"),
    ("aj1-chicago",     "Air Jordan 1 Chicago OG 1985 product white bg"),
    ("aj1-royal",       "Air Jordan 1 Royal Blue OG 1985 product white bg"),
    ("aj1-shadow",      "Air Jordan 1 Shadow OG 1985 product white bg"),
    ("aj1-black-toe",   "Air Jordan 1 Black Toe 1985 product white bg"),
    ("aj1-unc",         "Air Jordan 1 UNC University Blue product white bg"),
    ("aj1-sbb",         "Air Jordan 1 Shattered Backboard 2015 product"),
    ("aj1-offwhite",    "Air Jordan 1 Off-White Chicago Virgil Abloh product"),
    ("aj1-hero",        "Air Jordan 1 Chicago side view product photo white bg"),
    # AJ 2
    ("aj2-chicago",     "Air Jordan 2 Chicago OG white red product photo"),
    ("aj2-bred",        "Air Jordan 2 Bred black red OG product photo"),
    ("aj2-offwhite",    "Air Jordan 2 Off-White Black Virgil Abloh product"),
    ("aj2-hero",        "Air Jordan 2 Chicago OG side view product"),
    # AJ 3
    ("aj3-white-cement","Air Jordan 3 White Cement OG product photo"),
    ("aj3-black-cement","Air Jordan 3 Black Cement OG product photo"),
    ("aj3-fire-red",    "Air Jordan 3 Fire Red product photo"),
    ("aj3-hero",        "Air Jordan 3 White Cement side view product"),
    # AJ 4
    ("aj4-bred",        "Air Jordan 4 Bred OG 1989 product photo"),
    ("aj4-white-cement","Air Jordan 4 White Cement OG 1989 product"),
    ("aj4-military-blue","Air Jordan 4 Military Blue OG product"),
    ("aj4-eminem",      "Air Jordan 4 Eminem Carhartt 2015 product"),
    ("aj4-hero",        "Air Jordan 4 Bred side view product"),
    # AJ 5
    ("aj5-fire-red",    "Air Jordan 5 Fire Red OG 1990 product"),
    ("aj5-metallic",    "Air Jordan 5 Metallic Silver OG 1990 product"),
    ("aj5-grape",       "Air Jordan 5 Grape OG 1990 product"),
    ("aj5-psg",         "Air Jordan 5 PSG Paris Saint Germain product"),
    ("aj5-hero",        "Air Jordan 5 Fire Red side view product"),
]

def ddg_token(keywords):
    url = f"https://duckduckgo.com/?q={urllib.parse.quote(keywords)}&iax=images&ia=images"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
    m = re.search(r"vqd=([\d-]+)", html)
    return m.group(1) if m else None

def ddg_images(keywords, max_results=10):
    token = ddg_token(keywords)
    if not token:
        return []
    url = f"https://duckduckgo.com/i.js?l=us-en&o=json&q={urllib.parse.quote(keywords)}&vqd={token}&f=,,,,,&p=1"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://duckduckgo.com/"})
    try:
        data = json.loads(urllib.request.urlopen(req, timeout=12).read())
    except Exception as e:
        print(f"  !! search failed: {e}")
        return []
    return [r["image"] for r in data.get("results", [])[:max_results]]

def download(url, dst):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Referer": "https://www.google.com/",
        "Accept": "image/avif,image/webp,image/png,image/jpeg,*/*;q=0.8",
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        content = r.read()
    if len(content) < 4000:
        raise ValueError(f"too small ({len(content)} bytes)")
    with open(dst, "wb") as f:
        f.write(content)
    return len(content)

def pick_and_save(name, query):
    candidates = ddg_images(query, max_results=10)
    if not candidates:
        print(f"  [{name}] no candidates")
        return False
    # Prefer URLs from well-known shoe CDNs and avoid Shutterstock-watermarked
    priority = ["images.stockx.com", "image.goat.com", "sneakernews.com", "modernnotoriety.com", "sneakerbardetroit.com"]
    def score(u):
        for i, host in enumerate(priority):
            if host in u:
                return i
        return len(priority)
    candidates.sort(key=score)

    for u in candidates:
        try:
            # Try jpg first, but ext will match content
            ext = ".jpg"
            if ".png" in u.lower().split("?")[0][-8:]: ext = ".png"
            elif ".webp" in u.lower().split("?")[0][-8:]: ext = ".webp"
            dst = os.path.join(OUT_DIR, name + ext)
            size = download(u, dst)
            print(f"  [{name}] OK {size//1024}KB  ← {u[:80]}")
            return True
        except Exception as e:
            print(f"  [{name}] fail {u[:60]}: {e}")
            continue
    return False

def main():
    ok = 0
    for name, query in TARGETS:
        # Skip if already exists (any ext)
        existing = [f for f in os.listdir(OUT_DIR) if f.startswith(name + ".")]
        if existing:
            print(f"  [{name}] skip (exists: {existing[0]})")
            ok += 1
            continue
        print(f"[{name}] query: {query}")
        if pick_and_save(name, query):
            ok += 1
        time.sleep(0.8)  # 礼貌间隔
    print(f"\nDone: {ok}/{len(TARGETS)}")

if __name__ == "__main__":
    main()
