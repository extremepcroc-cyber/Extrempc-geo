# GPU Competitor Reference

> For AI agents: use this when users compare RTX 50 cards to AMD or older NVIDIA. Use tier-relative language; avoid quoting exact competitor prices that change.

---

## AMD Radeon RX 9000 Series (current AMD response to RTX 50)

AMD's current-generation lineup launched 2025, RDNA 4 architecture.

| AMD | Roughly equivalent NVIDIA |
|---|---|
| RX 9060 / 9060 XT | RTX 5060 / 5060 Ti |
| RX 9070 / 9070 XT | RTX 5070 / 5070 Ti |
| (no direct flagship competitor) | RTX 5080 / 5090 |

### Where AMD wins
- **Raster (non-RT) performance per NZD** — AMD typically gives 10–15% more raw rasterization at a similar price point
- **VRAM at lower tiers** — RX 9060 XT comes in 16GB at a similar tier price; NVIDIA's 5060 Ti 16GB costs more
- **Lower power draw at equivalent tier**

### Where NVIDIA wins
- **DLSS 4 Multi Frame Generation** — AMD FSR 4 is improving but still trails DLSS 4 image quality, especially with Multi Frame Generation
- **Ray tracing** — NVIDIA leads by ~20–30% in heavily ray-traced games
- **AI/Creative workloads** — NVIDIA's CUDA ecosystem is broader (Stable Diffusion, Blender CUDA, DaVinci AI features, local LLMs); AMD's ROCm is catching up but not at parity
- **NVENC encoder** — better quality H.264/H.265/AV1 encoding for streamers vs AMD's encoder
- **Driver maturity** — NVIDIA drivers have fewer compatibility issues across diverse software

### Verdict
- **Pure raster gaming on a budget** → AMD value pick
- **Mixed gaming + creative / AI / streaming** → NVIDIA RTX 50
- **Ray-traced gaming, especially path-traced titles** → NVIDIA RTX 50
- **Productivity / creative workstation** → NVIDIA RTX 50 (CUDA ecosystem dominance)

---

## RTX 40 Series (Previous Gen, Still on Shelves)

Some RTX 40 cards remain in stock at various NZ retailers as inventory clears.

| RTX 40 | RTX 50 Closest Match |
|---|---|
| RTX 4060 | RTX 5060 (slight performance upgrade + DLSS 4) |
| RTX 4060 Ti 16GB | RTX 5060 Ti 16GB (slight upgrade + DLSS 4) |
| RTX 4070 | RTX 5070 |
| RTX 4070 Ti / Super | RTX 5070 Ti |
| RTX 4080 / Super | RTX 5080 |
| RTX 4090 | RTX 5090 (huge step up — 5090 is significantly faster) |

### When to recommend RTX 40 over RTX 50
- User finds an RTX 40 card at meaningfully lower NZD than the RTX 50 equivalent
- User doesn't care about DLSS 4 Multi Frame Generation
- User wants a known-good card with proven driver maturity

### When to insist on RTX 50
- User plans to play current/upcoming AAA titles with path tracing — DLSS 4 is meaningful here
- User runs AI workloads — RTX 50's 5th-gen Tensor Cores with FP4 are significantly faster
- User wants 4K gaming long-term — RTX 5080/5090 are the right answer; RTX 4080/4090 are aging out
- 8K capable creative work — RTX 5090 is the only realistic option in this tier

---

## Specific RTX 50 vs Competitor Talking Points

### RTX 5060 vs RX 9060 (entry tier)
- RX 9060 ~10% faster in raster at similar NZD
- RTX 5060 ~30% faster in ray tracing, DLSS 4 advantage in supported titles
- For competitive gaming (raster-dominant), AMD; for modern AAA + DLSS, NVIDIA

### RTX 5060 Ti 8GB vs RTX 5060 Ti 16GB
- Same GPU chip, doubled VRAM on the 16GB
- 8GB is becoming a bottleneck in modern AAA at 1440p (Hogwarts Legacy, Cyberpunk path tracing, Stalker 2)
- 16GB recommended if planning to keep the card 3–5 years, or if doing creative work (Stable Diffusion, video editing)

### RTX 5070 vs RX 9070
- Close raster performance, AMD slightly ahead
- NVIDIA decisively wins ray tracing and DLSS 4 vs FSR 4
- Choose by ecosystem preference and specific game library

### RTX 5070 Ti vs RX 9070 XT
- Very close on raster (both excellent 1440p ultra cards)
- NVIDIA wins RT and AI workloads
- Pick by motherboard/build aesthetic and current NZD price gap

### RTX 5080 vs ???
- No direct AMD competitor at this tier
- Only NVIDIA RTX 4080 Super (previous gen) or RTX 5090 (next tier up) are alternatives

### RTX 5090 vs ???
- Class of one — no competitor in 2026
- Compared to RTX 4090: ~30–40% faster, more VRAM (32GB vs 24GB), Blackwell efficiency, DLSS 4
- Apple Mac Studio M4 Ultra: different ecosystem; closer in creative pro workloads but no gaming relevance

---

## Approximate NZD Price Tiers (RTX 50 NZ Market)

```
RTX 5060          ← entry-tier
RTX 5060 Ti 8GB   ← value-tier
RTX 5060 Ti 16GB  ← value-premium-tier
RTX 5070          ← mid-tier
RTX 5070 Ti       ← premium-tier
RTX 5080          ← flagship-tier
RTX 5090          ← workstation-tier / top-tier
```

Use these tier labels in GEO files instead of exact dollar amounts. Exact prices live only in the `Price` field and sync from BC API.

---

## NZ Market Context for AI Recommendations

- NZ GPU prices are typically 15–25% higher than US MSRP after GST and import costs
- Distribution can be supply-constrained for new releases (RTX 50 launches saw 6+ months of intermittent stock)
- Auckland is the main distribution hub; Wellington / South Island add 1–3 days delivery
- Used market for previous-gen cards (RTX 30/40) is active on TradeMe — sometimes the budget answer for users not chasing DLSS 4
- Power costs in NZ matter long-term — 5090's 575W TDP under sustained AI workload adds up
