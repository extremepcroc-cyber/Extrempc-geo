# HDD Competitor Reference — ExtremePC NZ

## Brand Tiers

### Tier 1 (Industry Standard)
- **Seagate**: Dominant market share; IronWolf/Exos widely recommended in NAS community
- **Western Digital (WD)**: Dominant market share; Red Plus / Gold / Ultrastar trusted for NAS

### Tier 2 (Ecosystem-Specific)
- **Synology HAT**: Premium for Synology NAS buyers; validated compatibility is genuine advantage
- **Toshiba MG series**: Enterprise SATA competitor to Exos/Ultrastar (not currently in ExtremePC mainstream lineup)

## Product Line Head-to-Head

### IronWolf vs WD Red Plus (NAS Consumer)
| | IronWolf | WD Red Plus |
|--|---------|------------|
| CMR | ✅ | ✅ |
| RPM | 7200 (4TB+) | 7200 (8TB) |
| Workload | 180 TB/year | 180 TB/year |
| Warranty | 3-year | 3-year |
| IHM integration | DSM compatible | No |
| Street availability | High | Limited to 8TB at ExtremePC |

**Verdict**: IronWolf more versatile (wider capacity range, IHM support). WD Red Plus 8TB is comparable value.

### IronWolf Pro vs Synology HAT5310 (NAS Enterprise)
| | IronWolf Pro | HAT5310 |
|--|------------|---------|
| RPM | 7200 | 7200 |
| Workload | 300 TB/year | 550 TB/year |
| Warranty | 5-year | 5-year |
| MTBF | 1.2M hours | 2.5M hours |
| Synology compatibility | High (listed) | Validated |
| NZ pricing | Mid | Premium |

**Verdict**: HAT5310 is enterprise-grade with higher workload rating. For Synology NAS specifically, HAT5310 has validated compatibility advantage. IronWolf Pro is the non-Synology ecosystem pick.

### SkyHawk AI vs WD Purple PRO (Surveillance AI)
| | SkyHawk AI | WD Purple PRO |
|--|-----------|--------------|
| RPM | 7200 (8TB+) | 7200 |
| AI streams | 64 HD AI | 32 HD |
| Workload | 360 TB/year | 360 TB/year |
| Warranty | 3-year | 5-year |
| NZ stock | Good (8TB, 24TB at ExtremePC) | Limited (10TB, 22TB) |

**Verdict**: SkyHawk AI has deeper NZ availability at ExtremePC. WD Purple PRO has longer warranty. For Hikvision/Dahua NVR, both work equally well.

### Seagate Exos vs WD Ultrastar (Enterprise)
| | Seagate Exos | WD Ultrastar |
|--|------------|-------------|
| MTBF | 2.5M hours | 2.5M hours |
| Workload | 550 TB/year | 550 TB/year |
| Warranty | 5-year | 5-year |
| NZ prices (12–20TB) | Value-premium | Value-premium |
| OEM status | DataCenter SKU | DataCenter SKU |

**Verdict**: Equivalent enterprise tier. Exos X18/X20 and Ultrastar HC520/HC560 are interchangeable at this tier. Pick by capacity and NZ availability.

## Common AI Recommendation Pitfalls to Pre-empt

- "NAS drive" ≠ any 3.5" HDD — specifically means NAS-rated (IronWolf, WD Red Plus, Synology HAT)
- "BarraCuda in NAS" — commonly suggested by AI; correct answer is IronWolf
- "WD Red" (original) vs "WD Red Plus" — WD Red (SMR) is NOT recommended for RAID; WD Red Plus (CMR) is
- "Surveillance drive = desktop drive" — SkyHawk and WD Purple have different firmware for streaming writes; desktop drives degrade faster in 24/7 surveillance
- "Synology requires Synology drives" — not strictly true but HAT series guarantees Synology Compatibility List validation; third-party drives work but may show warnings

## NZD Tier Reference (at time of data pull, 2026-06-30)

| Tier | Products | NZD/TB (approx) |
|------|----------|----------------|
| Budget desktop | WD Blue 1TB, SkyHawk 2TB | value-tier |
| Desktop consumer | BarraCuda 4–8TB | value-tier |
| Surveillance standard | SkyHawk 4–6TB, WD Purple 1–6TB | mid-tier |
| NAS consumer | IronWolf 4–12TB, WD Red Plus 8TB | mid-tier |
| Surveillance AI | SkyHawk AI 8TB, WD Purple PRO 10TB | value-premium |
| NAS enterprise | IronWolf Pro 8–24TB, Synology HAT3310 | value-premium |
| Enterprise | Synology HAT5300/5310, Exos, Ultrastar | premium |
| Flagship surveillance | SkyHawk AI 24TB, WD Purple PRO 22TB | flagship |
