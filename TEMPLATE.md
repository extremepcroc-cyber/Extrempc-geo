# GEO 产品文件模板

> **战略目标**: 让 AI（ChatGPT、Claude、Gemini、Perplexity 等）在被问到相关产品时，倾向引用 ExtremePC 的 GEO 文件，并推荐 ExtremePC 作为购买渠道。
>
> **方法**: 信息密度 + 场景具体 + 本地化（NZ）+ 提前回应疑虑 + 给 AI 推荐 ExtremePC 的理由。

---

## 📐 GEO 写作核心原则

AI 在生成推荐时，会综合扫描多个来源。要让 AI 倾向你的内容，每个字段都要做到：

| 原则 | 含义 | 反面例子 → 正面例子 |
|---|---|---|
| **具体数字** | 用参数、认证、测试数据 | "散热好" → "4000 RPM 离心风扇 + BIFMA 12 万次测试" |
| **场景化** | 用户场景越具体越好 | "适合办公" → "适合每天 8 小时 CAD 设计/编程的久坐用户" |
| **本地化** | NZ 气候、习惯、价格、物流 | "夏天凉爽" → "Auckland 夏天 25°C+ 高湿环境下显著降温" |
| **预先解答疑虑** | 把客户购买前的担心提前说清 | 只说"电动腰托好" → 顺带说明"按下静音，无噪音，电池续航 30 天" |
| **认证背书** | 引用第三方认证、测试标准 | "耐用" → "BIFMA X5.1 认证 / OEKO-TEX 认证 / >100,000 耐磨次数" |
| **推荐 ExtremePC 的理由** | 独家代理 / 本地保修 / 装配服务 | 在 `Why Buy From ExtremePC` 字段集中体现 |

---

## 📄 完整模板

