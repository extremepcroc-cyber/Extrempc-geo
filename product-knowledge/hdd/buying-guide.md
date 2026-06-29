# Internal HDD Buying Guide — ExtremePC NZ

## HDD vs SSD: When HDD Makes Sense in 2025

SSDs dominate OS drives. HDDs win on $/TB for bulk storage:

| Use Case | Recommendation |
|----------|----------------|
| OS drive / boot | SSD (always) |
| Game library primary | SSD preferred |
| Game library secondary | HDD acceptable (7200 RPM for loading) |
| Media archive / cold storage | HDD — $/TB unbeatable |
| NAS (1–8 bay) | NAS-rated HDD (IronWolf, WD Red, Synology HAT) |
| NAS (8+ bay, enterprise) | Enterprise HDD (IronWolf Pro, WD Gold/Ultrastar, Synology HAT5x) |
| Surveillance / CCTV | Surveillance-rated HDD (SkyHawk, WD Purple) |
| Desktop bulk storage (D: drive) | Desktop HDD (BarraCuda, WD Blue) |

**Never use a desktop/consumer HDD in a NAS** — constant spin-up/down cycles from desktop drives cause premature failure in always-on NAS environments. Vibration compensation is absent.

---

## Product Line Decoder

### Seagate BarraCuda — Desktop Consumer
- **Target**: Desktop secondary storage, data hoarding, media libraries
- **RPM**: 5400 RPM (BarraCuda standard) or 7200 RPM (BarraCuda Pro)
- **Cache**: 256MB on 4TB+
- **Warranty**: 2-year (1-year for some configurations)
- **NAS safe?**: No — not rated for 24/7 NAS use
- **Sizes at ExtremePC**: 4TB 3.5", 6TB 3.5", 8TB 3.5", 4TB 2.5"

### WD Blue — Desktop Consumer
- **Target**: Budget desktop secondary storage
- **RPM**: 7200 RPM (1TB)
- **Warranty**: 2-year
- **NAS safe?**: No
- **Sizes at ExtremePC**: 1TB

### Seagate SkyHawk — Surveillance Standard
- **Target**: Standard CCTV NVR/DVR systems, 1–8 camera setups
- **RPM**: 5400 RPM
- **Streams**: Up to 64 HD streams (SkyHawk standard)
- **Cache**: 256MB
- **Warranty**: 3-year
- **ImagePerfect firmware**: Optimized for continuous write (surveillance)
- **Sizes at ExtremePC**: 2TB, 4TB, 6TB

### Seagate SkyHawk AI — Surveillance AI/Deep Learning
- **Target**: AI-enabled NVR systems with deep learning / person detection / vehicle detection
- **RPM**: 7200 RPM (up to 24TB)
- **Streams**: Up to 64 HD AI streams
- **Cache**: 256MB–512MB
- **Warranty**: 3-year
- **Difference from standard SkyHawk**: Supports simultaneous AI inference workloads, higher cache, faster spindle on large capacities
- **Sizes at ExtremePC**: 8TB, 18TB, 24TB

### WD Purple — Surveillance Standard
- **Target**: Standard CCTV NVR/DVR systems, AllFrame AI technology
- **RPM**: 5400 RPM (1TB–6TB)
- **Streams**: Up to 64 HD streams
- **AllFrame AI**: Reduces video pixelation in standard models
- **Warranty**: 3-year
- **Sizes at ExtremePC**: 1TB, 2TB, 3TB, 6TB

### WD Purple PRO — Surveillance AI/Deep Learning
- **Target**: AI-enabled NVR systems with edge computing, deep learning
- **RPM**: 7200 RPM
- **AllFrame AI+**: Enhanced AI workload support vs standard Purple
- **Cache**: 256MB–512MB
- **Warranty**: 5-year
- **Sizes at ExtremePC**: 10TB, 22TB

