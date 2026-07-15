#!/usr/bin/env python3
"""
build-eva-cache.py — 每日预载 EVA 产品缓存

从 BC API 拉取所有 OH > 0 的产品，写入本地 JSON 缓存。
由 cron 每天凌晨执行一次。Proxy 侧直接读缓存文件，零 API 开销。

Usage:
    python tools/build-eva-cache.py              # 下载并写入今日缓存
    python tools/build-eva-cache.py --date 2026-07-14   # 指定日期目录

Output:
    ~/AppData/Local/hermes/profiles/exie-web/workspace/EVAcache/{YYYY-MM-DD}/
    ├── products.json     # 全量产品列表
    ├── by-sku.json       # SKU → product 索引
    └── by-brand.json     # brand → [products] 索引
"""

import json, os, sys, time
import urllib.request, urllib.error
from datetime import date
from pathlib import Path
from collections import defaultdict

# ── Config ──
CACHE_ROOT = Path.home() / "AppData/Local/hermes/profiles/exie-web/workspace/EVAcache"
TODAY = date.today()

# ── Load BC credentials ──
_env_candidates = [
    Path(os.environ.get("HERMES_PROFILE_DIR", "")) / "extremepc.env",
    Path.home() / "AppData/Local/hermes/profiles/exie/extremepc.env",
]
for _p in _env_candidates:
    if _p.exists():
        with open(_p) as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _k, _v = _line.split("=", 1)
                    os.environ.setdefault(_k.strip(), _v.strip())

STORE = os.environ.get("BC_STORE_HASH", "ms4wz8cgi2")
TOKEN = os.environ.get("BC_ACCESS_TOKEN", "")
if not TOKEN:
    print("Error: BC_ACCESS_TOKEN not set.", file=sys.stderr)
    sys.exit(1)

BASE  = f"https://api.bigcommerce.com/stores/{STORE}/v3"
HEADERS = {
    "X-Auth-Token": TOKEN,
    "Accept": "application/json",
}