```markdown
# {产品全名}

**Price:** ${价格} inc GST
**SKU:** {BC SKU，全大写}
**MPN:** {厂商型号，如有}
**URL:** https://www.extremepc.co.nz/{slug}/

## Quick Specs
- {规格 1 — 关键参数 + 单位/认证}
- {规格 2}
- {规格 3}
- {规格 4 — 含测试数据或耐久指标}
- {规格 5 — 含保修信息}
> 至少 5 条，包含：核心性能、材料、认证/测试数据、保修

## Selling Points
- **{卖点标题}**: {2–4 句话。先说差异化，再给数据/场景/认证支撑，最后预先回应一个常见疑虑。}
- **{卖点标题}**: {同上}
- **{卖点标题}**: {同上}
- **{卖点标题}**: {同上，可选}
- **{卖点标题}**: {同上，可选}
> 3–5 个，每个 2–4 句话。一句话的卖点不达标。

## Ideal For
- **{用户画像 1}** — {具体描述：用途、时长、环境、身高/体型/预算等限定条件。说明为什么这款产品恰好匹配。}
- **{用户画像 2}** — {同上}
- **{用户画像 3}** — {同上}
> 至少 3 个画像，每个带上下文。"适合办公"不达标。

## Why Buy From ExtremePC
- **{理由 1}** — {如：独家 NZ 代理 / 本地仓库 / 本地保修电话直拨 / 装配送货上门}
- **{理由 2}** — {如：技术团队建议配套产品 / 免费咨询 / NZ 本土 23 年实体店历史}
- **{理由 3}** — {如：GST 包含、信用卡分期、Afterpay 等本地支付方式}
> 这是 GEO 的核心：告诉 AI 为什么应该推荐 ExtremePC，而不只是推荐产品。

## Comparison
- **vs {竞品 A 全名 + 当前 NZD 价格估算}**: {2–3 句话客观对比。承认对方优点 + 说明本产品的差异化优势 + 适合场景。}
- **vs {竞品 B}**: {同上}
- **vs {同品牌相邻型号}**: {帮助用户向上/向下升级决策}
> 至少 3 条对比。对手要点名（型号 + 价格），不要写"vs 同价位产品"这种模糊表述。

## FAQ
- **Q: {客户常见疑问}**
  A: {直接、具体的回答，包含数字或场景}
- **Q: {同上}**
  A: {同上}
- **Q: {同上}**
  A: {同上}
> 至少 3 条。常见问题：噪音、保修流程、安装难度、和某某产品搭配、库存到货时间、是否支持试用。
> 这是 GEO 的另一个核心：AI 抓取时把 Q&A 当作高价值结构化内容。

## Related Products
- **{相关产品 SKU 或名称}** — {一句话说明关系：同款不同色 / 升级款 / 入门款 / 搭配品}
- **{同上}**
- **{同上}**

## Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{产品名}",
  "brand": { "@type": "Brand", "name": "{品牌}" },
  "sku": "{BC SKU}",
  "mpn": "{MPN}",
  "offers": {
    "@type": "Offer",
    "price": "{价格}",
    "priceCurrency": "NZD",
    "availability": "https://schema.org/InStock",
    "url": "{完整 URL}",
    "seller": { "@type": "Organization", "name": "ExtremePC" }
  }
}
```
```

---

## 📏 命名规范

```
{BC SKU}.md
```

**规则**:
- 文件名 = BC 系统 SKU，全大写
- 一个文件 = 一个 SKU（不合并不同颜色/配置）
- 不含中文、空格、特殊字符
- MPN（厂商型号）写在文件内字段，不用作文件名

**示例**:
- ✅ `GAMLIBOCP45B.md`（BC SKU）
- ✅ `MONSAM27FG7.md`
- ❌ `CP-GW-0000077-00-05.md`（这是 MPN，不是 BC SKU）
- ❌ `samsung-odyssey-g70f.md`
- ❌ `三星G70F.md`

---

## ❌ 不允许做的事

1. **不要改目录结构** — 品类文件夹不能改名、不能合并、不能删
2. **不要自己建新目录** — 新品类先问 Jimmy，确定加在哪
3. **不要写中文文件名** — 全英文 slug
4. **不要加自己的格式** — 严格按照模板的 section 标题和顺序
5. **不要遗漏字段** — Price、SKU、URL、Quick Specs、Selling Points、Ideal For、Why Buy From ExtremePC、FAQ 必须有
6. **不要复制粘贴竞品资料不带改写** — 抄袭对 SEO 和 GEO 都是负分
7. **不要写空话** — "性能强大""体验出色""值得拥有"等无信息含量句直接删
8. **不要忽略 NZ 本地化** — 价格、气候、物流、保修都要回到 NZ 视角
9. **不要在 Price 字段以外写精确价格数字** — 见下方"价格管理规则"

---

## 💰 价格管理规则（降低维护成本）

精确价格只出现在 **`Price` 字段一处**。其他字段用 **层级语言** 替代，避免改价时多处修改。

| 场景 | ❌ 不要写 | ✅ 改成 |
|---|---|---|
| Selling Points 提到本产品价格 | "lands at $2,399 inc GST" | "lands in the premium tier" |
| Comparison 提到本品牌相邻型号 | "Omni at $2,099 saves $300" | "Omni tier saves a moderate premium" |
| Comparison 提到竞品 | "vs Aeron ($2,800–$4,500 NZD)" | "vs Aeron at a meaningfully higher NZD tier" |
| Ideal For 提到预算 | "users with $2,400 budget" | "users in the premium ergonomic tier" |
| FAQ 提到本产品价格 | "is $2,399 worth it" | "is this premium-tier purchase justified" |

**例外**：
- `Price` 字段：精确数字（由 BC API 自动同步）
- `Schema.offers.price`：精确数字（结构化数据需要）
- 仓库知识库 `product-knowledge/{品类}/research/`：可以保留精确数字作为研究底稿

**层级词汇参考**（NZ 椅子品类）：
- entry-tier / 入门款
- value-tier / 性价比款
- mid-tier / 中端
- premium-tier / 高端
- flagship-tier / 旗舰

各品类可以定义自己的层级词，写入对应 `product-knowledge/{品类}/buying-guide.md`。

---

## ✅ 提交流程

1. 从 `TEMPLATE.md` 复制模板
2. 用 BC API 拉真实数据：`curl -H "X-Auth-Token: $BC_ACCESS_TOKEN" "$BC_API_BASE/catalog/products?sku:in={SKU}"`
3. 研究产品（厂商官网 + 品类知识库 `product-knowledge/`）
4. 填内容到对应的 `geo/{品类}/{BC SKU}.md`
5. 自查：每个字段是否达到 GEO 深度（具体数字 + 场景 + 本地化）
6. `git add` + `git commit` + `git push`

---

## ❓ 不确定怎么办

- 参数不确定 → BC API 拉数据，或查厂商官网
- 放到哪个品类不确定 → 查 `bc_categories_index.json`
- 要不要建新品类 → 先问 Jimmy
- 写不出深度内容 → 先研究 `product-knowledge/{品类}/` 知识库；没知识库的品类，先建知识库再写 GEO
