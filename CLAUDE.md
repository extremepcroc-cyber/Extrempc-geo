# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is the **ExtremePC GEO (Generative Engine Optimization) product content library** — a structured markdown file system for AI-driven product recommendations and SEO for a New Zealand computer hardware retailer (extremepc.co.nz).

- Each `.md` file = one product, named by its BigCommerce (BC) SKU in ALL CAPS (e.g., `XPC1129.md`)
- Files are organized by product category directories
- `bc_categories_index.json` maps BC category IDs to directory names
- There is no build system, test runner, or linter — this is a content repository

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

## Product File Structure (from `TEMPLATE.md`)

Every product file must follow this exact structure and section order:

```markdown
# {Product Name}

**Price:** ${price} inc GST
**SKU:** {BC SKU}
**MPN:** {manufacturer part number}
**URL:** https://www.extremepc.co.nz/{slug}/

## Quick Specs
- 5+ specs covering performance, materials, certifications, durability data, warranty

## Selling Points
- 3–5 points, each 2–4 sentences. Lead with differentiation, support with data/scenario/certification, pre-empt one likely objection.

## Ideal For
- 3+ specific user personas with context (use case + duration + environment + constraints)

## Why Buy From ExtremePC
- 3+ reasons specific to ExtremePC: exclusive NZ distribution / local warranty / Auckland Build Team / Afterpay etc.

## Comparison
- 3+ comparisons. Name competitors explicitly (model + NZD price). Acknowledge competitor strengths honestly.

## FAQ
- 3+ Q&A pairs. Cover noise, warranty process, install difficulty, bundling, stock, returns, etc.

## Related Products
- Same-brand alternates, step-up/step-down options, accessories

## Schema (JSON-LD)
- Includes brand, sku, mpn, offers with NZD/inStock/seller
```

**Required fields**: `Price`, `SKU`, `MPN`, `URL`, `Quick Specs`, `Selling Points`, `Ideal For`, `Why Buy From ExtremePC`, `Comparison`, `FAQ`, `Schema`. Use `TBC` if unknown.

**GEO depth standards (apply to every field):**
- **Concrete numbers** — replace adjectives with parameters, certifications, test data
- **Scenarios** — specify use case, duration, environment, user type
- **NZ localization** — climate (Auckland summer), local pricing context, delivery, warranty service
- **Pre-empt objections** — answer pre-purchase concerns inside the content
- **Authority** — cite third-party certifications (BIFMA, OEKO-TEX, BIFMA), test cycle counts, brand heritage

## One File, One Product — No Batch Generation

**Every GEO file must be written independently. Batch generation, template copy-paste, and find-and-replace are forbidden.**

Each product has a different GPU architecture, feature set, target audience, and competitive position. Copy-pasting a template and swapping the model name produces factually wrong content — wrong brand names, wrong technology (e.g., writing "DLSS 4" for an Intel Arc GPU that uses XeSS), wrong comparisons, wrong personas.

**Mandatory per-file checklist before writing:**
- Confirm the GPU brand and architecture from the fetch-category JSON (Intel / NVIDIA / AMD — never assume)
- Confirm which upscaling tech the GPU supports: DLSS (NVIDIA only), XeSS (Intel Arc), FSR (AMD)
- Write Selling Points, Ideal For, and Comparison fresh for this specific SKU — do not copy from a sibling product
- Cross-check Related Products: never list the current SKU as a related product

**Signs your file was batch-generated (fail = rewrite from scratch):**
- ❌ Selling Points mention a technology the GPU doesn't support (e.g., "DLSS 4" on an Arc B580)
- ❌ GPU brand or architecture is wrong (e.g., "NVIDIA" for an Intel card)
- ❌ Price fields contain scientific notation (`$3e+03` instead of `$3,000`)
- ❌ Related Products lists the current SKU
- ❌ Comparison text refers to a different GPU tier than what's in this build

**Anti-patterns (delete on sight):**
- ❌ "Great performance" / "Excellent quality" / "Premium build" — empty adjectives
- ❌ "vs similar products at this price" — vague comparisons without naming names
- ❌ "Suitable for office workers" — persona without context
- ❌ Generic content that could apply to 100 different products
- ❌ Exact dollar amounts anywhere except the `Price` field and `Schema.offers.price` — use tier language ("premium-tier", "entry-tier") instead. Reason: prices change; tier language doesn't need re-editing when BC API syncs a new price.

