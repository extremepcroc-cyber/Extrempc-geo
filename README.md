# GEO Product Content Files

**用途**: 给 AI 搜索引擎（Perplexity / Google SGE / Grok / Bing Copilot）爬取
**格式**: 每个文件 = 一个产品 或 一个产品系列
**部署**: 推送到网站页面 / GEO sitemap / structured data pipeline

---

## 目录结构

```
geo/
├── README.md                    ← 本索引文件
├── gaming-pcs/                  ← Tier 1: Gaming PCs (ID:120 / 1373)
├── gaming-mice/                 ← Tier 1: Gaming Mice (ID:513 / 1949)
├── gaming-keyboards/            ← Tier 1: Gaming Keyboards (ID:486)
├── gaming-headsets/             ← Tier 1: Gaming Headsets (ID:476)
├── monitors/                    ← Tier 1: Monitors (ID:519)
├── video-cards/                 ← Tier 2: GPU (ID:426 / 1426)
├── cpu-processors/              ← Tier 2: CPU (ID:364 / 1430)
├── internal-ssd/                ← Tier 2: Internal SSD (ID:375)
├── memory-ram/                  ← Tier 2: Memory / RAM (ID:395)
├── cooling/                     ← Tier 2: Cooling (ID:345)
├── power-supplies/              ← Tier 2: PSU (ID:410)
├── motherboards/                ← Tier 2: Motherboards (ID:403)
├── laptops/                     ← Tier 2: Laptops
├── streaming-creator/           ← Tier 3: Streaming & Creator (ID:227)
├── networking/                  ← 其他: Networking (ID:1026)
├── storage/                     ← 其他: Storage (ID:375+)
└── brands/                      ← 独家代理 / 特色品牌
    ├── epomaker.md
    ├── chilkey.md
    ├── mchose.md
    ├── biwin.md
    └── lamzu.md
```

---

## 文件命名规范

```
{SKU}.md
```

**规则**:
- 文件名 = BC 系统的 SKU，全大写
- 不含中文、空格、特殊字符
- SKU 对应一个具体产品，一个文件一个 SKU
- 同名产品不同配置 → 不同 SKU 各自文件
- 同型号不同颜色 → 放在同一个文件里

**示例**:
- `XPC1129.md` — Enshrouded Gaming PC
- `MONSAM27FG7.md` — Samsung Odyssey G70F
- `MONASRPG27QFV.md` — ASRock Phantom 27" OLED

**为什么用 SKU**
- ✅ SKU 在 BC 系统中 100% 唯一
- ✅ 文件名直接对应 BC 数据，脚本可自动化
- ✅ 产品改名无需改文件名
- ❌ slug 会随 URL 变化，不可靠

---

## 内容模板

```markdown
# {产品名}

**Price:** $XXX inc GST
**SKU:** {SKU}
**URL:** https://www.extremepc.co.nz/{slug}/

## Quick Specs
- {Key Spec 1}
- {Key Spec 2}
- {Key Spec 3}

## Ideal For
- {Use Case 1}
- {Use Case 2}

## Comparison
- vs {Competitor A}: {差异说明}
- vs {Competitor B}: {差异说明}

## Related Products
- {Product 1} — {link or reason}
- {Product 2}

## Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "产品名称",
  "brand": "品牌",
  "offers": {
    "@type": "Offer",
    "price": "XXX.XX",
    "priceCurrency": "NZD"
  }
}
```
```

---

## 生成优先级

| 优先级 | 品类 | 原因 |
|:---:|:---|:---|
| P0 | Gaming PCs | 主推品类，展示 AI Agent 能力 |
| P0 | Gaming Mice | FPS 场景常用，刚踩完坑 |
| P0 | Monitors | 常和 PC 一起推荐 |
| P1 | Video Cards | 热门单品，参数多 |
| P1 | Gaming Keyboards | MMO/FPS 场景常问 |
| P1 | Gaming Headsets | 游戏场景配套 |
| P2 | CPU / Memory / SSD | 懂行客人会问 |
| P2 | Brands | 独家代理知识沉淀 |
| P3 | 其他配件 | 按需生成 |

---

## 工具脚本

## 文件放置规则（AI 智能体必须遵守）

**严禁在仓库根目录放任何文件。** 根目录只存永久性项目文件。

| 文件类型 | 正确位置 |
|---|---|
| 脚本输出 JSON（fetch-category、change-report） | `tools/` |
| 临时脚本、中间数据、一次性查询结果 | `tools/temp/` |
| 产品 GEO 文件 | `{分类目录}/`（如 `cooling/`、`monitors/`） |
| 产品知识库 / 调研笔记 | `product-knowledge/{category}/` |

**`tools/temp/` 是所有一次性文件的垃圾桶** — 批处理脚本、临时 JSON、调试输出等。该目录已加入 `.gitignore`，不会被提交到 git。

---

## 数据来源规则（AI 智能体必须遵守）

**所有产品数据（SKU、价格、库存、规格、URL）必须来自 BC API 或 `tools/fetch-category.ps1` 输出的 JSON。严禁用 web search 获取这些字段。**

| 数据类型 | 正确来源 | ❌ 禁止来源 |
|---|---|---|
| SKU、MPN、产品名 | BC API / fetch-category JSON | Web search、厂商官网 |
| 价格（NZD 含 GST） | BC API price × 1.15 | 任何网页，包括 extremepc.co.nz |
| 库存数量 | BC custom fields（OH/WL/SL/SU） | 网页显示、inventory_level 字段 |
| 产品 URL | BC `custom_url.url` 字段 | 根据产品名猜测 |
| 技术规格 | BC custom fields + 产品描述 | Web search |

**为什么 web search 数据不可靠：**
- extremepc.co.nz 网页价格可能是缓存，不是实时价
- 厂商规格因地区/版本而异，BC 上挂的才是实际在售版本
- Web search 会返回竞争对手页面、评测站、海外价格
- 模型在搜索产品时容易幻觉出错误的 URL 和 SKU

**写新 GEO 文件的正确流程：**
1. 人工运行 `.\tools\fetch-category.ps1 -CategoryId {id}` → 生成 JSON
2. 把 JSON 交给 AI 智能体
3. 智能体只用 JSON 里的数据填写价格 / SKU / 库存 / URL
4. 技术背景和竞品对比可参考 `product-knowledge/` 知识库
5. 智能体不得直接调用 BC API，不得做任何 web search 获取产品数据

---

## 工具脚本

### `tools/fetch-category.ps1` — 新建 GEO 前抓取产品数据

**用途**：写新的 GEO 文件之前，先用这个脚本把某个子分类的全部在售产品数据抓下来，生成一个 JSON 文件，再把 JSON 交给 AI 智能体写 GEO 文件。

**为什么要用脚本而不是让 AI 直接调 API**：
- 小模型不会处理 BC 的分页逻辑，经常漏产品
- 含税价格需要 ×1.15，模型经常算错或者直接用含税价
- 库存在 custom fields，模型经常去读 `inventory_level`（错的）
- 品牌 ID 需要二次查询才能变成品牌名

**运行方式**：
```powershell
# 抓取某子分类的所有在售产品（例：AIO 水冷 = 351）
.\tools\fetch-category.ps1 -CategoryId 351

