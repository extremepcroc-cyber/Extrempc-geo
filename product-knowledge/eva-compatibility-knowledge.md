# EVA 兼容性问答 — 所需知识清单

> 目的: 让 EVA 不靠爬网站、不靠调 API，直接读本地数据就能回答"能不能装"类问题
> 优先级: 按客人提问频率排列

---

## 1. 机箱 (Case)

### 客人常问
- "这个机箱能装 4080 / 4090 吗？"
- "能装 360 水冷吗？"
- "这个电源能放进去吗？"
- "支持 ATX 主板吗？"
- "能装几个风扇？"

### 需要加进 GEO Quick Specs 的字段

| 字段 | 示例值 | 用途 |
|:-----|:-------|:-----|
| `Form Factor` | ATX Mid Tower | 告诉客人这是什么尺寸的机箱 |
| `Motherboard Support` | ATX, M-ATX, ITX | 能不能装客人的主板 |
| `Max GPU Length` | 360mm | 能不能装 4080/4090（4080 FE ~310mm, 4090 FE ~350mm） |
| `Max CPU Cooler Height` | 170mm | 能不能装塔式风冷 |
| `PSU Length Limit` | 200mm | 能不能装客人的电源 |
| `Radiator Support` | Top: 360mm, Front: 360mm | 能不能装 240/360 水冷 |
| `Fan Support` | 3x 120mm front, 1x 120mm rear | 能装几个风扇 |
| `GPU Clearance Note` | Support up to 360mm with front fan | 特殊说明（装风扇后显卡长度限制） |

### 数据来源
- 厂商官网规格表
- Newegg / Amazon listing
- 直接量实物

---

## 2. 电源 (PSU)

### 客人常问
- "这个电源能带 4080 吗？"
- "够我这套配置用吗？"
- "有 12VHPWR 接口吗？"
- "能装进我的机箱吗？"

### 需要加进 GEO Quick Specs 的字段

| 字段 | 示例值 | 用途 |
|:-----|:-------|:-----|
| `Wattage` | 850W | 够不够推客人的配置 |
| `Form Factor` | ATX / SFX | 能不能装进机箱 |
| `Dimensions` | 150 x 140 x 86mm | 能不能装进机箱 |
| `CPU Connectors` | 2x 4+4pin | 主板兼容性 |
| `PCIe Connectors` | 3x 6+2pin | 显卡供电 |
| `12VHPWR Connector` | Yes (600W) | 40 系列显卡原生供电 |
| `80 Plus Rating` | Gold | 能效等级 |
| `Modular` | Fully Modular | 理线方便程度 |

### 4080/4090 参考功耗
- RTX 4080: ~320W TDP，建议 750W+
- RTX 4090: ~450W TDP，建议 850W+
- RTX 5070: ~250W TDP，建议 650W+
- RTX 5060: ~150W TDP，建议 550W+

---

## 3. 主板 (Motherboard)

### 客人常问
- "支持 DDR5 还是 DDR4？"
- "能上 14900K 吗？"
- "有几个 M.2 插槽？"
- "能插我的 4080 吗？（PCIe 插槽间距）"

### 需要加进 GEO Quick Specs 的字段

| 字段 | 示例值 | 用途 |
|:-----|:-------|:-----|
| `Socket` | LGA1700 / AM5 | CPU 兼容性 |
| `Chipset` | Z790 / B650 | 功能级别 |
| `Memory Type` | DDR5-6400 | 内存兼容性 |
| `Max Memory` | 128GB | 最大容量 |
| `Memory Slots` | 4x DIMM | 插槽数量 |
| `PCIe x16 Slots` | 1x PCIe 5.0 x16 | 显卡插槽版本 |
| `M.2 Slots` | 3x M.2 NVMe | 固态硬盘数量 |
| `SATA Ports` | 4x SATA III | 传统硬盘数量 |
| `Form Factor` | ATX / M-ATX / ITX | 机箱兼容性 |

---

## 4. CPU 散热器 (Cooler)

### 客人常问
- "能压住 14900K 吗？"
- "能装进我的机箱吗？"
- "要换扣具吗？"

### 需要加进 GEO Quick Specs 的字段

| 字段 | 示例值 | 用途 |
|:-----|:-------|:-----|
| `Type` | Air Cooler / 360mm AIO | 散热类型 |
| `Socket Support` | LGA1700, AM5 | 兼容哪些 CPU |
| `Height` | 154mm | 能不能装进机箱（风冷） |
| `Radiator Size` | 360 x 120 x 27mm | 能不能装进机箱（水冷） |
| `TDP Rating` | 260W | 能不能压住客人的 CPU |
| `Fan Speed` | 500-1800 RPM | 散热性能 |
| `Noise Level` | ≤30 dBA | 噪音水平 |

---

## 5. 显卡 (GPU)

### 客人常问
- "能装进我的机箱吗？"
- "需要多大电源？"
- "需要什么接口的电源线？"

### 需要加进 GEO Quick Specs 的字段

| 字段 | 示例值 | 用途 |
|:-----|:-------|:-----|
| `Length` | 331mm | 能不能装进机箱 |
| `Width` | 2.5 slots | 机箱宽度兼容性 |
| `Recommended PSU` | 750W | 需要多大电源 |
| `Power Connectors` | 1x 12VHPWR | 需要什么电源线 |
| `TDP` | 320W | 功耗参考 |

---

## 6. 内存 (RAM)

### 客人常问
- "我的主板支持这个内存吗？"
- "能上 64GB 吗？"

### 需要加进 GEO Quick Specs 的字段

| 字段 | 示例值 | 用途 |
|:-----|:-------|:-----|
| `Type` | DDR5-6000 | 内存代数 |
| `Capacity` | 2x 16GB | 容量 |
| `Timings` | CL30-36-36-76 | 性能参考 |
| `Voltage` | 1.35V | 兼容性参考 |
| `XMP/EXPO` | EXPO Ready | 一键超频支持 |

---

## 实施优先级

| 优先级 | 品类 | 原因 |
|:------:|:-----|:------|
| 🥇 | **机箱** | 兼容性问题最多（能装什么？），而且客人决策的第一步 |
| 🥇 | **电源** | "够不够用"是第二高频问题 |
| 🥈 | **主板** | CPU/内存/显卡兼容性的枢纽 |
| 🥈 | **CPU 散热器** | "能不能压住" + "能不能装进机箱" |
| 🥉 | **显卡** | 长度和功耗信息 |
| 🥉 | **内存** | DDR4 vs DDR5 区分 |

---

## 备注

- 这些字段只需要加到 GEO 文件的 `Quick Specs` 部分
- 不需要每个字段都填——填了比不填好，没数据的标 `TBC`
- 数据来源优先级：厂商官网 > 实测 > Newegg/Amazon > 估算
