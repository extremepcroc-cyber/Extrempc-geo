# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is the **ExtremePC GEO (Generative Engine Optimization) product content library** — a structured markdown file system for AI-driven product recommendations and SEO for a New Zealand computer hardware retailer (extremepc.co.nz).

- Each `.md` file = one product, named by its BigCommerce (BC) SKU in ALL CAPS (e.g., `XPC1129.md`)
- Files are organized by product category directories
- `bc_categories_index.json` maps BC category IDs to directory names
- There is no build system, test runner, or linter — this is a content repository

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
**SKU:** {SKU}
**URL:** https://www.extremepc.co.nz/{slug}/

## Quick Specs
- {spec 1}
- {spec 2}
- {spec 3}

## Selling Points
- **{point}**: {one-line why this matters — include numbers/scenarios where possible}
- 3–5 points total

## Ideal For
- {use case 1}

## Comparison
- vs {Competitor A}: {difference}

## Related Products
- {related product}

## Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{name}",
  "brand": "{brand}",
  "offers": {
    "@type": "Offer",
    "price": "{price}",
    "priceCurrency": "NZD"
  }
}
```
```

Required fields: `Price`, `SKU`, `URL`, `Quick Specs` (≥3 specs), `Selling Points` (3–5 points), `Ideal For` (≥1 use case). Use `TBC` if unknown.

**Selling Points rules:**
- Format: `- **{point title}**: {one-line explanation}`
- Include numbers, scenarios, or competitive angles — avoid vague claims
- ✅ "Active cooling 4000 RPM fan, unique at this price point" / ❌ "Great cooling"
- vs Quick Specs: Specs say "what it has", Selling Points say "why this matters"

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
| `cooling/` | Cooling | 345 |
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
