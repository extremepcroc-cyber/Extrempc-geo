#!/usr/bin/env python3
"""coverage-report.py — GEO coverage per category vs live BC in-stock counts.

Answers "what still needs writing?" without anyone querying BC by hand.

Usage:
    python tools/coverage-report.py                 # print table
    python tools/coverage-report.py --write         # also write tools/geo-coverage.md
    python tools/coverage-report.py --category monitors

STOCK DEFINITION — must match the rest of the repo: **OH (Onehunga) > 0**.
audit-geo.py is explicit that WL/SL/SU are internal and never customer-available,
so BC's `availability=available` is the WRONG basis here (it counts
supplier-channel stock and overstates coverage badly). Products are fetched with
`include=custom_fields` and counted on the Onehunga custom field, exactly as
tools/query-category.py does.

Counts are LIVE, so this does not trust bc_categories_index.json — that file's
IDs have been found to disagree with the live store (see notes in the output).
"""
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request

REPO = pathlib.Path(__file__).resolve().parent.parent
OUT = REPO / "tools" / "geo-coverage.md"

# dir, label, [ids], priority, note, mode
#   mode="single" -> instock = count(ids[0]); other ids listed for reference
#   mode="sum"    -> instock = sum of all ids (use when SKUs live in subcategories)
CATS = [
    ("gaming-pcs",           "Gaming PCs",          ["120", "1373"],               "P0", "sells by config combo — cover main/flagship only, not all SKUs", "single"),
    ("gaming-mice",          "Gaming Mice",         ["513", "1949"],               "P0", "", "single"),
    ("monitors",             "Monitors",            ["519"],                       "P0", "", "single"),
    ("video-cards",          "Video Cards",         ["426", "1426"],               "P1", "", "single"),
    ("gaming-keyboards",     "Gaming Keyboards",    ["486"],                       "P1", "DONE 2026-09-15 — 69/69 written", "single"),
    ("gaming-headsets",      "Gaming Headsets",     ["484", "476"],                "P1", "docs say 476; live id is 484 (476 = Over Ear Headphones)", "single"),
    ("cpu-processors",       "CPU / Processors",    ["364", "1430"],               "P2", "", "single"),
    ("memory-ram",           "Memory / RAM",        ["395"],                       "P2", "", "single"),
    ("internal-ssd",         "Internal SSD",        ["375"],                       "P2", "", "single"),
    ("internal-hard-drives", "Internal HDD",        ["369"],                       "P2", "", "single"),
    ("cooling",              "Cooling",             ["351", "349", "347", "348", "363", "346"], "P3",
     "SKUs sit in subcategories, so this row SUMS the leaves; 349 (CPU Coolers) sits under 346 (Air Cooling), so if a product is assigned to both there is slight double-counting", "sum"),
    ("power-supplies",       "Power Supplies",      ["410"],                       "P3", "", "single"),
    ("computer-cases",       "Computer Cases",      ["336"],                       "P3", "", "single"),
    ("gaming-chairs",        "Gaming Chairs",       ["244"],                       "P3", "LiberNovo — golden-standard set", "single"),
    ("webcams",              "Webcams",             ["230"],                       "P3", "", "single"),
    ("microphones",          "Microphones",         ["229"],                       "P3", "", "single"),
]

_env = [pathlib.Path(os.environ.get("HERMES_PROFILE_DIR", "")) / "extremepc.env",
        pathlib.Path.home() / "AppData/Local/hermes/profiles/exie/extremepc.env",
        REPO / ".env"]
for p in _env:
    if p.exists():
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

STORE = os.environ.get("BC_STORE_HASH", "")
TOKEN = os.environ.get("BC_ACCESS_TOKEN", "")
if not STORE or not TOKEN:
    sys.exit("Error: BC_STORE_HASH / BC_ACCESS_TOKEN not set.")
BASE = f"https://api.bigcommerce.com/stores/{STORE}/v3"
HEAD = {"X-Auth-Token": TOKEN, "Accept": "application/json"}


def _get(path, attempts=3):
    for i in range(attempts):
        try:
            import urllib.request as u
            req = u.Request(BASE + path, headers=HEAD, method="GET")
            with u.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < attempts - 1:
                time.sleep(2)
                continue
            return None
        except Exception:
            if i < attempts - 1:
                time.sleep(1)
                continue
            return None
    return None


