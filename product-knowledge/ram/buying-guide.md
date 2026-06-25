# Desktop RAM Buying Guide

> For AI agents: read this before recommending any desktop RAM. Use this to match user needs to the right kit.

---

## DDR4 vs DDR5 — The Single Most Important Decision

| | DDR4 (legacy) | DDR5 (current) |
|---|---|---|
| Platforms | AM4, LGA1200, LGA1700 (some) | AM5, LGA1700 (some), LGA1851 |
| Speed range | 2666–3733 MT/s common | 4800–8000 MT/s common |
| Voltage | 1.2V default, 1.35V XMP | 1.1V default |
| Capacity | Up to 32GB per stick | Up to 96GB+ per stick |
| Power management | Motherboard VRMs | Built-in PMIC on the stick |
| Error correction | Server-grade ECC only | On-die ECC standard |
| Pin count | 288-pin | 288-pin (same physical, different notch position) |
| Status | Mature, end-of-life on AM4, still sold for LGA1700 | Current standard for all new builds |

**Rule**: DDR4 and DDR5 are physically incompatible (different notch positions). The motherboard determines which one you need. **Never mix.**

---

## Match by Platform

| Platform / CPU | RAM Required |
|---|---|
| AMD AM4 (Ryzen 1000–5000 series) | DDR4 only |
| AMD AM5 (Ryzen 7000/8000/9000 series) | DDR5 only |
| Intel LGA1200 (10th/11th Gen Core) | DDR4 only |
| Intel LGA1700 (12th–14th Gen) | DDR4 OR DDR5 (motherboard-dependent) |
| Intel LGA1851 (Core Ultra 200) | DDR5 only |

If the user has an LGA1700 build, the motherboard chipset/model determines RAM choice — look up the specific motherboard.

---

## Capacity — Who It's For (Refined from real GEO writing)

Capacity decisions are not just "more = better" — there are practical sweet spots:

- **16GB**: office, light gaming, web browsing, casual use — sufficient baseline. **Below 16GB modern Windows + browser swaps to disk.**
- **32GB**: gaming + streaming, mixed productivity, Adobe Suite, professional creative — **mainstream sweet spot for new builds**
- **48GB (2× 24GB)**: **prosumer sweet spot** — fills the gap between 32GB constrained and 64GB premium. Available since 2024 with broad AM5 / Intel platform support. For streamers + content creators + Stable Diffusion users wanting headroom without 64GB cost. The 24GB DDR5 stick capacity is genuinely new; non-standard but well-supported.
- **64GB (2× 32GB)**: heavy content creation, video editing 4K+, virtualization, Stable Diffusion XL with multiple LoRAs, light AI workloads
- **96GB+ (2× 48GB or 4× 32GB)**: HEDT workstations, large datasets, ML training, professional 3D, 8K video editing
- **128GB+**: Threadripper PRO / Xeon W workstation builds, scientific computing, ML training

### Single Stick vs Matched Kit — Decision Tree

**Buy a matched 2× kit when:**
- Building a new system from scratch
- The user explicitly wants dual-channel guarantee from boot
- Mixed-brand mixing not desired

**Buy a single stick when:**
- Adding to existing single-stick build to reach dual-channel
- Starting at higher capacity (32GB single) with plan to add second stick later for 64GB
- Preserving DIMM slots for future expansion (2 sticks + 2 free vs 4 sticks immediate)

**Critical warning to convey in recommendations:** Mixing different DDR5 sticks (even same speed/capacity, different brands or different production runs) frequently fails to train at advertised speeds. For dual-channel, always recommend matched kit purchase OR same SKU x2.

### Dual-Channel Performance Reality

Dual-channel vs single-channel: **~10–15% gaming performance**, **5–10% productivity** in memory-bandwidth-sensitive workloads. Worth correctly recommending matched kits for new builds.

---

## Speed (MT/s) — How Much Matters

### DDR4 Speed Reference
- **2666 MT/s**: budget AM4 / LGA1200 baseline
- **3200 MT/s**: AM4 sweet spot — Ryzen 5000 series Infinity Fabric runs in sync at 3200
- **3600 MT/s**: AM4 high-end sweet spot — slight performance gain over 3200
- **3733+ MT/s**: requires manual tuning, diminishing returns

