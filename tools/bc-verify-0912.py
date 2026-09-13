#!/usr/bin/env python3
"""BC API verification for 2026-09-12 KB backfill run (per-SKU, proven pattern)."""
import json, os
import urllib.request, urllib.parse
from pathlib import Path

_env = Path.home() / "AppData/Local/hermes/profiles/exie/extremepc.env"
with open(_env) as _f:
    for _line in _f:
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

STORE = os.environ.get("BC_STORE_HASH")
TOKEN = os.environ.get("BC_ACCESS_TOKEN")
BASE = f"https://api.bigcommerce.com/stores/{STORE}/v3"
HEADERS = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

def get(path):
    req = urllib.request.Request(BASE + path, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

def get_raw(path):
    """Return (status, body) without raising."""
    req = urllib.request.Request(BASE + path, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:400]

skus = [
    "MONACEX32X3", "MONACEX32X5",
    "HDSMCHX9PB", "MOSATKA9UB", "MOSRAZV4PB", "RAMGSKM5360RB", "KEYAULH68HBM",
    "KEYAULH68HWS", "CASJONZ20WP", "COOJONCR1000EB", "MONACEPD163Q",
    "RAMPNYX16D43", "RAMPNYX32D43", "XPC13811", "XPC1381",
]
for sku in skus:
    q = f"/catalog/products?sku={urllib.parse.quote(sku)}&include=custom_fields&limit=1"
    status, body = get_raw(q)
    if status != 200:
        print(f"== {sku} -> HTTP {status}: {body[:200]}")
        continue
    data = json.loads(body)
    prods = data.get("data", [])
    if not prods:
        print(f"== {sku} -> EMPTY (delisted)")
        continue
    p = prods[0]
    cf = p.get("custom_fields") or []
    oh = None
    for c in cf:
        lab = (c.get("code", "") + " " + c.get("name", "")).lower()
        if "onehunga" in lab or "oh stock" in lab or c.get("code", "").lower() in ("oh", "oh_stock"):
            v = c.get("value")
            oh = v.get("value") if isinstance(v, dict) else v
    calc = p.get("calculated_price")
    price = p.get("price")
    print(f"== {sku} | id={p['id']} | {p['name'][:70]}")
    print(f"   ex list={price} calc={calc} -> inc list={round((price or 0)*1.15,2)} calc={round((calc or 0)*1.15,2)}")
    print(f"   inv={p.get('inventory_level')} oh={oh} visible={p.get('is_visible')}")
    print(f"   url={(p.get('custom_url') or {}).get('url')}")
    if oh is None:
        print("   CF_RAW:", json.dumps(cf)[:300])
