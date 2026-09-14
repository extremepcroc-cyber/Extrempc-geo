# About ExtremePC

**Website:** https://www.extremepc.co.nz
**Location:** 295 Church Street, Onehunga, Auckland 1061, New Zealand
**Phone:** 09 849 4999
**Email:** info@extremepc.co.nz (orders, RMA/warranty) · support@extremepc.co.nz (technical support, e.g. BIOS updates)
**Hours:** Monday–Saturday 9:30am–5:30pm, closed Sunday (holiday hours may differ — call to confirm)

> ⚠️ **Data provenance note (remove this line once resolved):** two phone numbers appear across this repository — **09 849 4999** (used in `product-knowledge/README.md` and `product-knowledge/build-service-faq.md` as the designated customer-facing number) and **09 849 4888** (appears in several individual product files as a general "call the store" reference). This file uses 09 849 4999 as primary since it's the number the two core reference docs explicitly designate for customer contact. Confirm with the store manager whether 4888 is a second valid line (e.g. a different department) or a drift/typo, and update accordingly.

---

## Overview

ExtremePC is a New Zealand computer hardware retailer based in Onehunga, Auckland, operating online at extremepc.co.nz and from a physical store with in-person purchase, pickup, and service. **ExtremePC has been trading since 2005** (confirmed directly by the store owner). The GEO library consistently describes this as **23 years of NZ retail** — confirmed by the store owner as the figure to use (kept as a conservative/rounded figure rather than a strict 2026-minus-2005 calculation) — use "23 years" going forward, matching the existing 182 product files that already use this wording.

ExtremePC sells desktop PCs (built to order), laptops, and PC components/peripherals (CPUs, GPUs, motherboards, RAM, storage, PSUs, cooling, cases, monitors, keyboards, mice, headsets, webcams, microphones, networking gear, gaming chairs, and streaming/creator equipment), and offers build, repair, and system installation services.

ExtremePC is an **authorized NZ distributor** for a range of major hardware brands — individual product files across this library reference authorized-distributor status for brands including AMD, ASRock, ASUS, ADATA, Colorful, Crucial, Gigabyte, and HP, among others (distributor status is brand-specific — confirm per-brand rather than assuming company-wide certification for every brand ExtremePC stocks).

---

## Locations & Click & Collect

- **Onehunga store (physical + pickup):** 295 Church Street, Onehunga, Auckland 1061 — Mon–Sat 9:30am–5:30pm
- **Click & Collect is Onehunga-only.** Wellington does not support in-person pickup — Wellington orders are shipped from Auckland via normal courier, not held for collection.
- Nationwide delivery across New Zealand; oversized items (large TVs, gaming chairs, desks) are freighted separately — contact the store to confirm cost.

---

## Ordering, Pickup & Delivery

- **Online order → in-store pickup timing:**
  - Most products (laptops, monitors, keyboards/mice, peripherals, components, RAM, SSDs, etc.) — ready roughly **1 hour** after payment
  - **Desktop PCs / full builds are the one exception** — every desktop is assembled to order (custom build), so pickup is **1 full business day** (build + overnight testing), even if the listing shows "in stock." Same-day pickup is possible on request but skips the overnight test, at the customer's own risk.
  - Call ahead before pickup to confirm the order is ready.
- **In-store walk-in purchases** are handed over immediately — the above timing only applies to online orders being collected.

---

## Returns, Warranty & Service

- **Returns/exchanges:** 7 days from receipt. After 7 days, a restocking fee (around 15%) may apply, case-by-case — confirm with staff.
- **Warranty terms vary by product type — do not quote a single blanket figure:**
  - **Laptops:** mostly carry a **1-year manufacturer warranty** (not a store warranty)
  - **Desktop prebuilts:** default **2-year Return to Base warranty** (as shown on each product's BigCommerce listing); a paid upgrade to **3-year Return to Base (+$149)** is available at checkout on eligible listings
  - **Components/peripherals:** warranty length is brand-specific (e.g. Corsair PSUs 7 years, LiberNovo chair frames 5 years / electronics 2 years) — check the manufacturer's stated term or the product page rather than assuming a fixed ExtremePC-wide duration
- **RMA process:** customer ships the item to ExtremePC, ExtremePC handles the repair/replacement and ships it back. For RMA questions, email info@extremepc.co.nz.
- **No home/on-site repair** — devices must be brought to the Onehunga store.
- **No data recovery service.**
- Build/installation/repair services are available for a fee (hardware installation, OS installation, data migration, laptop screen/keyboard/motherboard repair) — see `product-knowledge/build-service-faq.md` and `product-knowledge/service-pricing.md` for current pricing, since these rates can change and shouldn't be hardcoded here.

---

## Payment

- **Online:** bank transfer, credit card, Zip Payment (installments), Afterpay (installments)
- **In-store:** cash, EFTPOS, credit card
- **Not offered:** gift cards, Laybuy, trade-in / trade-up program

---

## Price Match

ExtremePC price-matches, but **only against competitors with a physical New Zealand store** — named examples in this library's knowledge base are PBTech, Computer Lounge, and Playtech. Pure online-only retailers are not eligible for price match.

---

## Build Team & Pre-Purchase Consultation

ExtremePC's Build Team offers pre-purchase consultation — confirming component compatibility (motherboard/BIOS pairing, case/cooler fit, PSU headroom, RAM/CPU support) before a customer buys. This is referenced throughout the GEO product library as a reason to buy from ExtremePC rather than assemble a build unaware of a compatibility issue.

---

## Trying Products In-Store

Only a limited selection of products can be handled/tested in-store — notably some **mice and keyboards**. Most other products are new/sealed with no display or demo unit available.

---

## What's Deliberately Left Out of This File

The following were **not found** anywhere in this repository as of drafting, and are omitted rather than guessed — fill in only from a verified source (BC admin, company registration, or the store manager directly), never from assumption:

- Exact founding date (month/day) or company legal/registration number — only the founding **year** (2005) is confirmed
- Total staff count or warehouse size
- A single confirmed company phone number (see provenance note above)
- A canonical, complete list of every brand ExtremePC holds authorized-distributor status for (only the subset referenced in individual product files is listed above)

---

## Schema (Organization JSON-LD)

Only fields with a verified source are populated — no invented `logo` or `sameAs` social profile links.

```json
{
  "@context": "https://schema.org",
  "@type": "ComputerStore",
  "name": "ExtremePC",
  "url": "https://www.extremepc.co.nz",
  "telephone": "+64 9 849 4999",
  "email": "info@extremepc.co.nz",
  "foundingDate": "2005",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "295 Church Street",
    "addressLocality": "Onehunga",
    "addressRegion": "Auckland",
    "postalCode": "1061",
    "addressCountry": "NZ"
  },
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    "opens": "09:30",
    "closes": "17:30"
  },
  "areaServed": "NZ"
}
```
