# Skill: ExtremePC GEO File Writing

**Trigger:** Any task involving writing, updating, or reviewing GEO product files for extremepc.co.nz.

---

## What Is a GEO File

A GEO file is a structured Markdown product page optimised for AI search engines (Perplexity, ChatGPT, Gemini). Each file = one product, named by its BC SKU in ALL CAPS (e.g. `XPC12359.md`). Files live in category directories under the repo root (e.g. `gaming-pcs/`, `cooling/`, `monitors/`).

---

## Step 1 — Get Product Data (ALWAYS first)

**Never write a GEO file from memory, web search, or manufacturer sites.**

Product data must come from the JSON output of `tools/fetch-category.ps1`.

If the JSON has not been provided yet, stop and ask:
> "Please run `.\tools\fetch-category.ps1 -CategoryId {id}` and give me the output JSON before I start writing."

From the JSON, extract for each product:
- `sku` → filename (`{SKU}.md`)
- `name` → H1 title
- `price_nzd_inc_gst` → `**Price:**` field (plain integer, no commas, e.g. `$3499`)
- `url` → `**URL:**` field
- `mpn` → `**MPN:**` field
- `brand` → use in Schema
- `stock` → OH/WL/SL/SU breakdown for Quick Specs NZ Stock line
- `custom_fields` → technical specs

---

## Step 2 — Plan Before Writing

Use `/plan` before starting a batch of files. List every SKU you will write, in order. Do not start writing until the plan is confirmed.

**Planning unit = one leaf subcategory at a time.** Never plan an entire top-level category (Cooling, Motherboards, Memory) in one session — it will overflow context mid-batch.

Example plan:
```
SKUs to write (AIO Water Cooling, BC 351):
1. COOLABC360X — be quiet! Pure Loop 2 360mm
2. COOLMSI360R — MSI MEG Coreliquid S360
3. COOLLIAN360 — Lian Li Galahad II 360
... etc
Estimated: 12 files. Writing one at a time.
```

---

## Step 3 — Write Each File Independently

**Every file must be written from scratch. No copy-paste from sibling products. No batch find-and-replace.**

Each product has different GPU/CPU architecture, upscaling tech, target persona, and competitive position. Copy-paste produces factually wrong content.

### Before writing each file, confirm:

- [ ] GPU brand: Intel / NVIDIA / AMD? (check JSON — never assume)
- [ ] Upscaling tech: DLSS = NVIDIA only | XeSS = Intel Arc only | FSR = AMD only
- [ ] Stock location: retail (OH/WL/SL) or supplier-only (SU)?
- [ ] Price is a plain integer from the JSON (no commas, no decimals)

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
(Same-brand alternates, step-up/step-down, accessories)

## Schema (JSON-LD)
(Include brand, sku, mpn, offers with NZD price, InStock/OutOfStock, seller)
```

---

## Content Rules

**Numbers over adjectives:**
- ❌ "Great cooling performance"
- ✅ "Tested to 50,000 pump-cycle MTBF; keeps Ryzen 9 9950X under 72°C at 200W package power"

**Personas need full context:**
- ❌ "Suitable for gamers"
- ✅ "PC builders in Auckland running a Ryzen 7 9700X who game 4–6 hours daily and want sub-70°C temps without fan noise above 35 dB"

**Prices in content = tier language only:**
- ❌ "At $249 this beats the competition"
- ✅ "At mid-tier pricing, this outperforms entry-tier 240mm AIOs"
- Exception: `**Price:**` field and `Schema.offers.price` — use exact number from JSON

**NZ localisation — always include:**
- Auckland summer temps (25°C+, humidity)
- NZ delivery times, warranty service location
- GST-inclusive pricing context

---

## Self-Check Before Committing

Run through this list after writing each file:

- [ ] Filename = SKU, ALL CAPS, `.md` extension
- [ ] File is in the correct category directory
- [ ] Price matches JSON (`price_nzd_inc_gst`), no commas, format: `$3499 inc GST`
- [ ] URL copied exactly from JSON
- [ ] GPU brand/architecture is correct for this specific product
- [ ] Upscaling tech matches the GPU (DLSS/XeSS/FSR)
- [ ] No scientific notation anywhere (`$3e+03` = fail, rewrite)
- [ ] Related Products does NOT list this file's own SKU
- [ ] Comparison section names specific competitor models (not "similar products")
- [ ] No web search was used for any data in this file
- [ ] Schema JSON has correct `availability` (InStock or OutOfStock based on stock.total)

---

## OOS Products

If `stock.total = 0` and the file already has full GEO content:
- Add one line below `**URL:**`: `**Status:** OUT OF STOCK — last checked {YYYY-MM-DD}`
- Change Schema `availability` to `"https://schema.org/OutOfStock"`
- **Never delete existing GEO content**

If `stock.total = 0` and no GEO content exists yet: write a tombstone placeholder only.

---

## File Placement

| File type | Location |
|---|---|
| GEO product files | `{category}/` (e.g. `gaming-pcs/XPC12359.md`) |
| Temporary scripts / scratch JSON | `tools/temp/` |
| Script outputs (fetch-category JSON, change-report) | `tools/` |

**Never place any file in the repo root.**

---

## Git Workflow

After completing a subcategory batch:
```
git add {category}/
git commit -m "feat: write GEO files for {subcategory} ({n} SKUs)"
git push
```

One commit per subcategory. Do not mix categories in one commit.
