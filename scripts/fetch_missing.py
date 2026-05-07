#!/usr/bin/env python3
"""Smarter sneaker image fetcher: skip dup MD5, better queries, retry.
Usage: python3 scripts/fetch_missing.py
"""
import urllib.request, urllib.parse, json, re, os, sys, time, hashlib

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "img")
os.makedirs(OUT_DIR, exist_ok=True)

# More specific queries for previously-deduped items
TARGETS = [
    ("aj1-bred",       'StockX "Jordan 1 Retro Bred" 2016 OG banned side product'),
    ("aj1-shadow",     'StockX "Jordan 1 Retro High OG Shadow" grey black product'),
    ("aj1-black-toe",  'StockX "Jordan 1 Retro High OG Black Toe" 2016 product'),
    ("aj1-hero",       'Air Jordan 1 High OG stockx editorial hero shot'),
]

def existing_hashes():
    hashes = {}
    for f in os.listdir(OUT_DIR):
        path = os.path.join(OUT_DIR, f)
        if os.path.isfile(path):
            with open(path, "rb") as fp:
                hashes[f] = hashlib.md5(fp.read()).hexdigest()
    return hashes

def ddg_token(keywords):
    url = f"https://duckduckgo.com/?q={urllib.parse.quote(keywords)}&iax=images&ia=images"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
    m = re.search(r"vqd=([\d-]+)", html)
    return m.group(1) if m else None

def ddg_images(keywords, max_results=20):
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
    h = hashlib.md5(content).hexdigest()
    return content, h

def pick_unique(name, query, used_hashes):
    candidates = ddg_images(query, max_results=20)
    if not candidates:
        print(f"  [{name}] no candidates")
        return False
    priority = ["images.stockx.com", "image.goat.com", "sneakerbardetroit.com", "sneakernews.com", "modernnotoriety.com"]
    def score(u):
        for i, host in enumerate(priority):
            if host in u:
                return i
        return len(priority)
    candidates.sort(key=score)

    for u in candidates:
        try:
            ext = ".jpg"
            tail = u.lower().split("?")[0][-8:]
            if ".png" in tail: ext = ".png"
            elif ".webp" in tail: ext = ".webp"
            content, h = download(u, None)
            if h in used_hashes.values():
                print(f"  [{name}] dup-hash skip {u[:60]}")
                continue
            dst = os.path.join(OUT_DIR, name + ext)
            with open(dst, "wb") as f:
                f.write(content)
            used_hashes[name + ext] = h
            print(f"  [{name}] OK {len(content)//1024}KB  ← {u[:80]}")
            return True
        except Exception as e:
            print(f"  [{name}] fail {u[:60]}: {e}")
            continue
    return False

def main():
    used = existing_hashes()
    for name, query in TARGETS:
        # Already present?
        existing = [f for f in os.listdir(OUT_DIR) if f.startswith(name + ".")]
        if existing:
            print(f"  [{name}] exists: {existing[0]}")
            continue
        print(f"[{name}] query: {query}")
        pick_unique(name, query, used)
        time.sleep(1.0)

if __name__ == "__main__":
    main()
