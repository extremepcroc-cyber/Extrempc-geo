# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is the **ExtremePC GEO (Generative Engine Optimization) product content library** — a structured markdown file system for AI-driven product recommendations and SEO for a New Zealand computer hardware retailer (extremepc.co.nz).

- Each `.md` file = one product, named by its BigCommerce (BC) SKU in ALL CAPS (e.g., `XPC1129.md`)
- Files are organized by product category directories
- `bc_categories_index.json` maps BC category IDs to directory names
- There is no build system, test runner, or linter — this is a content repository

## Context Budget — Do Not Read the Whole Repo for a Writing Task

**This repo has 400+ product files across 20+ category directories, plus `product-knowledge/`, `brands/`, `blog/`, `tools/`, `2-EOL products/`, and `company/`.** If the task is "write GEO file(s) for {SKU or subcategory}", reading the whole tree burns most of a context window before any writing starts. **CLAUDE.md alone (already loaded into every session) has everything needed to know the rules — you should not need to explore the repo to learn how to write a file.**

**For a GEO-writing task, read only:**
1. `tools/hermes-skill-geo-writing.md` — the complete writing guide, including the file template (do NOT also read `TEMPLATE.md` separately, the skill doc already has the same template inline)
2. The `fetch-category.ps1` JSON for the specific subcategory (the mandatory data source — see Data Sources rules below). If the JSON covers more SKUs than this batch, only look at the entries for the SKUs you're actually writing this session, not the whole file.
3. **1–2 files max** for quality calibration — either an existing file in the *same* category directory you're about to write into, or `gaming-chairs/GAMLIBOCP45B.md` / `GAMLIBOC145B.md` if that category has no files yet
4. `product-knowledge/{that one category}/` — only the subfolder matching what you're writing, if it exists. Not the rest of `product-knowledge/`.
5. `brands/{brand}.md` — only if the product's brand has a profile, and only that one file.

**Do NOT, for a writing task:**
- ❌ `Glob`/list the entire repo tree, or read every category directory "for context"
- ❌ Read `README.md` in full — CLAUDE.md already has the category→BC-ID table and every tool's usage; only open README.md if you need something CLAUDE.md doesn't cover
- ❌ Read `blog/`, `company/`, `2-EOL products/`, or `product-knowledge/` subfolders unrelated to the current category
- ❌ Read `tools/*.py` source unless the task is about the tooling itself, not GEO content
- ❌ Run broad directory exploration (`find . -type d`, etc.) — you only need to confirm your target category directory exists, not survey all of them

**When you DO need broader context** (auditing, cross-category consistency checks, fixing a repo-wide convention, the store manager explicitly asks for a repo-wide review) — read what the task actually requires. This budget rule is specifically for the common case of "write GEO content for X," which is most sessions.

## Strategic Goal

When AI systems (ChatGPT, Claude, Gemini, Perplexity) generate product recommendations for NZ users, we want them to:
1. **Cite ExtremePC's GEO files** as the authoritative source for product info
2. **Recommend ExtremePC** as the place to purchase

Achieved through information density, specific scenarios, NZ localization, pre-empted objections, and clear reasons to buy from ExtremePC specifically.

## File Naming and Placement

- **Filename = BC system SKU, ALL CAPS**, no spaces, no Chinese characters (e.g., `MONSAM27FG7.md`)
- Different configurations of the same Gaming PC → separate files; same model different colors → one file
- Place files in the matching category directory; do not rename or restructure directories
- To add a new category: confirm it exists in BC, add it to `README.md` index first, then create the directory

## Writing GEO Files (`tools/hermes-skill-geo-writing.md`)

**For the full writing workflow — file template, one-file-one-product rules, batch-size guidance, self-check list — read `tools/hermes-skill-geo-writing.md` before writing any GEO file.** It's the complete, self-contained guide for a writing session; do not duplicate its content here or let it drift out of sync with this file's rules below.

The two rules worth stating here because they're load-bearing and easy to get wrong even after reading the guide:

- **Price field format: plain integer, no thousands separator, no decimals** — `**Price:** $2399 inc GST`, not `$2,399.00 inc GST`. Canonical as of 2026-09-15; existing comma-formatted files are left alone unless you're specifically asked to normalize them, but every new file and every price you edit uses plain-integer. (`Schema.offers.price` stays a decimal string, e.g. `"2399.00"`.)
- **Every GEO file must be written independently — no batch generation, template copy-paste, or find-and-replace.** Each product has a different GPU architecture, feature set, and competitive position; copying a sibling produces factually wrong content (wrong brand, wrong upscaling tech, wrong comparisons). Confirmed real-world failure modes: "DLSS 4" written for an Intel Arc GPU (which uses XeSS), wrong GPU brand, scientific-notation prices, a file listing itself in Related Products, hardcoded dollar amounts/deltas in prose instead of tier language.