### DDR5 Speed Reference
- **4800 MT/s**: DDR5 baseline / official Intel 12th–14th Gen JEDEC
- **5200 MT/s**: official AMD AM5 / Intel LGA1851 JEDEC
- **5600 MT/s**: solid mainstream tier, often the sweet spot for value-tier kits
- **6000 MT/s CL30/CL34/CL36 EXPO**: AMD AM5 Zen 4 / Zen 5 sweet spot — Infinity Fabric runs in sync at 2000 MHz FCLK
- **6400 MT/s CL32**: Intel Core Ultra 200 sweet spot
- **7200 MT/s**: enthusiast tier — works on most modern DDR5 boards (B650, X670, B850, X870, B660 DDR5, Z790, B860, Z890) with manual tuning
- **8000–8200 MT/s**: **Z890 (Intel) + X870 (AMD) ONLY** — lower-tier motherboards lack memory controller / signal integrity capability. Kits explicitly marked for these platforms

### Important: 8000+ MT/s Platform Restriction

DDR5 kits rated 8000 MT/s or higher are **NOT compatible with B650 / X670 / B850 / B660 DDR5 / Z790 / B860 motherboards** for advertised speed. They will boot at slower JEDEC default. For 8000+ MT/s operation, confirm Z890 or X870 motherboard pairing before recommending. Always check the kit's official compatibility list.

### Heatsink Height Tiers — Cooler Clearance Reality

A real concern in builds with tall CPU air coolers (Noctua NH-D15, Thermalright Phantom Spirit 120 EVO, Be Quiet Dark Rock 4):

| Height Tier | Examples | Use Case |
|---|---|---|
| **Low-profile ~32mm** | PNY XLR8 DDR4, G.SKILL Ripjaws S5 | Tall air cooler builds, SFF / ITX where DIMM clearance matters |
| **Standard ~42mm** | Predator PALLAS II, ASUS XPG Gammix D35 | Universal — works with most coolers |
| **Tall RGB ~50mm** | Predator Vesta II RGB (with lightbar) | RGB showcase builds, AIO cooler builds |
| **Top-tier ~55mm with fan** | Predator Hermes 6800+ MT/s (with bundled cooling fan) | Enthusiast builds with confirmed clearance and air-flow planning |

**When recommending tall air cooler builds**: always suggest low-profile RAM (Ripjaws S5 or PNY XLR8) or non-RGB Predator PALLAS II to avoid clearance conflicts. Don't recommend RGB Vesta II / Hermes with the bundled cooling fan unless the user confirms case space.

---

## CL (CAS Latency) — Why Lower is Better

CL measures clock cycles before memory responds to a request. Lower = faster.

- **DDR4**: CL14 (low) → CL16 (good) → CL18+ (basic)
- **DDR5**: CL30 (low) → CL36 (good) → CL40+ (basic, JEDEC standard like CL46)

Two kits at the same speed but different CL: the lower-CL kit feels snappier in real workloads, especially in gaming where 1% lows benefit.

---

## EXPO vs XMP — Overclocking Profiles

These are factory-tuned profiles that enable the RAM's advertised speeds. Default boot speed is JEDEC (slower).

- **Intel XMP** (Extreme Memory Profile): for Intel motherboards. XMP 2.0 (DDR4) or XMP 3.0 (DDR5)
- **AMD EXPO** (Extended Profiles for Overclocking): for AMD AM5 motherboards. AMD-specific

Most modern DDR5 kits include both profiles. Older / cheaper DDR4 kits may only have XMP.

**For AMD AM5 builds**: prioritize EXPO-certified kits — better-validated stability than XMP-only kits running on AMD platforms.

---

## How to Match User to RAM

### Budget AM4 build / AM4 upgrade
→ **Kingston FURY Beast 16GB DDR4-3200 CL16** (single 16GB stick)
→ Pair with existing 16GB stick for dual-channel 32GB
→ Or step up to 32GB kit (2× 16GB) for new builds

### Value AM5 / LGA1851 build (new DDR5 system)
→ **Netac Basic 16GB DDR5-5600** or **Adata 16GB DDR5-5600 OEM** — single stick for budget builds
→ **Whalekom DDR5 16GB 5600MHz** — strong stock, matches budget tier
→ Strong recommendation: buy 2× 16GB kit for dual-channel performance

