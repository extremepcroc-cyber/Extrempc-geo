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

## For AI Agents Reading Product Files

GEO files are **not real-time** — prices may have changed. To get current pricing from BC API:
```
GET /catalog/products?sku:in={SKU}&include_fields=price,calculated_price
# Multiply ex-GST price × 1.15 for NZD inc GST
```

If a product has no GEO file: use BC API for basic specs, tell the user "this product doesn't have detailed comparison info yet", and notify Jimmy to create the file.

AI agents may modify file content with these rules:
- **Direct update**: `Price` (sync from BC API, ×1.15 for GST) and `Quick Specs` (sync from BC)
- **Can optimize with explanation**: `Ideal For`, `Comparison`, `Related Products`, Schema JSON — GEO copy can be improved, but agent must state what changed and why
- **Never touch**: `URL`, filenames, directory structure

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

**Discontinued products** (removed from BC entirely) → delete the file.

## Price and Stock Audit (`tools/audit-geo.ps1`)

Use this script to detect GEO files that are out of date — price changed in BC, stock went to zero, or stock location shifted.

**When to run:** before any batch editing session, or when Jimmy reports prices have changed.

**What it checks:**
- **Price**: parses `**Price:**` from each `.md` file, fetches current BC price (×1.15 for GST), flags if difference > $0.05
- **Stock**: calls `/catalog/products/{id}/custom-fields` per SKU to read `__Stock Available Onehunga/Wellington/St Lukes/Supplier` — because stock lives in custom fields, NOT `inventory_level`
- **OOS trigger**: flags `needs_tombstone: true` when total stock (OH+WL+SL+SU) = 0
- **Stock shift**: detects when GEO describes retail stock but BC now shows supplier-only (or vice versa)
- **Tombstones**: automatically skipped — not checked

**Usage:**
```powershell
# Full audit — all categories
.\tools\audit-geo.ps1

# Single category only
.\tools\audit-geo.ps1 -CategoryDir "power-supplies"

# Preview only, no file written
.\tools\audit-geo.ps1 -DryRun
```

**Output:** `tools/change-report.json` — contains only SKUs flagged `needs_update: true`, with:
- `price_geo_nzd` / `price_bc_nzd` — old vs new price
- `stock` — current OH/WL/SL/SU breakdown
- `needs_oos_flag` — true if total stock = 0
- `file` — relative path to the GEO file to edit

**After running the script:**
- Read `change-report.json`
- For price changes: update `**Price:**` field and `Schema.offers.price` only — do not touch other content
- For `needs_oos_flag: true`: add `**Status:** OUT OF STOCK — last checked {date}` below URL, change Schema to `OutOfStock`. **Never delete GEO content.**
- For stock shifts (retail → supplier): update `NZ Stock` line in Quick Specs and any stock references in Selling Points / Why Buy sections

**BC API rate limit:** script pauses every 40 calls to stay within 150 req/30s. Expect ~2–3 minutes for a full audit of 200+ SKUs.

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

## Review Checklist

- [ ] Filename = BC SKU, ALL CAPS
- [ ] Correct category directory
- [ ] Price, SKU, URL present (or `TBC`)
- [ ] No Chinese filenames
- [ ] Matches template structure exactly
- [ ] SKU verifiable in BC admin
