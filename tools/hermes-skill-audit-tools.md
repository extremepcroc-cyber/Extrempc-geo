# Skill: ExtremePC GEO Audit & Coverage Tools

**Trigger:** Auditing existing GEO files against live BC data (price/stock/URL sync), or deciding what to write next based on real coverage gaps. Not needed for a straightforward "write these SKUs" writing task — see `tools/hermes-skill-geo-writing.md` for that.

---

## Price and Stock Audit (`tools/audit-geo.py`)

**Current tool — use this one.** `tools/audit-geo.ps1` still exists but is legacy/deprecated (2 API calls per SKU, 400+ calls for a full audit, no rate-limit protection, no backup mechanism, no URL-change detection). Do not use it for new work; kept only for reference.

**When to run:** before any batch editing session, or when the store manager reports prices have changed.

**What it checks:**
- **Price**: parses `**Price:**` from each `.md` file, fetches current BC price (×1.15 for GST), flags if difference > $0.05
- **Stock**: reads `__Stock Available Onehunga` (OH) from BC custom fields, fetched inline via `include=custom_fields` — no per-SKU extra call. Only OH = customer-available; WL/SL/SU are internal and ignored.
- **URL**: compares GEO `**URL:**` against BC's live `custom_url.url` — catches slug changes that would otherwise 404
- **OOS / back-in-stock**: flags `needs_oos_flag` when OH = 0, flags `back_in_stock` when OH > 0 but the file is still marked OOS
- **Tombstones**: automatically skipped — not checked
- **Not found in BC at all** (distinct from OOS): reported as an error, NOT auto-applied — this is the signal to move the file to `2-EOL products/` (see CLAUDE.md's EOL section), a human/agent judgment call, never automatic

**Usage:**
```bash
python tools/audit-geo.py --dry-run              # report only, no writes — always run this first
python tools/audit-geo.py                        # full audit + auto-apply
python tools/audit-geo.py --category power-supplies   # single category dir
python tools/audit-geo.py --dry-run --category monitors
```

**Auto-apply — what it's safe to trust vs what still needs judgment:**
- Auto-applies (100% mechanical, no ambiguity): price sync, OOS flag insertion, back-in-stock flag removal, URL correction
- Before writing, it backs up the original file to `tools/backups/<run-timestamp>/<path>.md.bak` — if a run goes wrong, restore from there (or `git checkout -- <file>`, since the repo is version-controlled anyway)
- Does NOT auto-apply: moving files to `2-EOL products/`, anything involving Selling Points/FAQ/Comparison copy — those still require an agent to read `tools/change-report.json` and make a judgment call

**Output:** `tools/change-report.json` — full audit summary plus `changes[]` array with `price_changed`, `needs_oos_flag`, `back_in_stock`, `url_changed`, `applied`, `backup` per SKU, and a separate `errors[]` array for SKUs not found in BC or fetch failures.

**Rate limiting:** self-paced against BC's 150 req/30s cap via a sliding window (not a fixed "pause every N calls") — safe whether the run covers 259 SKUs or scales toward the full 7000+ BC catalog. Batches `sku:in` queries at 40 SKUs per request — BC's edge/WAF returns 414 (URL too long) above that, which silently misreports as "not found" if not chunked correctly.

---

## Deciding What to Write Next (`tools/coverage-report.py`)

**Run this before planning any new GEO-writing batch.** It answers "what's actually missing" per category — live BC in-stock SKU count vs. GEO files already written — instead of relying on stale task lists or guesswork.

**Usage:**
```bash
python tools/coverage-report.py                  # print table only
python tools/coverage-report.py --write           # also refresh tools/geo-coverage.md
python tools/coverage-report.py --category monitors
```

**Stock basis: OH (Onehunga) > 0**, same as `audit-geo.py` — WL/SL/SU are internal, never customer-available. Do not use BC's `availability=available`, it counts supplier-only stock and badly overstates coverage.

**Do not hand-edit `tools/geo-coverage.md`** — it's generated output, regenerate with `--write` instead.

**Known category-ID trap this tool already handles correctly — be aware of it if you ever query BC categories directly elsewhere:** BC's `categories:in` filter does **not** roll up subcategories, and different category trees fail in different directions:
- CPU/Memory/SSD/HDD/PSU/Cases: real products sit almost entirely on **leaf** subcategories — querying the parent ID alone undercounted CPU by ~9x (11 direct vs 91 across its two leaves)
- Gaming Mice/Monitors: leaf subcategories **overlap** (a product can be tagged to two at once) — summing separate leaf counts double-counts
- Video Cards: some products are tagged only at the **parent/mid-level** node, not any specific leaf — summing leaves-only undercounts

The safe method when overlap direction is unknown: one combined `categories:in=id1,id2,...` query across every level of the subtree in a single call — BC returns each matching product exactly once no matter how many of the given ids it satisfies, so this can't double-count or undercount. This is `coverage-report.py`'s `mode="dedup"`.

Gaming Headsets: `476` in older docs/mirrors of the category table is wrong — the live BC id is `484` (`476` is a different category, *Over Ear Headphones*).
