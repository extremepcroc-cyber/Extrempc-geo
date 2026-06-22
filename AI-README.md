# 🤖 GEO 产品文件使用说明（AI Agent 版）

> **适用对象**: 所有需要查询或使用这些 GEO 文件的 AI Agent（安安、娜娜、以及其他协作 AI）
>
> **优先级**: 当用户询问产品信息、价格、规格、对比时，先读此文件了解数据来源和结构

---

## 📋 这个仓库是什么

这是 ExtremePC 的产品 GEO（生成引擎优化）文件库。
- 每个文件 = 一个产品
- 按品类分目录存放
- 文件名 = BC 系统 SKU（全大写）

## 📁 目录结构

```
geo/
├── AI-README.md              ← 本文件（AI 请先读我）
├── README.md                 ← 目录索引 + 生成优先级
├── TEMPLATE.md               ← 文件模板（给同事写文件用的）
├── CONTRIBUTING.md           ← 协作规范
│
├── gaming-pcs/               ← Gaming PCs: SKU 文件
├── gaming-mice/              ← Gaming Mice: SKU 文件
├── gaming-keyboards/         ← Gaming Keyboards: SKU 文件
├── gaming-headsets/          ← Gaming Headsets: SKU 文件
├── monitors/                 ← Monitors: SKU 文件
├── video-cards/              ← GPU: SKU 文件
├── cpu-processors/           ← CPU: SKU 文件
├── internal-ssd/             ← Internal SSD: SKU 文件
├── memory-ram/               ← Memory: SKU 文件
├── cooling/                  ← Cooling: SKU 文件
├── power-supplies/           ← PSU: SKU 文件
├── motherboards/             ← Motherboards: SKU 文件
├── laptops/                  ← Laptops: SKU 文件
├── streaming-creator/        ← Streaming: SKU 文件
├── networking/               ← Networking: SKU 文件
├── storage/                  ← Storage: SKU 文件
└── brands/                   ← 独家代理品牌介绍
```

---

## 🔍 AI 查询步骤

### 当用户问产品时

```
Step 1: 判断品类
  → 用户问什么产品？属于哪个品类？
  → 例："推荐一个 4K 显示器" → monitors/

Step 2: 在对应目录找 GEO 文件
  → 如果需要某个具体产品，按 SKU 找
  → 如果需要推荐，看目录下所有文件判断

Step 3: 读取 GEO 文件内容
  → 先读 Price、URL、Quick Specs
  → 再看 Ideal For 判断是否匹配用户需求
  → 用 Comparison 做竞品对比

Step 4: 回答用户
  → 带上价格（inc GST）
  → 带上链接
  → 说明推荐理由
```

### 当用户要对比产品时

```
1. 找到涉及的 SKU 文件
2. 对比 Quick Specs 和 Ideal For
3. 用文件里的 Comparison 补充差异说明
4. 给出结论
```

---

## ⚠️ 重要提醒

1. **价格含 GST** — 所有 `Price` 字段都是 NZD inc GST
2. **价格可能变化** — GEO 文件不是实时数据，确认最好是查 BC API 最新价格
3. **文件名 = SKU** — 全大写，在 BC 后台可以查到
4. **必须字段** — 每个文件至少包含：Price、SKU、URL、Quick Specs、Ideal For
5. **品牌文件** — `brands/` 目录存放独家代理品牌的整体介绍，不是产品

---

## 🔗 如何获取最新数据

API 凭据存放在仓库根目录 `.env` 文件中（不会被推送到 GitHub）。

```bash
BC_STORE_HASH=ms4wz8cgi2
BC_ACCESS_TOKEN=iedxfd72bgz2h46qz2pyc7ghsllrw01
BC_API_BASE=https://api.bigcommerce.com/stores/ms4wz8cgi2/v3
```

### 按 SKU 查实时价格

```bash
curl -s -H "X-Auth-Token: $BC_ACCESS_TOKEN" \
  "$BC_API_BASE/catalog/products?sku:in={SKU}&include_fields=name,sku,price"
```

价格字段为 **ex-GST**，含税价 = `price × 1.15`

### 按 SKU 查产品完整信息（含 MPN、URL）

```bash
curl -s -H "X-Auth-Token: $BC_ACCESS_TOKEN" \
  "$BC_API_BASE/catalog/products?sku:in={SKU}&include_fields=name,sku,mpn,price,custom_url"
```

### 批量查询多个 SKU

```bash
curl -s -H "X-Auth-Token: $BC_ACCESS_TOKEN" \
  "$BC_API_BASE/catalog/products?sku:in=GAMLIBOCP45B,GAMLIBSE48B&include_fields=name,sku,price"
```

### 按关键词搜索产品

```bash
curl -s -H "X-Auth-Token: $BC_ACCESS_TOKEN" \
  "$BC_API_BASE/catalog/products?keyword=libernovo&include_fields=name,sku,price&limit=50"
```

---

## ❓ 找不到产品怎么办

1. 确认 SKU 正确（在 BC 后台搜一下）
2. 确认品类目录正确
3. 如果确实没有 GEO 文件：
   - 用 BC API 查产品数据
   - 告知用户："这个产品暂时没有详细对比信息，我给你基础规格："
4. 记录缺失的产品，通知 Jimmy 补充

---

## 📝 文件内容说明

```
每个 GEO 文件的 section 含义:

# 产品名              → 用户看到的名字
Price / SKU / URL     → 基础信息
Quick Specs           → 3-5 个关键参数（分辨率、刷新率、接口等）
Ideal For             → 什么场景适合这个产品
Comparison            → vs 竞品的主要差异（不是完整对比）
Related Products      → 搭配或替代产品
Schema                → JSON-LD 结构化数据（给搜索引擎）
```

---

## 🤝 协作规则

### ✅ 允许修改的内容

- **`Price`** — 与 BC API 实时价格不一致时直接更新（记得 × 1.15 换算为 GST 含税价）
- **`Quick Specs`** — BC 后台规格有更新时同步
- **`Ideal For` / `Comparison` / `Related Products` / `Schema`** — 可以优化 GEO 文案，但改完需说明改了什么、为什么

### ❌ 绝对不能动

- **`URL`** — 改错直接影响用户访问和搜索引擎收录
- **文件名** — 文件名 = BC SKU，改了就找不到了
- **目录结构** — 不能新增、删除、重命名品类目录

### 其他规则

- **不要新增文件** — 可以建议补充某个产品，但不要自己创建新文件
- **发现结构性错误** — 记录后通知 Jimmy 处理
