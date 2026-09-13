import json, os

base = os.path.expanduser("~/AppData/Local/hermes/profiles/exie-web/workspace/EVAcache")

def load(date):
    d = json.load(open(os.path.join(base, date, "products.json")))
    return {p["sku"]: p for p in d["products"]}

old = load("2026-09-10")
new = load("2026-09-11")

old_skus = set(old.keys())
new_skus = set(new.keys())
added = new_skus - old_skus
removed = old_skus - new_skus
common = old_skus & new_skus

print(f"09-10: {len(old)} in-stock | 09-11: {len(new)} in-stock")
print(f"ADDED: {len(added)} | REMOVED: {len(removed)} | COMMON: {len(common)}")
print()

def show(sku, src, tag):
    p = src[sku]
    print(f"  [{tag}] {sku} | {p['name'][:75]} | {p['brand']} | ${p['price_nzd_inc_gst']} (list ${p['list_price_nzd_inc_gst']}, sale={p['on_sale']}) | OH={p['oh_stock']}")

print("=== ADDED (new in 09-11) ===")
for s in sorted(added):
    show(s, new, "ADD")
print()
print("=== REMOVED (gone from 09-11) ===")
for s in sorted(removed):
    show(s, old, "REM")
print()

# price / stock changes on common
print("=== COMMON: price changes (price_nzd_inc_gst differs) ===")
for s in sorted(common):
    if old[s]["price_nzd_inc_gst"] != new[s]["price_nzd_inc_gst"] or old[s]["on_sale"] != new[s]["on_sale"]:
        print(f"  {s} | {new[s]['name'][:60]} | {old[s]['price_nzd_inc_gst']} (sale={old[s]['on_sale']}) -> {new[s]['price_nzd_inc_gst']} (sale={new[s]['on_sale']}) | OH={new[s]['oh_stock']}")
print()
print("=== COMMON: stock (OH) changes ===")
for s in sorted(common):
    if old[s]["oh_stock"] != new[s]["oh_stock"]:
        print(f"  {s} | {new[s]['name'][:60]} | OH {old[s]['oh_stock']} -> {new[s]['oh_stock']}")
