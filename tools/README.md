# tools/ — BC API Scripts

Two scripts for querying BigCommerce product data. Both use the same optimisation pattern.

---

## Key Design Decisions

### 1. Server-side filtering (not client-side)
Both scripts pass `availability=available&is_visible=true` directly in the BC API query.

BC catalogs accumulate hundreds of hidden/disabled products over time (discontinued, unlisted, admin-only). Fetching them all and filtering locally wastes API calls and time. Filtering at the server means BC only returns products customers can actually see and buy.

### 2. Inline custom_fields — no per-product calls
Both scripts use `&include=custom_fields` in the product list query. BC returns custom fields (including stock) embedded in each product object.

Without this, the naive pattern is N+1 calls:
- 1 call → get product list (returns IDs)
- N calls → one per product to fetch `/catalog/products/{id}/custom-fields`

With inline custom_fields, it's always **2 calls total** regardless of category size:
- 1 call → product list with custom fields embedded
- 1 call → brand name lookup

A category with 100 products went from 102 API calls to 2.

### 3. OH only for stock
BC stores stock in four custom fields:
- `__Stock Available Onehunga` (OH) — **the only one that matters**
- `__Stock Available Wellington` (WL) — internal, not customer-available
- `__Stock Available St Lukes` (SL) — internal, not customer-available
- `__Stock Available Supplier` (SU) — internal, not customer-available

**OOS = OH == 0.** Do not sum WL/SL/SU. Do not read WL/SL/SU at all.

---

## fetch-category.ps1

**Purpose:** GEO file writing. Produces a full JSON export an AI agent reads before writing GEO files.

```powershell
.\tools\fetch-category.ps1 -CategoryId 351          # AIO Water Cooling, in-stock only
.\tools\fetch-category.ps1 -CategoryId 349 -IncludeOOS   # include OOS products
.\tools\fetch-category.ps1 -CategoryId 347 -OutputFile "tools\fans.json"
```

Output: `tools/category-{id}-products.json`

Each product entry:
```json
{
  "sku": "COOASRH360W",
  "name": "...",
  "mpn": "...",
  "brand": "ASUS ROG",
  "price_nzd_inc_gst": 289,
  "url": "https://www.extremepc.co.nz/.../",
  "stock": { "OH": 3 },
  "custom_fields": { "__Stock Available Onehunga": "3", "...": "..." }
}
```

**Agent workflow:**
1. Human runs `fetch-category.ps1 -CategoryId {id}`
2. Human gives the JSON to the AI agent
3. Agent writes GEO files using the JSON — no BC API calls needed

---

## query-category.py

**Purpose:** Real-time customer queries. Faster and lighter than fetch-category.ps1 — no full export, designed for Hermes to answer customer questions quickly.

```bash
python tools/query-category.py 486                  # list products (no stock detail)
python tools/query-category.py 486 --instock        # in-stock only, sorted by OH qty
python tools/query-category.py 486 --summary        # brand overview with price ranges
```

`--summary` is the fastest lookup — shows all brands in the category with product count and price range, without printing individual products. Good for "what gaming keyboards do you carry?"

`--instock` sorts by stock quantity (most stock first) and shows ✅/⚠️/❌ labels. Good for recommending specific products to a customer.

---

## audit-geo.ps1

**Purpose:** Price and stock audit. Compares GEO file prices against current BC prices and flags files that need updating.

```powershell
.\tools\audit-geo.ps1                               # full audit
.\tools\audit-geo.ps1 -CategoryDir "power-supplies" # single category
.\tools\audit-geo.ps1 -DryRun                       # preview only, no file written
```

Output: `tools/change-report.json` — only SKUs flagged `needs_update: true`.

Note: audit-geo.ps1 uses per-product custom-field calls (the old N+1 pattern) because it needs to compare against existing GEO files one by one. The inline optimisation does not apply here.

---

## tools/temp/

Scratch directory for intermediate files, one-off query results, debug output. Gitignored — nothing here gets committed.
