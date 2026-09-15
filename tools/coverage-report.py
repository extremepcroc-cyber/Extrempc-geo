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
#   mode="sum"    -> instock = sum of separate per-id counts. ONLY safe when the
#                    ids are known not to overlap (verified case by case, e.g.
#                    Cooling's leaves, CPU/RAM/SSD/HDD/PSU/Cases parent-vs-leaf).
#   mode="dedup"  -> instock = one combined categories:in=id1,id2,... query.
#                    Use this whenever ids might overlap (a product in two
#                    leaves at once) or might be undercounted by leaves alone
#                    (some products only tagged at a parent/mid node) — safe
#                    regardless of which tree level products actually sit at.
#                    Slower (can't split into independent single-id calls) but
#                    always correct; prefer it unless you've specifically
#                    verified sum is equivalent and cheaper.
CATS = [
    ("gaming-pcs",           "Gaming PCs",          ["120", "1373"],               "P0", "sells by config combo — cover main/flagship only, not all SKUs", "single"),
    ("gaming-mice",          "Gaming Mice",         ["513", "1237", "1238"],       "P0",
     "Fixed 2026-09-15: verified 1237 (Wired) + 1238 (Wireless) overlap — some products are tagged to "
     "both leaves, so a naive sum overcounted (90) vs the real deduped total (80). Uses mode=\"dedup\": "
     "one combined query across parent+leaves, BC returns each product once regardless of overlap.", "dedup"),
    ("monitors",             "Monitors",            ["519", "532", "533", "531", "538", "536", "534"], "P0",
     "Fixed 2026-09-15: same overlap issue as Gaming Mice (e.g. an ultrawide gaming monitor can sit in "
     "both \"Gaming\" and \"Ultrawide\" leaves) — naive leaf-sum gave 46, real deduped total is 41. "
     "mode=\"dedup\".", "dedup"),
    ("video-cards",          "Video Cards",         ["426", "429", "430", "1018", "1325", "427", "2038"], "P1",
     "Fixed 2026-09-15: opposite problem from Mice/Monitors — some GPUs are tagged only at the parent "
     "(426) or mid-level (429 Nvidia) node, not any specific RTX-generation leaf, so deepest-leaves-only "
     "undercounted (58) vs the real deduped total (69) that includes every level. mode=\"dedup\".", "dedup"),
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


def count_oh_instock_multi(cat_ids):
    """
    Products with OH > 0 across an ENTIRE category subtree (parent + every
    descendant), counted with a single combined `categories:in=id1,id2,...`
    query rather than summing separate per-id calls.

    Why this exists: mode="sum" (separate calls, added together) is only
    correct when the ids don't overlap. Verified against Gaming Mice and
    Monitors that they DO overlap (a product can sit in two leaf
    subcategories at once, e.g. an ultrawide gaming monitor tagged to both
    "Gaming Monitors" and "Ultrawide Monitors" - naive sum double-counts
    it) and Video Cards has the opposite problem (some products are tagged
    only at the parent/mid-level node, not any specific leaf - naive
    leaves-only sum undercounts). `categories:in` is an OR filter and BC
    already returns each matching product once even when it satisfies
    several of the given ids, so one combined query sidesteps both
    failure modes at once, regardless of which tree level a product
    happens to be tagged at.
    """
    idstr = ",".join(cat_ids)
    total, page = 0, 1
    while True:
        d = _get(f"/catalog/products?categories:in={idstr}"
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
        if mode == "dedup":
            # One combined query across the whole subtree — see
            # count_oh_instock_multi() for why sum/single are unsafe here.
            instock = count_oh_instock_multi(ids)
            counts = {",".join(ids): instock}
        else:
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
            "- **Gaming Mice, Monitors, Video Cards** (fixed 2026-09-15, same day, second pass):",
            "  neither \"single\" nor \"sum\" was safe here. Mice/Monitors leaves *overlap* — a",
            "  product can sit in two leaves at once (e.g. an ultrawide gaming monitor in both",
            "  \"Gaming\" and \"Ultrawide\"), so naive sum overcounted (Monitors: 46 vs real 41).",
            "  Video Cards has the opposite problem — some GPUs are tagged only at the parent",
            "  or mid-level node (426 / 429 Nvidia), not any RTX-generation leaf, so summing",
            "  leaves alone undercounted (58 vs real 69). Verified by diffing actual SKU sets,",
            "  not just counts (see commit for methodology). All three now use `mode=\"dedup\"`",
            "  — one combined `categories:in=` query across the whole subtree, which BC",
            "  returns de-duplicated regardless of which level a product is tagged at.",
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