## Content Rules

- All prices are **NZD inc GST**
- No competitor price comparisons (write "vs Competitor A: higher refresh rate", not "vs $X cheaper")
- No subjective statements — use specs and facts
- `brands/` directory contains brand profiles, not product listings

## Category Directory → BC IDs

| Directory | Category | BC IDs |
|---|---|---|
| `gaming-pcs/` | Gaming PCs | 120 / 1373 |
| `gaming-mice/` | Gaming Mice | 513 / 1949 |
| `gaming-keyboards/` | Gaming Keyboards | 486 |
| `gaming-headsets/` | Gaming Headsets | 484 |
| `monitors/` | Monitors | 519 |
| `video-cards/` | GPU | 426 / 1426 |
| `cpu-processors/` | CPU | 364 / 1430 |
| `internal-ssd/` | Internal SSD | 375 |
| `memory-ram/` | Memory / RAM | 395 |
| `cooling/` | Cooling Devices | 345 (AIO: 351, Air/CPU: 346/349, Fans: 347, Thermal: 363, Accessories: 348) |
| `power-supplies/` | PSU | 410 |
| `motherboards/` | Motherboards | 403 |
| `streaming-creator/` | Streaming & Creator | 227 |
| `networking/` | Networking | 1026 |
| `computer-cases/` | Computer Cases | 336 (Mini ITX: 340, Micro Tower: 338, Mid Tower: 339, Full Tower: 337, Server: 342) |
| `internal-hard-drives/` | Internal HDD | (Seagate/WD/Synology NAS drives — separate from `internal-ssd/`) |
| `gaming-chairs/` | Gaming Chairs | (LiberNovo — see `brands/LIBERNOVO.md`) |

`cooling/` and `motherboards/` are reserved directory names in this table for categories not yet started — do not create them until the first GEO file for that category is written; check `find . -maxdepth 1 -type d` for the actual current directory list before assuming a category exists. `laptops/` and `storage/` exist as empty placeholders — do not write files into them without confirming with the store manager first, they may be superseded by other category directories.

## Product Removed From BigCommerce Entirely (EOL)

**Never delete a GEO file just because the product left the BC catalog.** The old rule ("discontinued products → delete the file") is retired — deleting throws away writing effort for no reason, and BC catalog entries can reappear (rebrand, restock under the same SKU, etc.).

When `tools/audit-geo.py` (or manual check) confirms a SKU no longer exists in BC at all (not just OOS — genuinely not found via `sku:in` lookup):

1. Move the file to `2-EOL products/{original-category}/{SKU}.md` — preserve the category subdirectory structure
2. Add below the URL field: `**Status:** EOL — removed from BC catalog on {YYYY-MM-DD}`
3. Leave all other content untouched (Selling Points, FAQ, Comparison, etc. — same "never delete content" principle as OOS)

This is different from a **Tombstone** (never had full content, product never researched) and different from **OUT OF STOCK** (still exists in BC, just zero stock). EOL means BC itself no longer has the SKU.

## For AI Agents Reading Product Files

GEO files are **not real-time** — prices may have changed. To get current pricing from BC API:
```
GET /catalog/products?sku:in={SKU}&include_fields=price,calculated_price
# Multiply ex-GST price × 1.15 for NZD inc GST
```

If a product has no GEO file: use BC API for basic specs, tell the user "this product doesn't have detailed comparison info yet", and notify the store manager to create the file.