def oh_stock(custom_fields):
    for cf in (custom_fields or []):
        if "Onehunga" in (cf.get("name") or ""):
            try:
                return int(cf.get("value"))
            except (TypeError, ValueError):
                return 0
    return 0


def count_oh_instock(cat_id):
    """Products in this category (node only, no rollup) with OH > 0."""
    total, page = 0, 1
    while True:
        d = _get(f"/catalog/products?categories:in={cat_id}"
                 f"&is_visible=true&include_fields=id&include=custom_fields"
                 f"&limit=250&page={page}")
        if not d or not d.get("data"):
            break
        total += sum(1 for p in d["data"] if oh_stock(p.get("custom_fields")) > 0)
        if page >= d.get("meta", {}).get("pagination", {}).get("total_pages", 1):
            break
        page += 1
    return total


def local_count(d):
    p = REPO / d
    return len(list(p.glob("*.md"))) if p.exists() else 0


def main():
    only = sys.argv[sys.argv.index("--category") + 1] if "--category" in sys.argv else None
    rows, today = [], time.strftime("%Y-%m-%d")

    for d, label, ids, prio, note, mode in CATS:
        if only and d != only:
            continue
        counts = {c: count_oh_instock(c) for c in ids}
        instock = sum(counts.values()) if mode == "sum" else counts.get(ids[0], 0)
        have = local_count(d)
        rows.append(dict(dir=d, label=label, ids=ids, counts=counts, mode=mode,
                         instock=instock, have=have, gap=max(instock - have, 0),
                         prio=prio, note=note))

    w = max((len(r["label"]) for r in rows), default=10)
    print(f"{'category':<{w}}  {'prio':<4} {'OH>0':>6} {'files':>5} {'gap':>5}  ids")
    for r in rows:
        ids = ", ".join(f"{c}={n}" for c, n in r["counts"].items())
        print(f"{r['label']:<{w}}  {r['prio']:<4} {r['instock']:>6} {r['have']:>5} "
              f"{r['gap']:>5}  {ids}")

    if "--write" in sys.argv:
        L = [
            "# GEO Coverage — category vs live BC Onehunga stock",
            "",
            f"> Auto-generated by `tools/coverage-report.py` · last run **{today}**",
            "> Refresh: `python tools/coverage-report.py --write`",
            "",
            "**This file answers \"what still needs writing?\"** — regenerate it rather",
            "than querying BC by hand per category.",
            "",
            "**Stock basis: OH (Onehunga) > 0**, matching `audit-geo.py` — WL/SL/SU are",
            "internal and never customer-available, so BC's `availability=available` must",
            "NOT be used here (it counts supplier-channel stock and overstates coverage).",
            "",
            "Counts are live per category node; BC's `categories:in` does not roll up",
            "subcategories. `gap` = OH>0 SKUs with no GEO file, floored at 0.",
            "",
            "| category | dir | prio | OH>0 | files | gap | ids checked |",
            "|---|---|:---:|---:|---:|---:|---|",
        ]
        for r in rows:
            ids = ", ".join(f"{c}={n}" for c, n in r["counts"].items())
            L.append(f"| {r['label']} | `{r['dir']}/` | {r['prio']} | {r['instock']} | "
                     f"{r['have']} | {r['gap']} | {ids} |")
        L += ["", "## Notes", ""]
        for r in rows:
            if r["note"]:
                L.append(f"- **{r['label']}** — {r['note']}")
        L += [
            "",
            "## Category-ID problems found (verify before trusting the docs)",
            "",
            "- **Gaming Headsets**: `CLAUDE.md` / `README.md` say `476`; the live id is",
            "  `484`. `476` is *Over Ear Headphones* — a different product set entirely.",
            "- The secondary IDs in the docs (`1373` PCs, `1426` Video Cards, `1430` CPU,",
            "  `1949` Mice) do return live categories, but at counts near-identical to the",
            "  primary id — they look like mirror/duplicate category nodes. Check the `ids`",
            "  column: when a secondary matches the primary, do not sum them.",
            "",
            "## Update protocol",
            "",
            "1. `python tools/coverage-report.py --write` to refresh",
            "2. One leaf subcategory per batch, 4–5 SKUs at a time",
            "3. Commit the GEO files, then refresh this table",
            "4. Never hand-edit counts — regenerate",
        ]
        OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
        print(f"\nwrote {OUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
