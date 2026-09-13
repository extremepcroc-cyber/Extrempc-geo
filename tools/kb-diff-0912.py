#!/usr/bin/env python3
"""Diff EVAcache 2026-09-11 vs 2026-09-12 and cross-reference KB files."""
import json
from pathlib import Path

root = Path.home() / "AppData/Local/hermes/profiles/exie-web/workspace/EVAcache"
old = json.loads((root / "2026-09-11/by-sku.json").read_text())
new = json.loads((root / "2026-09-12/by-sku.json").read_text())

print("old:", len(old), "new:", len(new))

added = sorted(set(new) - set(old))
removed = sorted(set(old) - set(new))

def pinfo(p):
    return (f"{p.get('sku')} | {p.get('name','')[:70]} | "
            f"list={p.get('price')} calc={p.get('calculated_price')} "
            f"inv={p.get('inventory_level')} oh={p.get('oh_stock')} "
            f"sale={p.get('on_sale', p.get('calculated_price') != p.get('price'))}")

print("\n=== ADDED (%d) ===" % len(added))
for s in added:
    print("  +" + pinfo(new[s]))

print("\n=== REMOVED (%d) ===" % len(removed))
for s in removed:
    print("  -" + pinfo(old[s]))

# Price / stock changes for overlapping SKUs
print("\n=== CHANGED (calc_price or oh_stock) ===")
n = 0
for s in sorted(set(old) & set(new)):
    o, nw = old[s], new[s]
    changes = []
    if o.get("calculated_price") != nw.get("calculated_price"):
        changes.append(f"calc {o.get('calculated_price')}->{nw.get('calculated_price')}")
    if o.get("oh_stock") != nw.get("oh_stock"):
        changes.append(f"oh {o.get('oh_stock')}->{nw.get('oh_stock')}")
    if o.get("price") != nw.get("price"):
        changes.append(f"list {o.get('price')}->{nw.get('price')}")
    if changes:
        n += 1
        print(f"  * {s} | {nw.get('name','')[:60]} | " + ", ".join(changes))
print(f"({n} changed)")
