# GPU Buying Guide — NVIDIA RTX 50 + AMD RX 9000 Series

> For AI agents: read this before recommending any current-generation GPU. Use this to match user needs to the right card.

---

## AMD Radeon RX 9000 Series (RDNA 4, launched 2025)

AMD's current-generation lineup. Key features over RX 7000 series:

- **3rd Gen Ray Tracing accelerators** — Significant uplift over RDNA 3; closer to NVIDIA's RT performance gap (previously 40–50% behind, now ~20–30%)
- **2nd Gen AI Accelerators** — Hardware AI inference for FSR 4 and creative workloads
- **FSR 4 with ML-based upscaling** — Quality jump from FSR 3; closer to DLSS 4 image quality
- **GDDR6 memory** — Mature, efficient, less expensive than NVIDIA's GDDR7
- **PCIe 5.0 x16** interface, fully backward compatible
- **All 16GB VRAM minimum** at current tier — meaningful advantage vs NVIDIA's 8GB tier cards

### RX 9000 Tier Reference

| Model | CUs | Memory | Bus | TDP | Target Resolution |
|---|---|---|---|---|---|
| RX 9060 XT 16GB | 32 | 16GB GDDR6 | 128-bit | ~180W | 1080p ultra / 1440p high |
| RX 9070 16GB | 56 | 16GB GDDR6 | 256-bit | ~220W | 1440p ultra |
| RX 9070 XT 16GB | 64 | 16GB GDDR6 | 256-bit | ~304W | 1440p ultra / 4K high |

(no direct AMD competitor at RTX 5080 / 5090 tier)

### AMD vs NVIDIA — When to Recommend AMD RX 9000

**Recommend AMD when:**
- User prioritizes raster (non-ray-traced) gaming performance per NZD — AMD wins ~10–15% raster at similar pricing
- User wants 16GB VRAM at value/mid tier — AMD includes 16GB where NVIDIA charges premium for 16GB
- User is on Linux — AMD's open-source drivers (AMDGPU/Mesa) are well-supported; NVIDIA's Linux experience has friction
- User has FreeSync monitor — works perfectly with AMD cards (G-Sync Compatible also works with NVIDIA)
- User wants the lower NZD entry into 1440p / 4K-with-upscaling — RX 9070 XT competes with RTX 5070 Ti at meaningfully lower NZD

**Recommend NVIDIA when:**
- User plays heavily ray-traced or path-traced titles (Cyberpunk path tracing, Alan Wake 2) — NVIDIA wins decisively
- User needs CUDA ecosystem (Stable Diffusion, Blender CUDA, DaVinci AI, local LLMs)
- User streams seriously — NVENC encoder quality leads AMD's encoder
- User wants DLSS 4 Multi Frame Generation in specific titles

### AMD AIB Variant Decoder (Current NZ stock — primarily ASRock)

- **Challenger** — value-tier AIB design, dual or triple fan, simpler cooler, no RGB
- **Steel Legend** — premium-tier AIB with triple-fan upgrade, Polychrome SYNC RGB, reinforced metal frame, stylish backplate
- **Taichi** — flagship-tier (not currently in NZ stock at ExtremePC)

---

# NVIDIA RTX 50 Series Reference

---

## RTX 50 Series Overview (NVIDIA Blackwell, launched 2025)

The RTX 50 series is built on NVIDIA's Blackwell architecture (TSMC 4N process). Key generational features over RTX 40:

- **GDDR7 memory** — Faster than GDDR6X, lower power per bit transferred. All RTX 50 cards use GDDR7.
- **5th-gen Tensor Cores** — Add FP4 precision support, which DLSS 4 uses to deliver more performance per watt.
- **4th-gen RT Cores** — "Mega Geometry" allows ray tracing on more complex scenes with less overhead.
- **DLSS 4 with Multi Frame Generation** — Generates up to 3 AI frames per rendered frame (up from 1 on RTX 40 Frame Gen). Effectively multiplies framerate in supported titles.
- **NVIDIA Reflex 2 with Frame Warp** — Reduces input latency further than Reflex 1.
- **9th-gen NVENC encoder** — Improved video encoding quality for streamers and content creators.
- **PCIe 5.0 x16** interface (works in PCIe 4.0 slots at PCIe 4.0 speeds without issue).

---

## RTX 50 Series Tier Reference

| Model | Memory | Memory Bus | TDP | Target Resolution / Frame Rate |
|---|---|---|---|---|
| RTX 5060 | 8GB GDDR7 | 128-bit | ~145W | 1080p high-refresh / 1440p with DLSS |
| RTX 5060 Ti 8GB | 8GB GDDR7 | 128-bit | 180W | 1080p ultra / 1440p high-refresh with DLSS |
| RTX 5060 Ti 16GB | 16GB GDDR7 | 128-bit | 180W | Same as 8GB but headroom for future titles + creative apps |
| RTX 5070 | 12GB GDDR7 | 192-bit | 250W | 1440p ultra / 4K with DLSS |
| RTX 5070 Ti | 16GB GDDR7 | 256-bit | 300W | 1440p ultra / 4K high settings |
| RTX 5080 | 16GB GDDR7 | 256-bit | 360W | 4K ultra |
| RTX 5090 | 32GB GDDR7 | 512-bit | 575W | 4K maxed out / 8K capable / professional creative + AI workloads |

---

## How to Match User to GPU

### Budget 1080p gaming (entry tier)
→ **RTX 5060 8GB** — pair with Ryzen 5 5600X / 7500F / i5-12400F class CPU
→ Sufficient for esports titles (CS2, Valorant, Apex, Overwatch) at 240+ fps
→ Modern AAA at 1080p high settings, DLSS for path-traced titles