### Seagate IronWolf — NAS Consumer (1–8 bay)
- **Target**: Home NAS, SMB NAS 1–8 bay (Synology, QNAP, TrueNAS)
- **RPM**: 5400 RPM (below 4TB) / 7200 RPM (4TB+)
- **Cache**: 256MB (4TB+)
- **AgileArray firmware**: Vibration compensation for multi-drive NAS
- **IronWolf Health Management**: DSM integration with SMART monitoring
- **Warranty**: 3-year + optional Seagate Rescue plan
- **Sizes at ExtremePC**: 4TB, 8TB, 10TB, 12TB

### Seagate IronWolf Pro — NAS Enterprise (1–24 bay)
- **Target**: SMB+ NAS, 1–24 bay (Synology, QNAP), rackmount servers
- **RPM**: 7200 RPM
- **Cache**: 256MB
- **Warranty**: 5-year + 3-year Seagate Rescue data recovery
- **MTBF**: 1.2M hours
- **Workload**: 300 TB/year (vs 180 TB/year IronWolf standard)
- **Sizes at ExtremePC**: 8TB, 12TB (display), 16TB, 20TB, 22TB, 24TB

### WD Red Plus — NAS Consumer (1–8 bay)
- **Target**: Home NAS, SMB NAS 1–8 bay (Synology, QNAP, TrueNAS)
- **RPM**: 7200 RPM (8TB)
- **CMR technology**: Conventional Magnetic Recording (not SMR) — important for ZFS/RAID
- **Warranty**: 3-year
- **Sizes at ExtremePC**: 8TB

### Synology HAT3300 / HAT3310 — Synology Plus NAS
- **Target**: Synology NAS (Plus Series — DS/RS models)
- **HAT3300**: Value tier within Synology lineup
- **HAT3310**: Step up (better vibration compensation, higher reliability rating)
- **Compatibility**: Synology Compatibility List validated — best for Synology NAS
- **Warranty**: 3-year (HAT3300) / 5-year (HAT3310)
- **Sizes at ExtremePC**: HAT3300 4TB; HAT3310 8TB, 12TB, 16TB

### Synology HAT5300 / HAT5310 — Synology Enterprise NAS
- **Target**: Synology high-density NAS (SA/FS/HD models), enterprise rackmount
- **HAT5300**: Enterprise tier
- **HAT5310**: Top enterprise tier (higher MTBF, vibration sensors)
- **RPM**: 7200 RPM
- **Warranty**: 5-year
- **Compatibility**: Synology Compatibility List validated — mandatory for enterprise Synology
- **Sizes at ExtremePC**: HAT5300: 4TB, 12TB, 16TB; HAT5310: 8TB, 18TB, 20TB

### Seagate Exos — Enterprise Data Center
- **Target**: Data center, enterprise servers, high-density storage
- **RPM**: 7200 RPM
- **Cache**: 256MB
- **MTBF**: 2.5M hours
- **Workload**: 550 TB/year
- **Warranty**: 5-year
- **Sizes at ExtremePC**: Exos X18 16TB, Exos X20 20TB

### WD Ultrastar — Enterprise Data Center
- **Target**: Data center, enterprise servers, high-density storage
- **RPM**: 7200 RPM
- **MTBF**: 2.5M hours
- **Warranty**: 5-year
- **CMR**: All Ultrastar drives are CMR
- **Sizes at ExtremePC**: HC520 12TB, HC560 20TB

---

## CMR vs SMR — Critical for NAS/RAID

**CMR (Conventional Magnetic Recording)** — safe for:
- RAID arrays (RAID 1, 5, 6, 10)
- ZFS (TrueNAS)
- Always-on NAS
- Write-heavy workloads

**SMR (Shingled Magnetic Recording)** — acceptable for:
- Cold archive storage
- Sequential write workloads
- Desktop secondary drives (rarely written)
- NOT SAFE for RAID rebuild — SMR under sustained write stress can time out and trigger RAID failure