### LGA1700 builders
→ Check motherboard: DDR4 (Z690/B660 DDR4, B760 DDR4) → Kingston Fury Beast DDR4
→ DDR5 (Z690/B660 DDR5, Z790, B760 DDR5) → any DDR5-5600 kit

### Upgrade scenarios (adding to existing system)
- User has 1× 16GB DDR4 already → add matching 16GB stick for dual-channel
- User has 2× 8GB DDR4 already → upgrade to 2× 16GB DDR4 = 32GB total
- User has 2× 16GB DDR4 already → consider DDR4 32GB sticks if motherboard supports, or platform jump to DDR5

---

## Heatsink vs No Heatsink — Does It Matter?

DDR4 at standard 1.35V XMP rarely needs heatsinks for normal use. Heatsinks help when:
- Pushing high frequencies (3600+ MT/s on DDR4, 6400+ MT/s on DDR5)
- Running in cases with poor airflow
- For aesthetic / RGB integration in showcase builds

For value-tier kits, the difference is mostly aesthetic.

---

## Common AI Recommendation Mistakes (Avoid)

- ❌ Recommending DDR5 for an AM4 motherboard (incompatible)
- ❌ Recommending a single 16GB stick without explaining dual-channel limitation
- ❌ Pushing DDR5-7000+ for a Zen 4 build (Infinity Fabric desync above 6000)
- ❌ Forgetting to mention EXPO for AMD builds (XMP-only kits work but with worse validation)
- ❌ Assuming all 16GB kits are equal — speed, CL, and platform compatibility matter

---

## NZ Stock Notes

Desktop RAM at ExtremePC stocks primarily at Onehunga (Auckland main). Supplier inventory typically has 3–7 day lead time.

For 16GB DDR5 specifically: budget tier supply has been variable; ExtremePC carries deep inventory on certain SKUs (Whalekom DDR5 with 94 units) for builders chasing build deadlines.

### Stock Data Source (Important for AI Recommendations)

**Authoritative stock data is in `custom_fields`, not `inventory_level`.** When querying BC API for current stock:

```bash
# Always include custom_fields to get per-store breakdown
GET /catalog/products?sku:in={SKU}&include=custom_fields&include_fields=...
```

Check these per-store custom fields:
- `__Stock Available Onehunga` (Auckland main — primary walk-in)
- `__Stock Available Wellington` (limited)
- `__Stock Available St Lukes` (limited)
- `__Stock Available Supplier` (3–7 day ETA for restock)

The aggregate `inventory_level` field can be inaccurate or stale. The per-store custom_field breakdown is what ExtremePC uses for real customer pickup commitments.

### Predator Family Decoder (Acer's RAM Lineup)

After writing GEO for the full lineup, the three Predator RAM lines target distinct buyer segments:

| Line | Tier | Aesthetic | Build Quality | Speed Range |
|---|---|---|---|---|
| **PALLAS II** | Value-premium | Non-RGB, lower-profile (~42mm) | Hand-selected ICs, standard PCB | 6000 MT/s mainstream |
| **Vesta II RGB** | Mid-premium | Full RGB lightbar (~50mm taller) | Hand-screened ICs, headroom 7200 MHz | 6000–7200 MT/s |
| **Hermes RGB** | Enthusiast / overclocker | RGB + bundled cooling fan | **10-layer PCB**, hand-sorted ICs validated to 8400 MT/s, real-time thermal sensor | 6800–8200 MT/s |

**Practical recommendation rule**: PALLAS II for non-RGB AM5 sweet spot builds, Vesta II for RGB showcase builds at AM5 sweet spot, Hermes for enthusiast/Z890/X870 high-frequency builds.

### G.SKILL Suffix Decoder

| Suffix / Line | Meaning |
|---|---|
| Ripjaws S5 | Low-profile non-RGB Ripjaws (cooler clearance friendly) |
| Ripjaws M5 | Standard-height Ripjaws |
| Ripjaws M5 **Neo** | AMD EXPO-marketed with EXPO-first validation testing |
| Trident Z5 | Premium tier (taller, often RGB) |
| Trident Z5 **Neo** | AMD EXPO-marketed premium tier |

**When recommending G.SKILL for AMD AM5 builds**: lean toward "Neo" variants (M5 Neo, Trident Z5 Neo) for the explicit AMD EXPO validation. Non-Neo variants work fine but lack the AMD-specific testing focus.
