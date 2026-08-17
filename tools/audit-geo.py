#!/usr/bin/env python3
"""
audit-geo.py — Audit GEO markdown files against BC API. Auto-applies changes.

Usage:
    python tools/audit-geo.py                          # full audit + auto-apply
    python tools/audit-geo.py --dry-run                # report only, no file writes
    python tools/audit-geo.py --category power-supplies  # single category dir
    python tools/audit-geo.py --dry-run --category monitors

What it checks:
    - Price: GEO **Price:** vs BC API price × 1.15 (NZD inc GST)
    - Stock: OH (Onehunga) only — WL/SL/SU are internal, never customer-available
    - URL: GEO **URL:** vs BC API custom_url.url

What it auto-applies (unless --dry-run):
    - Price change → updates **Price:** line and Schema "price" field
    - OH = 0 → inserts **Status:** OUT OF STOCK line, sets Schema to OutOfStock
    - OH > 0 and file already flagged OOS → removes Status line, sets Schema to InStock
    - URL changed → updates **URL:** line

API efficiency:
    - Batch fetch with sku:in=... + include=custom_fields (inline, no per-product calls)
    - ~3 API calls for 200 SKUs (vs 400 in the PowerShell version)

Output: tools/change-report.json
"""

import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

# ── Credentials ──────────────────────────────────────────────────────────────

