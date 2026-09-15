# GEO 协作规范

**适用对象**: 所有写 GEO 文件的同事（人类）
**目的**: 让仓库保持整洁，文件一致，减少 review 成本

> ⚠️ **本文件是人类协作的快速参考，不是权威规则来源。** 详细规则（文件模板、批量生成禁令、价格格式、EOL/OOS/墓碑处理、工具用法）以 `CLAUDE.md` 和 `tools/hermes-skill-*.md` 系列文件为准——这里只给指路和几条人类容易忽略的注意事项，**不重复抄写细节**，避免两边内容各自改、越改越不一致（这个仓库已经因为这个问题踩过坑）。

---

## 📁 目录结构

当前实际存在的目录以 `find . -maxdepth 1 -type d` 或 `README.md` 的目录树为准——**不要凭记忆或本文件的旧版本假设某个目录存在**，仓库一直在新增分类目录（比如这次新增了 `gaming-chairs/`、`internal-hard-drives/`、`webcams/`、`microphones/`、`2-EOL products/`、`company/`）。

品类目录对应的 BC 分类 ID 表见 `CLAUDE.md`「Category Directory → BC IDs」。

### 新增目录流程
1. 确认 BC 上有对应的品类
2. 先在 `README.md` 的索引里加上
3. 再建目录

---

## 📝 写文件前必读

**写 GEO 产品文件（不是博客）前，先读 `tools/hermes-skill-geo-writing.md`** —— 完整的模板结构、每个字段的要求、批量生成禁令、写完后的自查清单都在这一份文件里，本文件不重复列出，避免抄错或过期。

**写博客前，读 `tools/hermes-skill-blog-writing.md`。**

**要核对价格/库存，或者想知道某个品类还缺多少文件没写，读 `tools/hermes-skill-audit-tools.md`** —— 里面有 `audit-geo.py`（价格库存审计）和 `coverage-report.py`（覆盖率查询）两个工具的完整用法。

---

## ⚠️ 下架产品 — 不要删除文件

**产品从 BC 完全下架（不是缺货，是 SKU 查不到了）时，不要删除对应的 GEO 文件。**

正确做法：移动到 `2-EOL products/{原品类}/{SKU}.md`，在 URL 字段下面加一行 `**Status:** EOL — removed from BC catalog on {日期}`，其余内容原样保留。原因：写这些内容花了很多功夫，直接删除是白费；而且 BC 上的商品有时候会重新上架（改名、复产等），到时候还能直接用。

完整规则见 `CLAUDE.md`「Product Removed From BigCommerce Entirely (EOL)」。

---

## 🪦 缺货产品

- 短期缺货 → 保留完整 GEO 内容，加一行 `**Status:** OUT OF STOCK` 状态，Schema 改 `OutOfStock`——**不要删除任何已写内容**
- 从未写过完整内容、刚发现缺货的新 SKU → 墓碑占位文件

完整规则和模板见 `CLAUDE.md`「Out-of-Stock Products」。

---

## 💰 价格格式

**`**Price:**` 字段用纯整数，不带千位逗号，不带小数** —— 例如 `$2399 inc GST`，不是 `$2,399.00 inc GST`。这是 2026-09-15 确立的规则；这之前写的旧文件保留原样，不用主动去改，但新写的文件和你改动的价格一律用新格式。`Schema.offers.price` 不受影响，照常用带小数的字符串（如 `"2399.00"`）。

**正文里（Selling Points、Comparison 等）不写具体金额或价差**，用档位语言（entry-tier / mid-tier / premium-tier）代替。原因：价格会变，写死的数字和价差没人会同步更新，等 BC 价格一变这句话就悄悄变成假话。精确数字只出现在 `Price` 字段和 `Schema.offers.price`。

---

## ✅ 提交前检查

- [ ] 文件名 = BC SKU，全大写
- [ ] 放在正确的品类目录
- [ ] Price、SKU、URL 都填了（或标注 `TBC`）
- [ ] 没有中文文件名
- [ ] 格式和模板一致（跑一遍 `tools/hermes-skill-geo-writing.md` 里的 Self-Check 清单）
- [ ] 没有抄袭/批量生成痕迹
- [ ] BC 后台能查到对应 SKU

## 🤝 提交流程

```
git add {品类目录}/
git commit -m "feat: write GEO files for {子品类} ({n} SKUs)"
git push
```

一个子品类一次提交，不要把多个品类混在一次提交里。