**Selling Points example:**
- ❌ One-liner: "Great cooling"
- ✅ Multi-sentence: "Active seat ventilation at this price point — 4000 RPM centrifugal fan inside the cushion with smart on/off sensor. Two speeds: low (36hr runtime, near-silent) for office, high (9hr) for Auckland 25°C+ summers. Herman Miller Aeron at higher NZD relies on passive mesh — adequate in mild climate but no answer for NZ humidity. Tested through 120,000 BIFMA recline cycles with fan active."

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
| `gaming-headsets/` | Gaming Headsets | 476 |
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

## Price and Stock Audit (`tools/audit-geo.py`) — current tool, use this one

**`tools/audit-geo.py` is the current audit tool.** `tools/audit-geo.ps1` still exists in the repo but is legacy/deprecated — it made 2 API calls per SKU (400+ calls for a full audit) with no rate-limit protection, no backup mechanism, and no URL-change detection. Do not use it for new work; it is kept only for reference.

**When to run:** before any batch editing session, or when the store manager reports prices have changed.

**What it checks:**
- **Price**: parses `**Price:**` from each `.md` file, fetches current BC price (×1.15 for GST), flags if difference > $0.05
- **Stock**: reads `__Stock Available Onehunga` (OH) from BC custom fields, fetched inline via `include=custom_fields` — no per-SKU extra call. Only OH = customer-available; WL/SL/SU are internal and ignored.
- **URL**: compares GEO `**URL:**` against BC's live `custom_url.url` — catches slug changes that would otherwise 404
- **OOS / back-in-stock**: flags `needs_oos_flag` when OH = 0, flags `back_in_stock` when OH > 0 but the file is still marked OOS
- **Tombstones**: automatically skipped — not checked
- **Not found in BC at all** (distinct from OOS): reported as an error, NOT auto-applied — this is the signal to move the file to `2-EOL products/` (see above), a human/agent judgment call, never automatic

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

**Rate limiting:** self-paced against BC's 150 req/30s cap via a sliding window (not a fixed "pause every N calls") — safe whether the run covers 259 SKUs (today) or scales toward the full 7000+ BC catalog as GEO coverage grows. Batches `sku:in` queries at 40 SKUs per request — BC's edge/WAF returns 414 (URL too long) above that, which silently misreports as "not found" if not chunked correctly.

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

**Always run this script first before writing GEO files for a subcategory.** Never have an AI agent call the BC API directly — models make mistakes with pagination, GST calculation, and custom-field parsing. The script outputs a clean JSON that agents read directly.

**Usage:**
```powershell
# Fetch all in-stock products for a subcategory (e.g., AIO Water Cooling = 351)
.\tools\fetch-category.ps1 -CategoryId 351

# Include OOS products too
.\tools\fetch-category.ps1 -CategoryId 349 -IncludeOOS

# Custom output path
.\tools\fetch-category.ps1 -CategoryId 347 -OutputFile "tools\fans.json"
```

**Output:** `tools/category-{id}-products.json` — one entry per in-stock product:

| Field | Description |
|---|---|
| `sku` | BC SKU — use as filename |
| `name` | Product name |
| `mpn` | Manufacturer part number |
| `brand` | Brand name (resolved from BC brands list) |
| `price_nzd_inc_gst` | Price already ×1.15 — paste directly into `**Price:**` field |
| `url` | Full extremepc.co.nz URL |
| `stock` | OH / WL / SL / SU breakdown + total |
| `custom_fields` | All BC custom fields (specs, stock, etc.) |

**Agent workflow:**
1. Human runs `fetch-category.ps1 -CategoryId {id}`
2. Human gives the output JSON to the AI agent
3. Agent reads the JSON and writes GEO files — no BC API calls needed

## Task Planning Rules for AI Agents

**Plan by smallest subcategory branch — never by top-level category.**

A top-level category (e.g., Cooling, Motherboards, Memory) can contain 50–200+ SKUs across multiple subcategories. Processing the whole category in one session will exhaust context and cause degraded output or crashes.