_env_candidates = [
    pathlib.Path(os.environ.get("HERMES_PROFILE_DIR", "")) / "extremepc.env",
    pathlib.Path.home() / "AppData/Local/hermes/profiles/exie/extremepc.env",
    pathlib.Path(__file__).parent.parent / ".env",
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
    sys.exit("Error: BC_ACCESS_TOKEN not set. Add it to extremepc.env")

BASE    = f"https://api.bigcommerce.com/stores/{STORE}/v3"
HEADERS = {"X-Auth-Token": TOKEN, "Accept": "application/json"}

# ── Args ──────────────────────────────────────────────────────────────────────

DRY_RUN      = "--dry-run" in sys.argv
CATEGORY_DIR = None
for i, arg in enumerate(sys.argv[1:], 1):
    if arg == "--category" and i < len(sys.argv):
        CATEGORY_DIR = sys.argv[i + 1]
        break

GEO_ROOT    = pathlib.Path(__file__).parent.parent
REPORT_OUT  = pathlib.Path(__file__).parent / "change-report.json"
TODAY       = date.today().isoformat()

SKIP_DIRS  = {"brands", "product-knowledge", "tools", "blog"}
SKIP_FILES = {"README.md", "TEMPLATE.md", "CLAUDE.md", "PROGRESS.md", "todo.md",
              "categories-tree.md", "内容选题清单.md"}

# ── API helpers ───────────────────────────────────────────────────────────────

def api_get(path: str) -> dict | None:
    url = f"{BASE}{path}"
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(3)
                continue
            print(f"  [API {e.code}] {url}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"  [Error] {e}", file=sys.stderr)
            return None
    return None


def fetch_products_by_skus(skus: list[str]) -> dict[str, dict]:
    """
    Batch-fetch products by SKU list.
    Uses include=custom_fields so stock is inline — no per-product calls.
    Returns dict keyed by SKU (uppercase).
    BC limit: 250 per page, 600 SKUs per sku:in query.
    """
    result = {}
    chunk_size = 200  # stay well under 600-char URL limit per chunk

    for i in range(0, len(skus), chunk_size):
        chunk = skus[i:i + chunk_size]
        sku_param = ",".join(urllib.parse.quote(s) for s in chunk)
        page = 1
        while True:
            path = (
                f"/catalog/products"
                f"?sku:in={sku_param}"
                f"&include_fields=id,name,sku,price,custom_url"
                f"&include=custom_fields"
                f"&limit=250&page={page}"
            )
            data = api_get(path)
            if not data or not data.get("data"):
                break
            for p in data["data"]:
                result[p["sku"].upper()] = p
            pagination = data.get("meta", {}).get("pagination", {})
            if page >= pagination.get("total_pages", 1):
                break
            page += 1

    return result


# ── GEO file parser ───────────────────────────────────────────────────────────

_RE_SKU   = re.compile(r"\*\*SKU:\*\*\s+([A-Z0-9\-]+)")
_RE_PRICE = re.compile(r"\*\*Price:\*\*\s+\$([0-9,]+(?:\.[0-9]{1,2})?)")
_RE_URL   = re.compile(r"\*\*URL:\*\*\s+(https?://\S+)")
_RE_TOMB  = re.compile(r"\*\*Status:\*\*\s+TOMBSTONE")
_RE_OOS   = re.compile(r"\*\*Status:\*\*\s+OUT OF STOCK")


def parse_geo(path: pathlib.Path) -> dict:
    text = path.read_text(encoding="utf-8")
    sku_m   = _RE_SKU.search(text)
    price_m = _RE_PRICE.search(text)
    url_m   = _RE_URL.search(text)
    return {
        "path":      path,
        "text":      text,
        "sku":       sku_m.group(1).strip() if sku_m else None,
        "price_nzd": float(price_m.group(1).replace(",", "")) if price_m else None,
        "url":       url_m.group(1).strip() if url_m else None,
        "tombstone": bool(_RE_TOMB.search(text)),
        "already_oos": bool(_RE_OOS.search(text)),
    }


# ── Stock helper ──────────────────────────────────────────────────────────────

def get_oh(custom_fields: list) -> int:
    for cf in (custom_fields or []):
        if "Onehunga" in cf.get("name", ""):
            try:
                return int(cf["value"])
            except (ValueError, TypeError):
                return 0
    return 0


# ── Auto-apply helpers ────────────────────────────────────────────────────────

def _apply_price(text: str, new_price: float) -> str:
    """Update **Price:** line and Schema "price" field."""
    formatted = f"{new_price:,.2f}"
    # **Price:** field
    text = re.sub(
        r'(\*\*Price:\*\*\s+)\$[0-9,]+(?:\.[0-9]{1,2})?',
        rf'\g<1>${formatted}',
        text,
    )
    # Schema "price": "..."
    text = re.sub(
        r'("price":\s*")[0-9,]+(?:\.[0-9]{1,2})?(")',
        rf'\g<1>{new_price:.2f}\g<2>',
        text,
    )
    return text


def _apply_oos(text: str) -> str:
    """Insert OUT OF STOCK status line after URL line. Update Schema availability."""
    status_line = f"**Status:** OUT OF STOCK — last checked {TODAY}"
    # Remove any existing Status line first (avoid duplicates)
    text = re.sub(r"\*\*Status:\*\*\s+OUT OF STOCK[^\n]*\n", "", text)
    # Insert after **URL:** line
    text = re.sub(
        r"(\*\*URL:\*\*\s+https?://\S+\n)",
        rf"\1{status_line}\n",
        text,
    )
    # Schema availability
    text = re.sub(
        r'"availability":\s*"https://schema\.org/InStock"',
        '"availability": "https://schema.org/OutOfStock"',
        text,
    )
    return text


def _apply_back_in_stock(text: str) -> str:
    """Remove OOS Status line. Restore Schema to InStock."""
    text = re.sub(r"\*\*Status:\*\*\s+OUT OF STOCK[^\n]*\n", "", text)
    text = re.sub(
        r'"availability":\s*"https://schema\.org/OutOfStock"',
        '"availability": "https://schema.org/InStock"',
        text,
    )
    return text


def _apply_url(text: str, new_url: str) -> str:
    """Update **URL:** line."""
    return re.sub(
        r"(\*\*URL:\*\*\s+)https?://\S+",
        rf"\g<1>{new_url}",
        text,
    )


# ── Scan GEO files ────────────────────────────────────────────────────────────

search_root = GEO_ROOT / CATEGORY_DIR if CATEGORY_DIR else GEO_ROOT

md_files = [
    p for p in search_root.rglob("*.md")
    if not (SKIP_DIRS & set(p.relative_to(GEO_ROOT).parts))
    and p.name not in SKIP_FILES
]

print(f"\n=== ExtremePC GEO Audit {'(DRY RUN) ' if DRY_RUN else ''}===")
print(f"Root  : {GEO_ROOT}")
if CATEGORY_DIR:
    print(f"Filter: {CATEGORY_DIR}")
print(f"Files : {len(md_files)} markdown files found\n")

# Parse all GEO files
geo_records = []
skipped = 0
for f in md_files:
    geo = parse_geo(f)
    if not geo["sku"] or geo["tombstone"]:
        skipped += 1
        continue
    geo_records.append(geo)

print(f"Parsed : {len(geo_records)} files with valid SKU")
print(f"Skipped: {skipped} (tombstones / no SKU)\n")

# ── Batch fetch from BC ───────────────────────────────────────────────────────

all_skus = [g["sku"] for g in geo_records]
print(f"Fetching {len(all_skus)} SKUs from BC API (batched)...", end="", flush=True)
bc_by_sku = fetch_products_by_skus(all_skus)
print(f" done. {len(bc_by_sku)} matched.\n")

# ── Compare and report ────────────────────────────────────────────────────────

report   = []
changed  = []
errors   = []

for geo in geo_records:
    sku = geo["sku"]
    bc  = bc_by_sku.get(sku)

    if not bc:
        errors.append({"sku": sku, "file": str(geo["path"].relative_to(GEO_ROOT)), "error": "SKU not found in BC"})
        print(f"  [NOT FOUND] {sku}")
        continue

    bc_price_nzd = round(float(bc["price"]) * 1.15, 2)
    oh           = get_oh(bc.get("custom_fields", []))
    bc_url       = "https://www.extremepc.co.nz" + bc.get("custom_url", {}).get("url", "")

    geo_price = geo["price_nzd"]
    geo_url   = geo["url"] or ""

    price_changed = geo_price is not None and abs(bc_price_nzd - geo_price) > 0.05
    needs_oos     = oh == 0 and not geo["already_oos"]
    back_in_stock = oh > 0 and geo["already_oos"]
    url_changed   = (
        geo_url
        and bc_url
        and geo_url.rstrip("/") != bc_url.rstrip("/")
        and "TBC" not in geo_url
    )

    needs_update = price_changed or needs_oos or back_in_stock or url_changed

    entry = {
        "sku":           sku,
        "file":          str(geo["path"].relative_to(GEO_ROOT)),
        "bc_name":       bc["name"],
        "needs_update":  needs_update,
        "price_geo_nzd": geo_price,
        "price_bc_nzd":  bc_price_nzd,
        "price_changed": price_changed,
        "oh_stock":      oh,
        "needs_oos_flag":  needs_oos,
        "back_in_stock":   back_in_stock,
        "url_geo":       geo_url,
        "url_bc":        bc_url,
        "url_changed":   url_changed,
        "applied":       False,
        "apply_error":   None,
    }

    if not needs_update:
        tag, color = "OK", "\033[32m"
    elif needs_oos:
        tag, color = "OOS", "\033[31m"
    elif back_in_stock:
        tag, color = "BACK", "\033[36m"
    elif price_changed:
        tag, color = "PRICE", "\033[33m"
    else:
        tag, color = "URL", "\033[33m"

    reset = "\033[0m"
    print(f"  [{color}{tag}{reset}] {sku}", end="")
    if price_changed:
        print(f"  ${geo_price} → ${bc_price_nzd}", end="")
    if needs_oos:
        print(f"  OH=0 → OOS", end="")
    if back_in_stock:
        print(f"  OH={oh} → back in stock", end="")
    if url_changed:
        print(f"  URL changed", end="")
    print()

    report.append(entry)
    if needs_update:
        changed.append(entry)

# ── Auto-apply ────────────────────────────────────────────────────────────────

if changed and not DRY_RUN:
    print(f"\nApplying {len(changed)} changes...")
    for entry in changed:
        geo = next(g for g in geo_records if g["sku"] == entry["sku"])
        text = geo["text"]
        try:
            if entry["price_changed"]:
                text = _apply_price(text, entry["price_bc_nzd"])
            if entry["needs_oos_flag"]:
                text = _apply_oos(text)
            if entry["back_in_stock"]:
                text = _apply_back_in_stock(text)
            if entry["url_changed"]:
                text = _apply_url(text, entry["url_bc"])
            geo["path"].write_text(text, encoding="utf-8")
            entry["applied"] = True
            print(f"  ✓ {entry['sku']} — {geo['path'].relative_to(GEO_ROOT)}")
        except Exception as e:
            entry["apply_error"] = str(e)
            print(f"  ✗ {entry['sku']} — {e}", file=sys.stderr)
elif DRY_RUN and changed:
    print(f"\n[Dry run] {len(changed)} files would be updated — no changes written.")

# ── Summary ───────────────────────────────────────────────────────────────────

ok_count    = len([r for r in report if not r["needs_update"]])
oos_count   = len([r for r in report if r["needs_oos_flag"]])
back_count  = len([r for r in report if r["back_in_stock"]])
price_count = len([r for r in report if r["price_changed"]])
url_count   = len([r for r in report if r["url_changed"]])
applied     = len([r for r in report if r.get("applied")])

print(f"""
=== Summary ===
  Scanned  : {len(geo_records)}
  Skipped  : {skipped}
  OK       : {ok_count}
  Price Δ  : {price_count}
  OOS      : {oos_count}
  Back→Stock: {back_count}
  URL Δ    : {url_count}
  Errors   : {len(errors)}
  Applied  : {applied if not DRY_RUN else 'n/a (dry run)'}
""")

# ── Write report ──────────────────────────────────────────────────────────────

report_data = {
    "generated":  TODAY,
    "dry_run":    DRY_RUN,
    "geo_root":   str(GEO_ROOT),
    "summary": {
        "scanned":      len(geo_records),
        "ok":           ok_count,
        "price_changed": price_count,
        "needs_oos_flag": oos_count,
        "back_in_stock": back_count,
        "url_changed":  url_count,
        "errors":       len(errors),
        "applied":      applied,
    },
    "changes": [r for r in report if r["needs_update"] or r.get("apply_error")],
    "errors":   errors,
}

REPORT_OUT.write_text(json.dumps(report_data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Report: {REPORT_OUT}")