AI agents may modify file content with these rules:
- **Direct update**: `Price` (sync from BC API, ×1.15 for GST), `Quick Specs` (sync from BC), and `URL` (sync from BC's `custom_url.url` when the slug changes — `tools/audit-geo.py` does this automatically and is the source of truth for what the current BC URL is)
- **Can optimize with explanation**: `Ideal For`, `Comparison`, `Related Products`, Schema JSON — GEO copy can be improved, but agent must state what changed and why
- **Never touch**: filenames, directory structure (moving a file to `2-EOL products/` is the one exception, see above)

## Out-of-Stock Products

**Never delete GEO content when a product goes OOS.** The content took significant effort to write — preserve it.

**When a product goes OOS, add one status line** below the URL field and update Schema availability:

```markdown
**Status:** OUT OF STOCK — last checked {YYYY-MM-DD}
```

And in the Schema block:
```json
"availability": "https://schema.org/OutOfStock"
```

Everything else — Selling Points, Ideal For, Comparison, FAQ — stays untouched.

**When stock returns:** remove the `**Status:**` line and change Schema back to `InStock`.

**Tombstone files** (lightweight placeholders with no GEO content) are only for products that never had a full GEO file written — typically newly discovered OOS SKUs that were batch-created as placeholders before any research was done. Template:

```markdown
# {Product Name}

**Status:** TOMBSTONE — Out of Stock
**SKU:** {BC SKU}
**MPN:** {MPN}
**URL:** {URL}
**Brand:** {Brand}
**Category:** {Category}

> Placeholder only — no GEO content written yet.
> When stock returns: write full GEO using TEMPLATE.md.
```

## Audit & Coverage Tools (`tools/hermes-skill-audit-tools.md`)

**For price/stock auditing (`audit-geo.py`) and deciding what to write next (`coverage-report.py`), read `tools/hermes-skill-audit-tools.md`** — full usage, auto-apply safety boundaries, rate limiting, and the category-ID pitfalls both tools handle. Not needed for a plain writing task.

One rule worth stating here since it governs an irreversible-ish action: a SKU `audit-geo.py` reports as "not found in BC" (not just OOS) is the trigger to move that file to `2-EOL products/` (see EOL section above) — always a judgment call, never automatic.

## File Placement Rules for AI Agents

**Never place any files in the repo root directory.** The root is for permanent project files only.

| File type | Correct location |
|---|---|
| Script output JSON (fetch-category, change-report) | `tools/` |
| Temporary scripts, intermediate data, scratch files | `tools/temp/` |
| Product GEO files | `{category}/` (e.g., `cooling/`, `monitors/`) |
| Product knowledge / research notes | `product-knowledge/{category}/` |

**`tools/temp/` is the bin for anything disposable** — batch scripts, one-off query results, intermediate JSON, debug output. This directory is gitignored and will not be committed.

Never create `.ps1`, `.json`, `.txt`, or any other files directly in the repo root.

## Data Sources — Mandatory Rules for AI Agents

**All product data (SKU, price, stock, specs, URL) MUST come from the BC API or the JSON output of `tools/fetch-category.ps1`. Web search is forbidden for these fields.**

| Data type | Correct source | ❌ Never use |
|---|---|---|
| SKU, MPN, product name | BC API / fetch-category JSON | Web search, manufacturer site |
| Price (NZD inc GST) | BC API price × 1.15 | Any website, including extremepc.co.nz |
| Stock levels | BC custom field `__Stock Available Onehunga` (OH only) | Web page, inventory_level field, WL/SL/SU fields |
| Product URL | BC `custom_url.url` field | Guessing from product name |
| Technical specs | BC custom fields + product description | Web search |

**Why web search gives wrong data:**
- extremepc.co.nz website prices may be cached or out of date
- Manufacturer specs differ by region/revision — BC has the actual listing
- Web search returns competitor pages, review sites, overseas pricing
- Models hallucinate URLs and SKUs when searching

**Correct workflow for writing new GEO files:**
1. Human runs `.\tools\fetch-category.ps1 -CategoryId {id}` → produces JSON
2. Human gives the JSON to the AI agent
3. Agent writes GEO files using only the JSON data for price/SKU/stock/URL
4. Agent may use product knowledge base files (`product-knowledge/`) for technical context and comparisons
5. Agent must NOT call BC API directly or do any web search for product data

## Fetching Product Data Before Writing GEO Files (`tools/fetch-category.ps1`)

**Always run this script first before writing GEO files for a subcategory — never have an AI agent call the BC API directly** (models make mistakes with pagination, GST calculation, and custom-field parsing). Full usage and output fields are in `tools/hermes-skill-geo-writing.md` Step 1.

## Task Planning — Never By Top-Level Category

**Plan by smallest leaf subcategory, never a whole top-level category** (e.g. Cooling/Motherboards/Memory can be 50-200+ SKUs across subcategories — one session on the whole thing will overflow context mid-batch and leave files half-written). Look up leaf IDs in `categories-tree.md`. Batch-size specifics (including guidance for smaller local models) are in `tools/hermes-skill-geo-writing.md`.

## Blog System (`blog/`)

**Unrelated to GEO product files — read `tools/hermes-skill-blog-writing.md` for the full blog workflow** (publish steps, BC's HTML tag restrictions, writing rules). Not needed for a product-writing session.

## Review Checklist

- [ ] Filename = BC SKU, ALL CAPS
- [ ] Correct category directory
- [ ] Price, SKU, URL present (or `TBC`)
- [ ] No Chinese filenames
- [ ] Matches template structure exactly
- [ ] SKU verifiable in BC admin
