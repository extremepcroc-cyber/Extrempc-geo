#!/usr/bin/env python3
"""
query-category.py — Quick product query by category ID for real-time customer use.

Usage:
    python tools/query-category.py 486                    # Gaming Keyboards
    python tools/query-category.py 486 --stock            # Include stock check (slower)
    python tools/query-category.py 486 --stock --instock  # Only show in-stock products

Compared to fetch-category.ps1:
- Faster (lighter, no brand lookup, no full export)
- Designed for real-time customer queries, not GEO file writing
- Supports --instock flag to filter out OOS products
"""

import json
import sys
import os
import time
import urllib.request
import urllib.error

# === Config ===
STORE = "ms4wz8cgi2"
TOKEN = "iedxfd72bgz2h46qz2pyc7ghsllrw01"
BASE = f"https://api.bigcommerce.com/stores/{STORE}/v3"
HEADERS = {
    "X-Auth-Token": TOKEN,
    "Accept": "application/json",
}

# === Args ===
do_stock = "--stock" in sys.argv or len(sys.argv) > 2  # auto-enable if --instock
do_instock_only = "--instock" in sys.argv
do_summary = "--summary" in sys.argv

# Get category ID
cat_ids = [a for a in sys.argv[1:] if a.isdigit()]
if not cat_ids:
    print("Usage: python tools/query-category.py <category_id> [--stock] [--instock] [--summary]")
    print("       --stock     check real stock via custom-fields (slower but accurate)")
    print("       --instock   only show products with stock > 0 (implies --stock)")
    print("       --summary   show brand overview instead of individual products")
    sys.exit(1)

CAT_ID = int(cat_ids[0])


def api_get(path):
    """GET request to BC API with retry."""
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


def get_brands():
    """Fetch brand list and return {id: name} mapping (handles pagination)."""
    mapping = {}
    page = 1
    while True:
        result = api_get(f"/catalog/brands?limit=250&page={page}")
        if not result or "data" not in result or not result["data"]:
            break
        for b in result["data"]:
            mapping[b["id"]] = b["name"]
        meta = result.get("meta", {}).get("pagination", {})
        if page >= meta.get("total_pages", 1):
            break
        page += 1
    return mapping


def get_stock(product_id):
    """Fetch OH stock only. Only Onehunga stock = customer-available.
    WL/SL/SU are internal — customers cannot receive those units."""
    result = api_get(f"/catalog/products/{product_id}/custom-fields")
    if not result or "data" not in result:
        return {"oh": 0, "total": 0}

    oh = 0
    for cf in result["data"]:
        if "Onehunga" in cf["name"]:
            try:
                oh = int(cf["value"])
            except (ValueError, TypeError):
                oh = 0
            break

    return {"oh": oh, "total": oh}


def stock_label(s):
    """Stock label based on OH (Onehunga) only — customer-available units."""
    t = s["total"]
    if t == 0:
        return "❌ Out of stock"
    elif t <= 3:
        return "⚠️ Only a few left"
    else:
        return "✅ In stock"


# === Main ===
print(f"\n=== Category {CAT_ID} — Query ===")
print()

# Fetch all pages
all_products = []
page = 1
while True:
    path = f"/catalog/products?categories:in={CAT_ID}&limit=250&page={page}&include_fields=id,name,sku,price,brand_id,custom_url,availability,is_visible"
    result = api_get(path)
    if not result or not result.get("data"):
        break
    all_products.extend(result["data"])
    meta = result.get("meta", {}).get("pagination", {})
    total_pages = meta.get("total_pages", 1)
    if page >= total_pages:
        break
    page += 1

if not all_products:
    print("  No products found in this category.")
    sys.exit(0)

print(f"  Total products: {len(all_products)}")

# Filter: only available + visible
available = [p for p in all_products if p.get("availability") == "available" and p.get("is_visible", True)]
hidden_count = len(all_products) - len(available)
if hidden_count > 0:
    print(f"  (skipped {hidden_count} disabled/hidden)")

# Fetch brand mapping
print("  Loading brands...", end="", file=sys.stderr)
brands = get_brands()
print(f" {len(brands)} brands cached", file=sys.stderr)

# Stock check (if requested)
if do_stock or do_instock_only:
    print(f"  Checking stock for {len(available)} products...")
    print()
    results = []
    for i, p in enumerate(available):
        stock = get_stock(p["id"])
        label = stock_label(stock)
        price = round(p["price"] * 1.15)
        url = "https://www.extremepc.co.nz" + p["custom_url"]["url"]
        results.append((stock["total"], p, stock, label, price, url))

        # Show progress for large categories
        if (i + 1) % 20 == 0:
            print(f"    ...checked {i+1}/{len(available)}", end="\r", file=sys.stderr)

    # Sort by stock (in stock first)
    results.sort(key=lambda r: r[0], reverse=True)

    # Filter in-stock only
    if do_instock_only:
        results = [r for r in results if r[0] > 0]

    print()

    # --summary mode: show brand overview
    if do_summary:
        from collections import Counter
        brand_counts = Counter()
        brand_prices = {}
        for total, p, stock, label, price, url in results:
            bname = brands.get(p.get("brand_id"), "Unknown")
            brand_counts[bname] += 1
            if bname not in brand_prices:
                brand_prices[bname] = {"min": price, "max": price}
            else:
                brand_prices[bname]["min"] = min(brand_prices[bname]["min"], price)
                brand_prices[bname]["max"] = max(brand_prices[bname]["max"], price)

        # Sort by count descending
        print(f"  📊 In-stock by brand ({len(results)} products):")
        print()
        for bname, cnt in brand_counts.most_common():
            p = brand_prices[bname]
            print(f"    {bname:20s}  {cnt:2d} products  (${p['min']} ~ ${p['max']})")
        print()
        print(f"  Use --stock --instock to see individual products.")
        sys.exit(0)

    for total, p, stock, label, price, url in results:
        brand = brands.get(p.get("brand_id"), "")
        brand_tag = f" [{brand}]" if brand else ""
        s = stock
        stock_detail = f"[OH={s['oh']}]" if do_stock and not do_instock_only else ""
        print(f"  {label}{brand_tag}  ${price}  {p['name'][:55]}")
        if stock_detail:
            print(f"           {stock_detail}")
        print(f"           SKU: {p['sku']} | {url}")
        print()

else:
    # No stock check — just list with price
    print()
    for p in available[:20]:
        brand = brands.get(p.get("brand_id"), "")
        brand_tag = f" [{brand}]" if brand else ""
        price = round(p["price"] * 1.15)
        url = "https://www.extremepc.co.nz" + p["custom_url"]["url"]
        print(f" ${price}{brand_tag}   {p['name'][:55]}")
        print(f"           SKU: {p['sku']} | {url}")
        print()

    if len(available) > 20:
        print(f"  ...and {len(available) - 20} more. Use --stock --instock to see all with stock info.")

print(f"  ────\n  {len(results) if (do_stock or do_instock_only) else len(available)} products shown")
