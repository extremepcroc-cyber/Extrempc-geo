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
import collections
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
    ("gaming-mice",          "Gaming Mice",         ["513", "1949"],               "P0",
     "UNVERIFIED — 513 is itself a mid-level node with leaf children 1237 (Wired)/1238 (Wireless); "
     "raw product count under 513 alone is 144 but the two leaves sum to 187, so 513 may not roll up "
     "its own children either. Do not trust this row's gap until re-verified like cooling/CPU were.", "single"),
    ("monitors",             "Monitors",            ["519"],                       "P0",
     "UNVERIFIED — 519 has 6 leaf children (532/533/531/538/536/534) summing to 326 raw products vs "
     "165 directly under 519. Same parent-undercount pattern as CPU/RAM/SSD/HDD/PSU/Cases had — likely "
     "needs mode=\"sum\" over the leaves, not confirmed yet.", "single"),
    ("video-cards",          "Video Cards",         ["426", "1426"],               "P1",
     "UNVERIFIED — 426's own children (429 Nvidia/427 AMD/2038 Intel) sum higher, and 429 itself has "
     "further children (430/1018/1325 = RTX 30/40/50). Do not naively sum parent+children here, it will "
     "double-count — needs the deepest-leaf IDs only, not checked yet.", "single"),
    ("gaming-keyboards",     "Gaming Keyboards",    ["486"],                       "P1", "DONE 2026-09-15 — 69/69 written, but ~52/68 have wrong prices vs BC, see audit-geo.py output before trusting this as \"done\"", "single"),
    ("gaming-headsets",      "Gaming Headsets",     ["484", "476"],                "P1", "docs say 476; live id is 484 (476 = Over Ear Headphones)", "single"),
    ("cpu-processors",       "CPU / Processors",    ["757", "758"],                "P2",
     "Fixed 2026-09-15: parent 364 only has 11 products directly on it; almost everything sits on leaf "
     "757 (AMD Desktop CPUs, 39) / 758 (Intel Desktop CPUs, 52). Switched to sum-of-leaves.", "sum"),
    ("memory-ram",           "Memory / RAM",        ["1023", "1024", "1025", "1308", "1026",
                                                      "1027", "1028", "1029", "1216", "1217", "1322"], "P2",
     "Fixed 2026-09-15: parent 395 only has 4 direct products; real SKUs sit on the deepest leaves — "
     "Desktop RAM by size (1023-1026,1308), Laptop RAM by size (1027-1029,1216,1217), Server RAM (1322).", "sum"),
    ("internal-ssd",         "Internal SSD",        ["376", "380"],                "P2",
     "Fixed 2026-09-15: parent 375 only has 4 direct products; leaves 376 (M.2 NVMe, 26) + 380 (SATA, 2) "
     "hold the real count.", "sum"),
    ("internal-hard-drives", "Internal HDD",        ["371", "372", "373", "370"],  "P2",
     "Fixed 2026-09-15: parent 369 undercounts; leaves are 371 (1-4TB) / 372 (6-10TB) / 373 (12-20TB) / "
     "370 (22TB+).", "sum"),
    ("cooling",              "Cooling",             ["351", "349", "347", "348", "363", "346"], "P3",
     "SKUs sit in subcategories, so this row SUMS the leaves; 349 (CPU Coolers) sits under 346 (Air Cooling), so if a product is assigned to both there is slight double-counting", "sum"),
    ("power-supplies",       "Power Supplies",      ["411", "412", "413", "414", "415", "416", "1319"], "P3",
     "Fixed 2026-09-15: parent 410 has 30 direct products but its 7 leaves (by wattage band + Server PSU) "
     "sum to 74 — switched to sum-of-leaves.", "sum"),
    ("computer-cases",       "Computer Cases",      ["340", "338", "339", "337", "342"], "P3",
     "Fixed 2026-09-15: parent 336 has 25 direct products but its 5 leaves (by form factor + Server) sum "
     "to 110 — switched to sum-of-leaves.", "sum"),
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


# Same sliding-window throttle as tools/audit-geo.py — BC's cap is 150
# requests/30s per store token, shared across whatever else is hitting the
# API at the same time (EVA, other tools), so stay well under it.
_RATE_LIMIT, _RATE_WINDOW_SEC, _SAFETY_MARGIN = 150, 30, 20
_call_times = collections.deque()


def _throttle():
    now = time.monotonic()
    while _call_times and now - _call_times[0] > _RATE_WINDOW_SEC:
        _call_times.popleft()
    if len(_call_times) >= (_RATE_LIMIT - _SAFETY_MARGIN):
        sleep_for = _RATE_WINDOW_SEC - (now - _call_times[0]) + 0.5
        if sleep_for > 0:
            print(f"  [rate limit] pacing - sleeping {sleep_for:.1f}s", file=sys.stderr)
            time.sleep(sleep_for)
    _call_times.append(time.monotonic())


def _get(path, attempts=3):
    for i in range(attempts):
        _throttle()
        try:
            req = urllib.request.Request(BASE + path, headers=HEAD, method="GET")
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < attempts - 1:
                time.sleep(5)
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


# Non-product files that legitimately live in a category directory but are
# not GEO product files — must be excluded or coverage counts are inflated.
_NON_PRODUCT_FILES = {"README.md", "TEMPLATE.md", "PROGRESS.md", "QUEUE.md",
                       "TODO.md", "CLAUDE.md", "categories-tree.md"}


def local_count(d):
    """
    Count only files that look like real SKU-named GEO files.
    Filename must be ALL CAPS (CLAUDE.md's naming rule: filename = BC SKU,
    ALL CAPS) — this excludes known tracker files (PROGRESS.md, QUEUE.md)
    *and* any stray slug-named file (e.g. "enshrouded-gaming-pc.md") without
    needing to hardcode every bad filename in the repo.
    """
    p = REPO / d
    if not p.exists():
        return 0
    count = 0
    for f in p.glob("*.md"):
        if f.name in _NON_PRODUCT_FILES:
            continue
        if f.stem != f.stem.upper():
            continue
        count += 1
    return count


def main():
    only = None
    if "--category" in sys.argv:
        idx = sys.argv.index("--category")
        if idx + 1 >= len(sys.argv):
            sys.exit("Error: --category requires a value, e.g. --category monitors")
        only = sys.argv[idx + 1]
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
            "- **Parent-category undercounting** (found + fixed 2026-09-15 for CPU, Memory,",
            "  Internal SSD, Internal HDD, Power Supplies, Computer Cases): BC's storefront",
            "  categorizer puts most real products on the *leaf* subcategory, not the parent",
            "  node these rows used to query. Example: CPU parent `364` had only 11 products",
            "  directly on it while its two leaves (`757` AMD, `758` Intel) held 91 combined —",
            "  querying the parent alone silently reported ~9x too few in-stock SKUs. All six",
            "  rows above were switched to `mode=\"sum\"` over their real leaf IDs.",
            "- **Gaming Mice, Monitors, Video Cards are NOT yet verified for this same bug** —",
            "  quick checks during the 2026-09-15 fix found the same parent/leaf mismatch",
            "  pattern (e.g. Monitors parent `519` = 165 raw products vs its 6 leaves summing",
            "  to 326), but Video Cards' tree goes an extra level deep (429 Nvidia → 430/1018/",
            "  1325 RTX 30/40/50) where naively summing parent+children double-counts. These",
            "  three rows are left on the old (likely wrong) IDs — do not trust their `gap`",
            "  numbers until someone walks the tree properly like CPU/Memory/SSD/HDD/PSU/Cases",
            "  were.",
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