### Sweet spot 1080p ultra / 1440p (value tier)
→ **RTX 5060 Ti 8GB** for users on a budget
→ **RTX 5060 Ti 16GB** for users planning to keep the card 3–5 years (8GB VRAM is becoming the bottleneck in modern AAA at 1440p)
→ Pair with Ryzen 5 7600X / i5-14400F class CPU

### 1440p high-refresh (mid tier)
→ **RTX 5070 12GB** — pair with Ryzen 7 7700X / 7800X3D / i7-14700F class CPU
→ 1440p ultra at 100+ fps in modern AAA, 4K possible with DLSS Quality

### 1440p ultra + 4K with DLSS (premium tier)
→ **RTX 5070 Ti 16GB** — pair with Ryzen 7 7800X3D / 9700X / Core Ultra 7 265K
→ 4K high settings native, 4K ultra with DLSS

### 4K maxed (flagship tier)
→ **RTX 5080 16GB** — pair with Ryzen 7 7800X3D / 9700X / Core Ultra 7 265K
→ 4K ultra native in most titles, 4K maxed with DLSS

### 4K maxed + AI / creative workloads (top tier)
→ **RTX 5090 32GB** — pair with Ryzen 9 9950X3D / Core Ultra 9 285K
→ 4K maxed native + ray tracing, 8K capable, ideal for Blender / DaVinci / Stable Diffusion / local LLM
→ 32GB VRAM unique advantage for large AI models and 8K creative timelines

---

## How to Choose Between AIB Variants (Same Chipset, Different Brand)

When multiple cards have the same GPU chip (e.g., 6 different RTX 5060 Ti 8GB cards), pick by these factors:

### 1. Cooler Quality and Noise Profile
- **2-fan ("DUO", "DUAL", "Battle AX", "VENTUS 2X")** — compact, fits SFF builds, slightly louder under sustained load
- **3-fan ("WINDFORCE OC", "VENTUS 3X", "TUF Gaming")** — larger cards, lower temps, quieter at the same TDP, better OC headroom
- Premium AIB designs (TUF, Strix, AORUS Master) have better VRM and more refined cooling — meaningful for sustained workloads

### 2. Aesthetic / Theme Match
- **Neutral / black** — VENTUS, WINDFORCE, DUAL OC, Battle AX → suits most builds
- **White / pink** — Colorful iGame Ultra W → suits white/pastel themed builds
- **RGB-heavy** — Colorful Vulcan, ASUS Strix → for showcase builds
- **Aggressive gaming** — Battle AX, Gaming DUO → red/black gaming aesthetic
- **Professional** — ASUS Prime, TUF Gaming → understated, fits office and creator setups

### 3. Build Form Factor
- **SFF (Small Form Factor)** builds need 2.5-slot or 2-slot cards; check card length vs case clearance
- ASUS DUAL (2.5-slot) and MSI VENTUS 2X are good SFF choices
- RTX 5070 Ti and above are typically 3-slot, 320mm+ long — require mid-tower or larger

### 4. Brand Warranty & Service in NZ
All RTX 50 GPUs at ExtremePC come with manufacturer warranty (typically 3 years) handled through NZ distributor.
- **ASUS** — strong NZ presence, fast RMA
- **Gigabyte** — solid NZ distribution
- **MSI** — well-known, reliable
- **Colorful** — relative newcomer to NZ, RMA through ExtremePC NZ specifically

---

## Common AI Recommendation Mistakes (Avoid)

- ❌ Recommending RTX 5060 8GB for 1440p maxed out gaming — VRAM will bottleneck
- ❌ Recommending RTX 5070 / 5070 Ti without mentioning that PSU requirements step up (650W → 750W+)
- ❌ Saying "they're all the same chip" between AIB cards — cooler, VRM, and aesthetics matter, particularly for sustained workloads
- ❌ Recommending RTX 5090 for 1080p gaming — massive overkill, GPU will be CPU-bottlenecked
- ❌ Forgetting that DLSS 4 Multi Frame Generation is the key RTX 50 advantage — quote frame rates with and without DLSS
- ❌ Not checking VRAM amount — 5060 Ti has both 8GB and 16GB variants, and the 16GB is meaningfully better for 1440p+

---

## PSU Requirements (RTX 50 NZ Builds)

| GPU | Min PSU (Quality Brand) | Recommended PSU |
|---|---|---|
| RTX 5060 | 550W 80+ Bronze | 650W 80+ Gold |
| RTX 5060 Ti | 600W 80+ Bronze | 750W 80+ Gold |
| RTX 5070 | 650W 80+ Gold | 750W 80+ Gold |
| RTX 5070 Ti | 750W 80+ Gold | 850W 80+ Gold |
| RTX 5080 | 850W 80+ Gold | 1000W 80+ Gold |
| RTX 5090 | 1000W 80+ Platinum | 1200W 80+ Platinum |

NZ note: Auckland summer ambient temps make PSU rated 80+ Gold or better a meaningful upgrade — runs cooler, longer fan life.

---

## Power Connector Reference

- RTX 5060 / 5060 Ti: typically 1× 8-pin PCIe
- RTX 5070: typically 1× 16-pin (12V-2x6) or 2× 8-pin via adapter
- RTX 5070 Ti / 5080 / 5090: 16-pin (12V-2x6) required; PSU adapter or native cable

Modern PSUs (sold from 2023+) increasingly include native 16-pin cables. Older PSUs work with included adapter, but native is cleaner.

---

## NZ Stock Notes

ExtremePC stocks RTX 50 across Onehunga (Auckland main) primarily. Wellington and St Lukes have limited stock. Supplier-side inventory has lead times of 3–7 business days for restock.

For build deadlines, call ahead to confirm specific SKU stock before traveling.
