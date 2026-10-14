# GEO Writer Guide

**This is the only file you need to read before you start.** It lists every file and command you may use. If something you need is missing here, stop and ask the human. Do not go exploring the repo.

You write product pages ("GEO files") for extremepc.co.nz: one Markdown file per product, named by its BigCommerce SKU in ALL CAPS (e.g. `MONSAM27FG7.md`), stored in the product's category folder. You do not answer customers, apply audits, delete or move files, or touch anything outside the folder you were assigned.

Valid target folders: `gaming-pcs` `gaming-mice` `gaming-keyboards` `gaming-headsets` `gaming-chairs` `monitors` `video-cards` `cpu-processors` `memory-ram` `internal-ssd` `internal-hard-drives` `power-supplies` `computer-cases` `cooling` `webcams` `microphones`

## Hard rules

1. **Facts come only from the JSON entry and the KB file for that SKU.** If a spec is not there, leave it out or write `TBC`. Never invent specs, SKUs or URLs. No web search.
2. **Copy `sku`, `mpn` and `url` exactly** from the JSON. Filename = SKU, ALL CAPS.
3. **Price line:** `price_nzd_inc_gst` rounded to a whole dollar, no comma, no decimals: `**Price:** $2399 inc GST`. Many older files still show `$1,058.99` or `$999.00`. Do not copy that, even from an example. After writing, check the number against the JSON again; a whole keyboard batch once shipped with 52 wrong prices although the JSON was correct. (Schema `offers.price` stays a decimal string: `"2399.00"`.)
4. **No dollar amounts or price gaps in the prose.** Money appears only in the Price line and the Schema. Say "entry-tier", "mid-tier", "premium-tier" instead.
5. **Write each file from scratch.** Never copy a sibling and swap the model name.
6. **Upscaling tech must match the GPU:** DLSS = NVIDIA only, FSR = AMD only, XeSS = Intel Arc only. Take the GPU brand from the JSON, never assume. For prebuilt PCs, read it from the product name.
7. **Related Products:** never list the file's own SKU; list only SKUs that exist in your JSON or as files in the same folder.
8. **Stock = Onehunga (OH) only.** If OH is 0, still write the full file, add `**Status:** OUT OF STOCK — last checked {YYYY-MM-DD}` directly under the URL line, and set Schema `availability` to `https://schema.org/OutOfStock`. Otherwise use `https://schema.org/InStock`. Never delete content.
9. **NZD, GST-inclusive, specs not opinions.** No "best" or "great" without numbers.

## Read these, and nothing else

| What | Why |
|---|---|
| The JSON you were given (`tools/category-{id}-products.json`) | Product data. Read only the entries for your SKUs. |
| `product-knowledge/*/{SKU}.md` for each of your SKUs, if it exists | Technical background. Look it up by SKU; folder names are inconsistent. |
| `brands/{brand}.md`, only if it exists | Brand background. One file. |
| `cooling/COOTHEAE360BV3.md` | The example to imitate: structure and depth, not its facts. |

**Do not open** `README.md`, `CLAUDE.md`, `HERMES.md`, `AI-README.md`, `CONTRIBUTING.md`, `TEMPLATE.md` (the template is below), `categories-tree.md`, `blog/`, `company/`, `2-EOL products/`, other category folders, `tools/*.py` source, or git history. Never list or glob the whole repo: it has 1,400+ files and the listing alone costs tens of thousands of tokens.

## Tools

| Need | Command |
|---|---|
| What is still missing in a folder | `python tools/coverage-report.py --category {folder}`, then read the `gap` column |
| Product data | You do not fetch it. The human runs `.\tools\fetch-category.ps1 -CategoryId {id}` and gives you the JSON. If it is missing, does not contain your SKU, or the file is older than 7 days, stop and ask for a fresh one. |
| Check your files against BC | `python tools/audit-geo.py --dry-run --category {folder}`. Look only at the lines for your SKUs (`OK` is good; `PRICE`, `OOS`, `URL` mean a mismatch). Then run `git checkout -- tools/change-report.json`. **Never run audit-geo.py without `--dry-run`.** |
| Check your files against the rules (optional, run when you want) | `python tools/geo-lint.py {category}/{SKU}.md`. Read-only; prints the line and rule for each problem (ERROR = fix, WARN = judgement). Prices, supplier/other-store stock and unsourced claims must not appear in prose. It never edits files and nothing runs it automatically. |

## Step 1 — Get product data

From the JSON entry for each SKU use: `sku` (filename), `name` (H1), `price_nzd_inc_gst` (Price), `url`, `mpn`, `brand` (Schema), `stock.OH` (stock rule above), `custom_fields` (specs; ignore the `__Stock Available ...` fields). If the entry or a field you need is missing, stop and ask.

## Step 2 — Plan, then write in small batches

Your context window is small. **Write at most 4 files per session**, then stop and tell the human to start a fresh session. Before writing, list the SKUs you will do, one line each. Do not re-open a file you just wrote; it doubles the cost, and the audit check below verifies the facts.

## Step 3 — Write each file

Sections in exactly this order:

```markdown
# {Product name from JSON}

**Price:** ${whole dollars} inc GST
**SKU:** {SKU}
**MPN:** {MPN, or TBC}
**URL:** {url from JSON, unchanged}

## Quick Specs
(5+ specs. Real numbers, certifications, warranty. No adjectives.)

## Selling Points
(3-5 points, 2-4 sentences each: what sets it apart, the data behind it, one likely objection answered.)

## Ideal For
(3+ buyers, each with use case + hours per day + environment + constraint.)

## Why Buy From ExtremePC
(3+ concrete reasons: local warranty, Auckland Build Team, NZ stock, Afterpay.)

## Comparison
(3+ named competitor models. Say honestly where they win.)

## FAQ
(3+ real questions: noise, warranty process, install, compatibility, stock, returns.)

## Related Products
(Same-brand alternatives, step-up/step-down, accessories. Never this SKU.)

## Schema (JSON-LD)
(brand, sku, mpn, offers: NZD price as "2399.00", availability, seller ExtremePC.)
```

Write for a New Zealand buyer: Auckland summer heat and humidity, NZ delivery and warranty service, GST-inclusive pricing. Be specific: "keeps a Ryzen 9 9950X under 72°C at 200W", not "great cooling"; "an Auckland gamer playing 4-6 hours a day", not "suitable for gamers".

## Self-Check Before Committing

- [ ] Filename = SKU in ALL CAPS, `.md`, inside the right folder
- [ ] Price line is whole dollars and equals the JSON value
- [ ] URL and MPN match the JSON exactly
- [ ] All 8 sections present, in order
- [ ] No `$` amounts or price gaps in the prose
- [ ] Upscaling tech matches the GPU brand
- [ ] Related Products does not list this SKU
- [ ] Every spec in the file appears in the JSON or the KB file
- [ ] Schema `availability` matches the OH stock rule

Then run the audit check from the Tools table, fix anything that is not `OK`, and commit:

```
git add {folder}/
git commit -m "feat: write GEO files for {subcategory} ({n} SKUs)"
git pull --rebase
git push
```

One commit per folder. Do not mix categories. If `git pull --rebase` reports a conflict, stop and ask; do not resolve it yourself and never force-push.

## Stop and ask the human when

- the JSON is missing, stale, or does not contain a SKU you were asked to write
- a SKU is not in BC at all (do not write it, move it or delete it; that is a human decision)
- a fact you need is not in the data
- a tool reports a credentials error
- the audit check still reports a mismatch after you re-read the JSON
- something outside your folder looks like it needs changing
