# Skill: ExtremePC GEO File Writing

**Trigger:** Any task involving writing, updating, or reviewing GEO product files for extremepc.co.nz.

**This is the complete guide for a GEO-writing session.** You should not need to read CLAUDE.md's full audit/coverage-tool docs, the blog system section, or explore the rest of the repo — this file plus the JSON you're given is enough to write correct files. If something here seems to conflict with CLAUDE.md, CLAUDE.md wins (this file is a working guide, CLAUDE.md is the source of truth) — but flag the conflict rather than silently picking one, it means this file drifted and needs fixing.

---

## What Is a GEO File

A GEO file is a structured Markdown product page optimised for AI search engines (Perplexity, ChatGPT, Gemini). Each file = one product, named by its BC SKU in ALL CAPS (e.g. `XPC12359.md`). Files live in category directories under the repo root (e.g. `gaming-pcs/`, `cooling/`, `monitors/`). Category → BC ID mapping is in `CLAUDE.md`'s "Category Directory → BC IDs" table — don't re-derive it, just look it up there.

---

## Context Budget — This Matters More Than It Looks

The repo has 400+ product files across 20+ categories. **Do not Glob the repo tree, do not read other categories "for context," do not read `blog/`, `company/`, `2-EOL products/`, or unrelated `product-knowledge/` subfolders.** Read only: this file, the fetch-category JSON for your subcategory, 1-2 calibration files (below), and the one `product-knowledge/{category}/` subfolder that matches what you're writing.

**Batch size — if you're running on a smaller/local model (≤160k context), plan for 3-5 files per batch, not 10-20.** Each GEO file is 100-130 lines of dense, fact-checked prose; by file 8-10 in one continuous session, quality visibly degrades (generic phrasing, copied comparisons, missed brand/spec details) even before you hit a hard context wall. If you're a large-context model (Claude with 1M context, etc.) you can push batches larger, but still plan by leaf subcategory (see Step 2), never a whole top-level category in one go.

---

## Step 0 — Check What's Actually Missing

