#!/usr/bin/env python3
"""
query-category.py — Quick product query by category ID for real-time customer use.

Usage:
    python tools/query-category.py 486                    # list products (no stock check)
    python tools/query-category.py 486 --instock          # only show products with OH > 0
    python tools/query-category.py 486 --summary          # brand overview with price ranges

Optimisations:
    - availability=available&is_visible=true filtered server-side (skips hidden products)
    - include=custom_fields returns stock inline — no per-product API calls
    - Only OH (Onehunga) checked for stock — WL/SL/SU are internal, not customer-available
    - Net: 2 API calls total (products + brands) regardless of category size
"""

import json
import sys
import time
import urllib.request
import urllib.error

# === Config ===
STORE = "ms4wz8cgi2"
TOKEN = "iedxfd72bgz2h46qz2pyc7ghsllrw01"
BASE  = f"https://api.bigcommerce.com/stores/{STORE}/v3"
HEADERS = {
    "X-Auth-Token": TOKEN,
    "Accept": "application/json",
}

# === Args ===
do_instock_only = "--instock" in sys.argv
do_summary      = "--summary" in sys.argv

cat_ids = [a for a in sys.argv[1:] if a.isdigit()]
if not cat_ids:
    print("Usage: python tools/query-category.py <category_id> [--instock] [--summary]")
    print("       --instock   only show products with OH stock > 0")
    print("       --summary   show brand overview instead of individual products")
    sys.exit(1)

CAT_ID = int(cat_ids[0])


def api_get(path):
    url = f"{BASE}{path}"
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
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
        if page >= meta.get("total_pages", 1):
            break
        page += 1
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


def stock_label(oh):
    if oh == 0:
        return "❌ Out of stock"
    elif oh <= 3:
        return "⚠️  Only a few left"
    else:
        return "✅ In stock"


# === Main ===
print(f"\n=== Category {CAT_ID} ===\n")

# One paginated call — available+visible products with custom_fields inline
print("  Fetching...", end="", file=sys.stderr)
products = get_all_pages(
    f"/catalog/products"
    f"?categories:in={CAT_ID}"
    f"&availability=available"
    f"&is_visible=true"
    f"&include_fields=id,name,sku,price,brand_id,custom_url"
    f"&include=custom_fields"
)
print(f" {len(products)} products", file=sys.stderr)

if not products:
    print("  No products found.")
    sys.exit(0)

# Brand lookup (one call)
print("  Loading brands...", end="", file=sys.stderr)
brand_result = api_get("/catalog/brands?limit=250")
brands = {}
if brand_result and brand_result.get("data"):
    for b in brand_result["data"]:
        brands[b["id"]] = b["name"]
print(f" {len(brands)} cached", file=sys.stderr)
print()

# Build result list with OH stock
results = []
for p in products:
    oh    = get_oh(p.get("custom_fields", []))
    price = round(p["price"] * 1.15)
    url   = "https://www.extremepc.co.nz" + p["custom_url"]["url"]
    brand = brands.get(p.get("brand_id"), "")
    results.append({
        "oh": oh, "price": price, "name": p["name"],
        "sku": p["sku"], "url": url, "brand": brand,
    })

# Filter in-stock
if do_instock_only:
    results = [r for r in results if r["oh"] > 0]

# Sort: in-stock first, then by OH desc
results.sort(key=lambda r: r["oh"], reverse=True)

# --summary mode
if do_summary:
    from collections import defaultdict
    by_brand = defaultdict(lambda: {"count": 0, "min": 9999999, "max": 0})
    for r in results:
        b = r["brand"] or "Unknown"
        by_brand[b]["count"] += 1
        by_brand[b]["min"] = min(by_brand[b]["min"], r["price"])
        by_brand[b]["max"] = max(by_brand[b]["max"], r["price"])

    label = "in-stock " if do_instock_only else ""
    print(f"  {len(results)} {label}products across {len(by_brand)} brands:\n")
    for bname, info in sorted(by_brand.items(), key=lambda x: -x[1]["count"]):
        rng = f"${info['min']}" if info["min"] == info["max"] else f"${info['min']} – ${info['max']}"
        print(f"    {bname:22s}  {info['count']:3d} products   {rng}")
    print()
    sys.exit(0)

# Product list
for r in results:
    label     = stock_label(r["oh"])
    brand_tag = f" [{r['brand']}]" if r["brand"] else ""
    print(f"  {label}{brand_tag}  ${r['price']}  {r['name'][:55]}")
    print(f"           SKU: {r['sku']} | {r['url']}")
    print()

print(f"  ── {len(results)} products shown")