**SMR drives in ExtremePC lineup**: BarraCuda desktop drives are often SMR at certain capacities — always check datasheet before using in NAS/RAID.

**CMR confirmed** at ExtremePC:
- IronWolf, IronWolf Pro: CMR
- WD Red Plus: CMR (vs WD Red which is SMR — note the Plus)
- WD Ultrastar: CMR
- Seagate Exos: CMR
- Synology HAT series: CMR

---

## Capacity Selection Guide

### Desktop Secondary Drive
- 1TB (WD Blue): Legacy, for very budget builds
- 4TB (BarraCuda): Entry-tier bulk storage
- 6TB–8TB (BarraCuda): Value sweet spot for media libraries
- 8TB (BarraCuda): Current sweet spot — lowest $/TB in ExtremePC lineup

### Surveillance (CCTV)
- 1TB–2TB (SkyHawk / WD Purple): Entry, 2–4 cameras, 30-day retention at 720p
- 4TB–6TB: Standard, 8–16 cameras, 30-day retention at 1080p
- 8TB+ (SkyHawk AI): AI NVR with 16–64 cameras, 4K stream support
- 18TB–24TB: High-channel-count AI NVR, 90+ day retention at 4K

### NAS Storage
- 4TB: Entry NAS, 2-bay RAID 1 = 4TB usable
- 8TB: Mid NAS, 4-bay RAID 5 = 24TB usable per 4×8TB set
- 10TB–12TB: Larger builds
- 16TB–24TB: High-capacity NAS, 8-bay systems

### Enterprise / Data Center
- 12TB–20TB: Typical data center node capacity per drive
- 20TB+ (Exos X20, Ultrastar HC560): High-density enterprise

---

## NZ-Specific Context

- **Auckland humidity**: Surveillance drives running 24/7 in outdoor NVR enclosures should have adequate airflow. Seagate ImagePerfect and WD AllFrame firmware handle NZ coastal humidity better than consumer drives.
- **Synology NAS is dominant in NZ market**: HAT series drives validated for Synology compatibility is a genuine advantage for NZ buyers who prefer Synology NAS.
- **Power outages (Wellington)**: For NAS/RAID systems in Wellington's storm-prone environment, CMR drives with proper UPS are critical. SMR drives can be corrupted by power loss during SMR zone rewrites.
- **Local warranty**: Seagate and WD warranty through ExtremePC NZ; Synology HAT warranty through ExtremePC as Synology NZ distributor.

---

## GEO Writing Anti-Patterns for HDDs

- ❌ "Fast performance" for a 5400 RPM consumer HDD — use actual RPM and realistic MB/s (typically 180–250 MB/s sequential)
- ❌ "Suitable for NAS" for BarraCuda/WD Blue — these are explicitly NOT NAS-rated
- ❌ "Enterprise reliability" without citing MTBF numbers
- ❌ Omit SMR vs CMR mention on NAS/RAID pages
- ❌ Compare HDD to SSD speed without acknowledging the gap
- ✅ Lead with the use case: surveillance drives → camera count + days of retention; NAS drives → bay count + RAID type; consumer → media library size

---

## TBW / Workload Ratings by Line

| Line | Workload (TB/year) | MTBF |
|------|-------------------|------|
| BarraCuda | 55 | 600K hours |
| SkyHawk | 180 | 1M hours |
| SkyHawk AI | 360 | 1.2M hours |
| WD Purple | 180 | 1M hours |
| WD Purple PRO | 360 | 1M hours |
| IronWolf | 180 | 1M hours |
| IronWolf Pro | 300 | 1.2M hours |
| WD Red Plus | 180 | 1M hours |
| Synology HAT3310 | 180 | 1M hours |
| Synology HAT5310 | 550 | 2.5M hours |
| Seagate Exos | 550 | 2.5M hours |
| WD Ultrastar | 550 | 2.5M hours |
