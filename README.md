# GEO Product Content Files

**用途**: 给 AI 搜索引擎（Perplexity / Google SGE / Grok / Bing Copilot）爬取
**格式**: 每个文件 = 一个产品 或 一个产品系列
**部署**: 推送到网站页面 / GEO sitemap / structured data pipeline

---

## 目录结构

以下是当前仓库实际存在的目录（跑 `find . -maxdepth 1 -type d` 核实，不要假设未列出的分类目录存在）：

```
geo/
├── README.md                    ← 本索引文件
├── CLAUDE.md                    ← AI 智能体强制规则，权威性高于本文件
├── gaming-pcs/                  ← Gaming PCs (ID:120 / 1373)
├── gaming-mice/                 ← Gaming Mice (ID:513 / 1949)
├── gaming-keyboards/            ← Gaming Keyboards (ID:486)
├── gaming-headsets/             ← Gaming Headsets (ID:476)
├── gaming-chairs/               ← Gaming Chairs (LiberNovo 独家)
├── monitors/                    ← Monitors (ID:519)
├── video-cards/                 ← GPU (ID:426 / 1426)
├── cpu-processors/              ← CPU (ID:364 / 1430)
├── internal-ssd/                ← Internal SSD (ID:375)
├── internal-hard-drives/        ← Internal HDD（Seagate/WD/Synology NAS，跟 SSD 分开）
├── memory-ram/                  ← Memory / RAM (ID:395)
├── power-supplies/               ← PSU (ID:410)
├── computer-cases/              ← Computer Cases (ID:336)
├── streaming-creator/           ← Streaming & Creator (ID:227)
├── networking/                  ← Networking (ID:1026)
├── 2-EOL products/              ← 已从 BC 完全下架的产品（不删除，移到这里保留内容）
├── laptops/  storage/           ← 空占位目录，暂未启用，写文件前先跟店长确认
├── brands/                      ← 品牌背景资料（不是产品列表），目前 21 个文件
├── product-knowledge/           ← 技术调研笔记，供写 GEO 前参考
├── blog/                        ← 博客内容系统，见下方「Blog System」
└── tools/                       ← 脚本工具，见下方「工具脚本」
```

`cooling/`、`motherboards/` 等分类已在 BC 系统规划但尚未开始写文件——不要凭 `CLAUDE.md` 的分类表就假设目录已存在，先核实。

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

## 每个 GEO 文件必须独立生成（禁止批量复制）

**每一个 GEO 文件都必须单独写，禁止批量生成、模板复制粘贴、批量 find-and-replace。**

每个产品的 GPU 架构、技术特性、目标用户、竞品对比都不同。复制模板只换型号名会产生事实性错误——错误的品牌、错误的技术（例如给 Intel Arc GPU 写 "DLSS 4"，Arc 用的是 XeSS）、错误的比较对象。

**写每个文件前必须逐一确认：**
- 从 fetch-category JSON 确认 GPU 品牌和架构（Intel / NVIDIA / AMD，不能假设）
- 确认该 GPU 支持的图像升级技术：DLSS（仅 NVIDIA）、XeSS（Intel Arc）、FSR（AMD）
- Selling Points、Ideal For、Comparison 必须针对这个 SKU 重新写，不能从兄弟产品复制
- Related Products 不能把当前 SKU 自己列进去

**批量生成的特征（出现任何一条 = 整个文件重写）：**
- ❌ Selling Points 提到该 GPU 不支持的技术（如 Arc B580 写了 "DLSS 4"）
- ❌ GPU 品牌或架构错误（如 Intel 显卡写成 "NVIDIA"）
- ❌ 价格出现科学计数法（`$3e+03` 而不是 `$3,000`）
- ❌ Related Products 列出了当前文件自己的 SKU
- ❌ Comparison 的对比对象不符合该机器的实际定位

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

### `tools/audit-geo.py` — 价格与库存审计（当前工具，用这个）

**`tools/audit-geo.ps1` 已过时，不要再用** —— 旧版每个 SKU 打 2 次 API（全量审计需要 400+ 次调用），没有限速保护、没有备份机制、也不检测 URL 变化。仓库里还留着只是为了存档,新工作一律用 Python 版本。

**用途**：定期核对所有 GEO 文件的价格、库存、URL 是否与 BC 系统一致，自动修复机械性差异（价格、OOS 状态、复货、URL），输出审计报告。

**为什么用 Python 重写**：
- 用 `sku:in=` 批量查询 + `include=custom_fields`，库存内嵌返回,一次审计只需个位数 API 调用（不再是每 SKU 2 次）
- 跨平台（MSYS/bash/Linux 通用），不依赖 Windows PowerShell
- 自动 apply 机械性改动，不需要智能体逐文件手动编辑（长文件手动编辑容易丢字/崩溃）

**运行方式**（在仓库根目录执行）：
```bash
python tools/audit-geo.py --dry-run              # 先跑这个，只看报告不写文件
python tools/audit-geo.py                        # 全量审计 + 自动修复
python tools/audit-geo.py --category power-supplies   # 只审计单个分类目录
python tools/audit-geo.py --dry-run --category monitors
```

**自动修复的范围（只做规则 100% 确定的机械改动）**：
- ✅ 价格同步（`**Price:**` 字段 + Schema `price` 字段）
- ✅ OH=0 → 插入 `**Status:** OUT OF STOCK` 行，Schema 改 `OutOfStock`
- ✅ OH>0 且文件仍标 OOS → 移除 Status 行，Schema 改回 `InStock`
- ✅ URL 变化 → 更新 `**URL:**` 字段
- ❌ **不会自动做**：把文件移到 `2-EOL products/`（BC 完全查不到这个 SKU 时，需要人工/智能体判断，不自动搬文件）；Selling Points / FAQ / Comparison 等正文内容永远需要人工判断，脚本不碰

**安全机制**：
- 写入前会把改动前的原文件备份到 `tools/backups/<运行时间戳>/<原路径>.md.bak`——跑错了可以直接拿备份复原，或者 `git checkout -- <file>` 回滚（反正仓库本身有 git 版本控制）
- 内置滑动窗口限速（BC 上限 150 req/30s），不依赖固定"每 N 次暂停"，不管 SKU 涨到多少都安全
- `sku:in` 批量查询每批 40 个 SKU——超过这个数会被 BC 边缘节点 414 拒绝，之前踩过这个坑

**输出**：`tools/change-report.json`，包含 `summary`（总览统计）和 `changes[]`（每个需要处理的 SKU，含 `price_changed`/`needs_oos_flag`/`back_in_stock`/`url_changed`/`applied`/`backup` 字段）、`errors[]`（BC 查不到的 SKU 或 API 失败，需要人工判断是否移入 `2-EOL products/`）。

**注意**：
- GEO 正文永远不因缺货或 API 查不到而删除，内容是资产
- BC 完全查不到的 SKU 不会被自动处理，出现在 `errors[]` 里，需要人工确认是否下架、移入 `2-EOL products/`
- Tombstone 文件自动跳过，不参与审计