**Required planning unit:** one leaf subcategory at a time. Examples:
- ✅ "Write GEO files for AIO Water Cooling (BC 351)" — 10–20 SKUs
- ✅ "Write GEO files for CPU Coolers (BC 349)" — 15–25 SKUs
- ❌ "Write GEO files for Cooling (BC 345)" — 50+ SKUs, too large

**Workflow:**
1. Look up the category tree in `categories-tree.md` to find leaf subcategory IDs
2. Create one task per leaf subcategory (e.g., TaskCreate for each)
3. Query BC API for that subcategory's in-stock products only
4. Write GEO files, commit, then move to the next subcategory task

**Why:** GEO files require BC API calls + deep research + full template content per product. Even 20 products × 2 API calls = 40 requests + writing time. A full category session risks context overflow mid-batch, leaving files half-written.

## Workflow for Adding/Updating Files

1. Copy template from `TEMPLATE.md`
2. Fill content; verify SKU exists in BC admin
3. Place in `geo/{category}/{SKU}.md`
4. `git add` → `git commit` → `git push`

## Blog System (`blog/`)

### File Structure

```
blog/
  TEMPLATE.md                  ← start every new post from here
  内容选题清单.md               ← topic priorities (P1–P5)
  {slug}.md                    ← one file per post, named by BC URL slug
tools/
  publish-blog.py              ← publishes/updates post to BC Blog API
```

### Publish Workflow

1. Copy `blog/TEMPLATE.md` → `blog/{slug}.md`
2. Fill in frontmatter (Title H1, BC URL, 发布日期, Meta Description, Tags)
3. Write body in HTML (not markdown — BC strips most HTML tags except `<p>`, `<table>`, `<ul>/<li>`, `<strong>`, `<em>`, `<pre>`, `<hr>`)
4. Publish: `python tools/publish-blog.py blog/{slug}.md --draft` (preview first)
5. Review on BC admin, then: `python tools/publish-blog.py blog/{slug}.md --update {post_id}`
6. `git add` → `git commit` → `git push`

Requires `BC_BLOG_TOKEN` (Content permission scope) set in `extremepc.env`. **Never commit this token to git.**

### BC HTML Tag Restrictions — Verified Behavior

BC's blog editor strips or ignores these tags — **do not use them**:

| Tag | Behavior |
|---|---|
| `<h1>` `<h2>` `<h3>` | **Stripped entirely** — content becomes unstyled body text |
| `<a href="...">` | Rendered but links often 404 — **forbidden** unless Jimmy verifies the URL |

**Use instead:**
- Section headings → `<p style="font-size:24px; font-weight:700; margin:48px 0 14px 0; ...">` (see TEMPLATE.md)
- Links → plain text only

### Known Issues Fixed

- **BOM encoding**: PowerShell writes UTF-8 with BOM by default — `publish-blog.py` reads with `utf-8-sig` to strip it. Always write `.md` files with UTF-8 no-BOM.
- **H2 stripped**: BC removes `<h2>` tags. Use styled `<p>` tags for all section headings.
- **HTML pass-through**: `publish-blog.py` detects if body starts with `<` and skips the markdown converter — body must be pure HTML, not mixed.
- **Date format**: BC Blog API requires RFC-2822 (`Tue, 15 Jul 2026 00:00:00 +0000`). Script converts from `YYYY-MM-DD` automatically.

### Blog Writing Rules

1. One question per post — deep analysis, not a list of answers
2. Open with the user's pain point; second paragraph introduces ExtremePC's perspective
3. Always include a comparison table with blue/green color coding (see TEMPLATE.md)
4. Scenario-based sections (by budget / resolution / use case)
5. Clear recommendation at the end — no hedging
6. Inline CSS only — no external stylesheets
7. **No `<a href>` links** in body — plain text only. Exception: Jimmy-verified URLs only, annotated with "已验证"
8. No `<h2>` / `<h3>` tags — use styled `<p>` for headings

## Review Checklist

- [ ] Filename = BC SKU, ALL CAPS
- [ ] Correct category directory
- [ ] Price, SKU, URL present (or `TBC`)
- [ ] No Chinese filenames
- [ ] Matches template structure exactly
- [ ] SKU verifiable in BC admin