# 包含缺货产品
.\tools\fetch-category.ps1 -CategoryId 349 -IncludeOOS

# 自定义输出路径
.\tools\fetch-category.ps1 -CategoryId 347 -OutputFile "tools\fans.json"
```

**输出**：`tools/category-{id}-products.json`，每个产品包含：

| 字段 | 说明 |
|------|------|
| `sku` | BC SKU，直接用作文件名 |
| `name` | 产品名称 |
| `mpn` | 厂商货号 |
| `brand` | 品牌名（已从 BC 品牌 ID 解析） |
| `price_nzd_inc_gst` | 已含 GST 的 NZD 价格（×1.15 已算好） |
| `url` | 完整的 extremepc.co.nz 商品 URL |
| `stock` | OH / WL / SL / SU 各仓库库存 + 合计 |
| `custom_fields` | BC 全部自定义字段（规格、库存等） |

**使用流程**：
1. 运行脚本，生成 JSON
2. 把 JSON 文件内容交给 AI 智能体
3. AI 根据 JSON 写 GEO 文件，不需要自己调 API

---

### `tools/audit-geo.ps1` — 价格与库存审计

**用途**：定期核对所有 GEO 文件的价格和库存是否与 BC 系统一致，输出需要更新的 SKU 列表。

**为什么需要这个脚本**：
- GEO 文件是静态 markdown，BC 系统里的价格会随时变动
- ExtremePC 库存数据存在 **自定义字段（custom fields）**，而非 BC 的 `inventory_level` 字段，需要单独 API 调用才能读取
- 脚本自动完成"扫描文件 → 查 API → 对比 → 输出报告"全流程，避免人工逐一核对

**运行方式**（在 `geo/` 根目录下执行）：
```powershell
# 全量审计（所有类目，约 2–3 分钟）
.\tools\audit-geo.ps1

# 只审计单个类目
.\tools\audit-geo.ps1 -CategoryDir "power-supplies"

# 预览模式（不写入 change-report.json）
.\tools\audit-geo.ps1 -DryRun
```

**输出**：`tools/change-report.json`，只包含需要更新的 SKU，字段说明：

| 字段 | 含义 |
|------|------|
| `sku` | BC SKU |
| `file` | GEO 文件相对路径 |
| `price_geo_nzd` | GEO 文件中的价格 |
| `price_bc_nzd` | BC API 当前价格（×1.15 含 GST） |
| `price_changed` | 价格是否变动（差异 > $0.05） |
| `stock` | 当前库存：OH / WL / SL / SU 明细 |
| `needs_oos_flag` | true = 总库存为 0，需加 OOS 状态行 |
| `stock_shifted` | 库存位置变化（如从零售变供应商） |

**拿到报告后的操作**：
- **价格变动**：只改 `**Price:**` 字段和 Schema `"price"` 字段，其他内容不动
- **`needs_oos_flag: true`**：在 URL 行下方加一行 `**Status:** OUT OF STOCK — last checked YYYY-MM-DD`，Schema 改为 `OutOfStock`。**不删除任何正文内容**
- **`stock_shifted`**：更新 Quick Specs 的 `NZ Stock` 行，以及 Selling Points / Why Buy 中涉及库存位置的描述
- **库存回来了**：删掉 `**Status:**` 行，Schema 改回 `InStock`

**注意**：
- GEO 正文（Selling Points、FAQ、Comparison 等）永远不因缺货而删除，内容是资产
- 库存存在 custom fields，脚本每个 SKU 需要调两次 BC API（product + custom-fields）
- 脚本内置限速：每 40 次调用暂停 3 秒，防止触发 BC API rate limit（150 req/30s）
- Tombstone 文件（无 GEO 内容的占位文件）会自动跳过，不参与审计