Before planning a batch, run `python tools/coverage-report.py --category {your-category}` to confirm there's a real gap and see the true live-BC-vs-written-files count. Don't rely on a stale task list or assumption — coverage numbers for several categories were found to be badly wrong before this tool existed (see CLAUDE.md's "Deciding What to Write Next" section for the category-ID pitfalls it handles). If the report says gap=0, stop and confirm with whoever assigned the task before writing anything.

---

## Quality Reference — Read Before Writing

**Golden standard:** `gaming-chairs/` directory (10 LiberNovo chair files).

Before writing GEO files for any new category, read **1-2 files max** from `gaming-chairs/` to calibrate (or an existing file in the category you're about to write into, if one already exists — prefer that, it's more directly comparable):
- Technical depth (specs with real numbers, not adjectives)
- Selling Points length (2-4 full sentences per point, differentiation → data → objection pre-emption)
- User persona specificity (height range, session duration, environment, constraints)
- Comparison honesty (acknowledge competitor strengths, give decision logic)
- FAQ real-world relevance (noise, warranty, install, pairing, try-before-buy)
- Why Buy From ExtremePC substance (specific reasons, not boilerplate)

**Key reference files:**
- `gaming-chairs/GAMLIBOCP45B.md` — Premium tier example (131 lines, BIFMA data, NZ climate analysis)
- `gaming-chairs/GAMLIBOC145B.md` — Mid-tier example (129 lines, upgrade/downgrade logic)
- `gaming-chairs/GAMLIBSE45B.md` — Entry tier example (130 lines, mechanical vs electronic tradeoffs)

---

## Step 1 — Get Product Data (ALWAYS first)

**Never write a GEO file from memory, web search, or manufacturer sites.**

Product data must come from the JSON output of `tools/fetch-category.ps1`.

If the JSON has not been provided yet, stop and ask:
> "Please run `.\tools\fetch-category.ps1 -CategoryId {id}` and give me the output JSON before I start writing."

```powershell
.\tools\fetch-category.ps1 -CategoryId 351              # in-stock only (e.g. AIO Water Cooling = 351)
.\tools\fetch-category.ps1 -CategoryId 349 -IncludeOOS   # include OOS too
.\tools\fetch-category.ps1 -CategoryId 347 -OutputFile "tools\fans.json"
```

Output: `tools/category-{id}-products.json`, one entry per product:

| Field | Use for |
|---|---|
| `sku` | filename (`{SKU}.md`) |
| `name` | H1 title |
| `price_nzd_inc_gst` | `**Price:**` field (plain integer, no commas, e.g. `$3499`) |
| `url` | `**URL:**` field |
| `mpn` | `**MPN:**` field |
| `brand` | Schema |
| `stock` | OH/WL/SL/SU breakdown for Quick Specs NZ Stock line |
| `custom_fields` | technical specs |

**If the JSON covers more SKUs than this batch (e.g. a 60-product category JSON but you're only writing 4-5 this session), only read the entries for the SKUs you're actually writing.** Don't hold the whole file in context for a small batch.

**⚠️ Real incident (2026-09-15): a batch of 68 keyboard files was written with 52 wrong prices — some off by 50-76% — even though the source JSON had the correct number the whole time** (e.g. one file was written at $79 when its own JSON entry said `price_nzd_inc_gst: 139`). This wasn't stale data, it was copying the wrong number while writing. **Before moving to the next file, re-read the price you just wrote against the JSON entry for that exact SKU — don't trust memory of "roughly what it was."**

---

## Step 2 — Plan Before Writing

List every SKU you will write, in order, before starting. Do not start writing until the plan is confirmed (with the user, or with yourself if working autonomously — just don't skip straight to writing).

**Planning unit = one leaf subcategory at a time.** Never plan an entire top-level category (Cooling, Motherboards, Memory) in one session — it will overflow context mid-batch. Look up leaf subcategory IDs in `categories-tree.md`.

Example plan:
```
SKUs to write (AIO Water Cooling, BC 351):
1. COOLABC360X — be quiet! Pure Loop 2 360mm
2. COOLMSI360R — MSI MEG Coreliquid S360
3. COOLLIAN360 — Lian Li Galahad II 360
... etc
Estimated: 12 files. Batch size 4 — three sessions.
```

---

## Step 3 — Write Each File Independently

**Every file must be written from scratch. No copy-paste from sibling products. No batch find-and-replace.**

Each product has different GPU/CPU architecture, upscaling tech, target persona, and competitive position. Copy-paste produces factually wrong content — wrong brand, wrong tech (e.g. "DLSS 4" on an Intel Arc card, which uses XeSS), wrong comparisons.

### Before writing each file, confirm:

- [ ] GPU brand: Intel / NVIDIA / AMD? (check JSON — never assume)
- [ ] Upscaling tech: DLSS = NVIDIA only | XeSS = Intel Arc only | FSR = AMD only
- [ ] Stock location: retail (OH/WL/SL) or supplier-only (SU)?
- [ ] Price is a plain integer from the JSON (no commas, no decimals) — **and matches the JSON exactly, see the incident note in Step 1**

### Required file structure (in this exact order):

```markdown
# {Product Name}

**Price:** ${price} inc GST
**SKU:** {SKU}
**MPN:** {MPN}
**URL:** {URL}

## Quick Specs
(5+ specs — concrete numbers, certifications, test data. No adjectives.)

## Selling Points
(3–5 points, 2–4 sentences each. Lead with differentiation, support with data/scenario, pre-empt one objection.)

## Ideal For
(3+ personas — each must have: use case + duration + environment + constraints)

## Why Buy From ExtremePC
(3+ reasons — local warranty, Auckland Build Team, NZ stock, Afterpay, etc.)

## Comparison
(3+ named competitors with model names. Acknowledge competitor strengths honestly.)

## FAQ
(3+ Q&A pairs — noise, warranty process, install difficulty, stock, returns)

## Related Products
(Same-brand alternates, step-up/step-down, accessories — never list this file's own SKU)

## Schema (JSON-LD)
(Include brand, sku, mpn, offers with NZD price, InStock/OutOfStock, seller)
```

Required fields: `Price`, `SKU`, `MPN`, `URL`, `Quick Specs`, `Selling Points`, `Ideal For`, `Why Buy From ExtremePC`, `Comparison`, `FAQ`, `Schema`. Use `TBC` only if genuinely unknown after checking the JSON.

---

## Content Rules

**Numbers over adjectives:**
- ❌ "Great cooling performance"
- ✅ "Tested to 50,000 pump-cycle MTBF; keeps Ryzen 9 9950X under 72°C at 200W package power"

**Personas need full context:**
- ❌ "Suitable for gamers"
- ✅ "PC builders in Auckland running a Ryzen 7 9700X who game 4–6 hours daily and want sub-70°C temps without fan noise above 35 dB"

**Prices in body content = tier language only, never a dollar figure or a dollar difference:**
- ❌ "At $249 this beats the competition" / "$20 cheaper than the alternative"
- ✅ "At mid-tier pricing, this outperforms entry-tier 240mm AIOs" / "a moderate premium over the entry option"
- Exception: `**Price:**` field and `Schema.offers.price` — use the exact number from the JSON
- Reason: prices change; a hardcoded dollar figure or delta in prose goes stale silently and nothing catches it (the price *field* gets synced by `audit-geo.py`, prose does not)

**All prices are NZD inc GST.** No subjective statements — specs and facts only. `brands/` holds brand profiles, not product listings — don't confuse the two.

**NZ localisation — always include:**
- Auckland summer temps (25°C+, humidity)
- NZ delivery times, warranty service location
- GST-inclusive pricing context

---

## Self-Check Before Committing

- [ ] Filename = SKU, ALL CAPS, `.md` extension
- [ ] File is in the correct category directory
- [ ] Price matches the JSON's `price_nzd_inc_gst` **exactly** — re-check, don't trust memory
- [ ] URL copied exactly from JSON
- [ ] GPU brand/architecture is correct for this specific product
- [ ] Upscaling tech matches the GPU (DLSS/XeSS/FSR)
- [ ] No scientific notation anywhere (`$3e+03` = fail, rewrite)
- [ ] No hardcoded dollar amounts in prose outside the Price field/Schema
- [ ] Related Products does NOT list this file's own SKU
- [ ] Comparison section names specific competitor models (not "similar products")
- [ ] No web search was used for any data in this file
- [ ] Schema JSON has correct `availability` (InStock or OutOfStock based on stock.total)

---

## OOS / EOL — Only If You Hit It Mid-Batch

Full rules live in CLAUDE.md ("Out-of-Stock Products" and "Product Removed From BigCommerce Entirely (EOL)") — this is the short version for while you're writing:

- `stock.total = 0` in the JSON and you're writing full content anyway → write it in full, then add `**Status:** OUT OF STOCK — last checked {date}` below the URL, Schema `availability` → `OutOfStock`
- A SKU in your plan isn't in BC at all anymore → don't write a file for it, don't delete anything that already exists for it — flag it for the EOL process (CLAUDE.md) instead, that's a judgment call, not something to do automatically while writing

---

## Git Workflow

After completing a batch:
```
git add {category}/
git commit -m "feat: write GEO files for {subcategory} ({n} SKUs)"
git push
```

One commit per subcategory batch. Do not mix categories in one commit.