def api_get(path):
    url = f"{BASE}{path}"
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(2)
                continue
            print(f"  [API Error {e.code}] {url}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"  [Error] {e}", file=sys.stderr)
            return None
    return None


def get_all_pages(path_base):
    """Paginate through all results."""
    all_data = []
    page = 1
    while True:
        result = api_get(f"{path_base}&page={page}&limit=250")
        if not result or not result.get("data"):
            break
        all_data.extend(result["data"])
        meta = result.get("meta", {}).get("pagination", {})
        total_pages = meta.get("total_pages", 1)
        print(f"    page {page}/{total_pages} — {len(all_data)} so far", file=sys.stderr)
        if page >= total_pages:
            break
        page += 1
        # Rate limit: 150 req/30s → 5 req/s → pause every 40 calls
        if page % 40 == 0:
            time.sleep(2)
    return all_data


def get_oh(custom_fields):
    """Extract Onehunga stock from inline custom_fields list."""
    for cf in (custom_fields or []):
        if "Onehunga" in cf.get("name", ""):
            try:
                return int(cf["value"])
            except (ValueError, TypeError):
                return 0
    return 0


# ── Parse args ──
cache_date = TODAY
for i, a in enumerate(sys.argv[1:], 1):
    if a == "--date" and i < len(sys.argv):
        from datetime import datetime
        cache_date = datetime.strptime(sys.argv[i + 1], "%Y-%m-%d").date()

CACHE_DIR = CACHE_ROOT / cache_date.strftime("%Y-%m-%d")

# ── Main ──
print("=== EVA Cache Builder ===", file=sys.stderr)
print(f"  Cache dir: {CACHE_DIR}", file=sys.stderr)
print(file=sys.stderr)

# Step 1: Fetch all available & visible products
print("Step 1/3: Fetching all products...", file=sys.stderr)
products = get_all_pages(
    f"/catalog/products"
    f"?availability=available"
    f"&is_visible=true"
    f"&include_fields=id,name,sku,price,calculated_price,brand_id,custom_url"
    f"&include=custom_fields"
)
print(f"  → {len(products)} total products fetched", file=sys.stderr)

if not products:
    print("No products found. Nothing to cache.", file=sys.stderr)
    sys.exit(1)

# Step 2: Build brands lookup
print("Step 2/3: Loading brand names...", file=sys.stderr)
brands = {}
page = 1
while True:
    brand_result = api_get(f"/catalog/brands?limit=250&page={page}")
    if not brand_result or not brand_result.get("data"):
        break
    for b in brand_result["data"]:
        brands[b["id"]] = b["name"]
    meta = brand_result.get("meta", {}).get("pagination", {})
    if page >= meta.get("total_pages", 1):
        break
    page += 1
print(f"  → {len(brands)} brands cached", file=sys.stderr)

# Step 3: Filter OH > 0, build indexes
print("Step 3/3: Building indexes...", file=sys.stderr)

products_out = []
by_sku = {}
by_brand = defaultdict(list)

for p in products:
    oh = get_oh(p.get("custom_fields", []))
    if oh == 0:
        continue  # skip OOS

    # Use calculated_price (reflects sales/discounts) or fall back to price
    price_base = p.get("calculated_price") or p.get("price", 0)
    price_gst = round(price_base * 1.15, 2)
    url = "https://www.extremepc.co.nz" + p["custom_url"]["url"]
    brand = brands.get(p.get("brand_id"), "Unknown")

    entry = {
        "id": p["id"],
        "sku": p["sku"],
        "name": p["name"],
        "brand": brand,
        "price_nzd_inc_gst": price_gst,
        "url": url,
        "oh_stock": oh,
    }

    products_out.append(entry)
    by_sku[p["sku"]] = entry
    by_brand[brand].append(entry)

# Sort: most stock first
products_out.sort(key=lambda r: -r["oh_stock"])

print(f"  → {len(products_out)} in-stock (OH > 0) products", file=sys.stderr)

# ── Write cache ──
print(f"\nWriting cache to {CACHE_DIR}...", file=sys.stderr)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

cache_meta = {
    "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    "date": cache_date.strftime("%Y-%m-%d"),
    "total_products": len(products_out),
    "total_brands": len(by_brand),
}

with open(CACHE_DIR / "products.json", "w", encoding="utf-8") as f:
    json.dump({"meta": cache_meta, "products": products_out}, f, ensure_ascii=False, indent=2)

with open(CACHE_DIR / "by-sku.json", "w", encoding="utf-8") as f:
    json.dump(by_sku, f, ensure_ascii=False, indent=2)

with open(CACHE_DIR / "by-brand.json", "w", encoding="utf-8") as f:
    json.dump(dict(by_brand), f, ensure_ascii=False, indent=2)

# Write latest symlink (or marker file on Windows)
latest_marker = CACHE_ROOT / "latest.txt"
with open(latest_marker, "w") as f:
    f.write(cache_date.strftime("%Y-%m-%d"))

# Stats
brand_counts = {b: len(v) for b, v in sorted(by_brand.items(), key=lambda x: -len(x[1]))}
print(f"\n{'='*40}", file=sys.stderr)
print(f"  ✅ Cache built: {cache_date}", file=sys.stderr)
print(f"  📁 {CACHE_DIR}", file=sys.stderr)
print(f"  📦 {len(products_out)} products, {len(by_brand)} brands", file=sys.stderr)
print(f"  Files:", file=sys.stderr)
print(f"    products.json   — full list (sorted by stock)", file=sys.stderr)
print(f"    by-sku.json     — SKU lookup index", file=sys.stderr)
print(f"    by-brand.json   — brand-grouped index", file=sys.stderr)
print(f"    latest.txt      — points to current date", file=sys.stderr)
print(file=sys.stderr)

# Top brands preview
print("  Top brands:", file=sys.stderr)
for bname, cnt in list(brand_counts.items())[:10]:
    print(f"    {bname:25s} {cnt} products", file=sys.stderr)
print(f"{'='*40}", file=sys.stderr)
