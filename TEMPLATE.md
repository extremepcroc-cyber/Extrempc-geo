# GEO 产品文件模板

> 每个产品一个文件，放在对应的品类目录下。
> 不要改结构，不要改格式，填内容就行。

---

```markdown
# {产品名}

**Price:** ${价格} inc GST
**SKU:** {SKU}
**URL:** https://www.extremepc.co.nz/{slug}/

## Quick Specs
- {规格 1}
- {规格 2}
- {规格 3}

## Ideal For
- {适用场景 1}
- {适用场景 2}

## Comparison
- vs {竞品 A}: {差异说明}
- vs {竞品 B}: {差异说明}

## Related Products
- {相关产品 1}
- {相关产品 2}

## Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{产品名}",
  "brand": "{品牌}",
  "offers": {
    "@type": "Offer",
    "price": "{价格}",
    "priceCurrency": "NZD"
  }
}
```
```

---

## 📏 命名规范

```
{SKU}.md
```

**规则**:
- 文件名 = BC 系统 SKU，全大写
- 一个文件 = 一个 SKU
- 同型号不同颜色 → 放在一个文件
- 不含中文、空格、特殊字符

**示例**:
- ✅ `XPC1129.md`
- ✅ `MONSAM27FG7.md`
- ✅ `MONASRPGO27QFV.md`
- ❌ `samsung-odyssey-g70f.md`
- ❌ `Enshrouded PC.md`
- ❌ `三星G70F.md`

---

## ❌ 不允许做的事

1. **不要改目录结构** — 品类文件夹不能改名、不能合并、不能删
2. **不要自己建新目录** — 新品类先问 Jimmy，确定加在哪
3. **不要写中文文件名** — 全英文 slug
4. **不要加自己的格式** — 严格按照模板的 section 标题和顺序
5. **不要遗漏字段** — Price、SKU、URL 必须有，不知道的写 `TBC`
6. **不要复制粘贴竞品资料不带改写** — 给搜索引擎看的，抄袭影响 SEO

---

## ✅ 提交流程

1. 从 `TEMPLATE.md` 复制模板
2. 填内容到对应的 `geo/{品类}/{产品}.md`
3. 本地检查格式
4. `git add` + `git commit` + `git push`
5. （可选）在 PR 描述里写：新品 / 改价 / 改规格

---

## ❓ 不确定怎么办

- 参数不确定 → 查 BC 后台或问 Jimmy
- 放到哪个品类不确定 → 查 `category-reference.md`
- 要不要建新品类 → 先问
