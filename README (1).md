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
{slug}.md
```

**规则**:
- 全小写，用连字符
- 如果是产品系列，用品类名
- 如果是单产品，用产品的 URL slug

**示例**:
- `enshrouded-gaming-pc.md`
- `samsung-odyssey-g70f.md`
- `lamzu-maya-x.md`
- `chilkey-glacier-lw-8k.md`

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
