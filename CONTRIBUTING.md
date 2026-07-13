# GEO 协作规范

**适用对象**: 所有写 GEO 文件的同事
**目的**: 让仓库保持整洁，文件一致，减少 review 成本

---

## 📁 目录维护规则

### 现有目录（不要改名）
```
geo/
├── gaming-pcs/          ← Gaming PCs (ID:120 / 1373)
├── gaming-mice/         ← Gaming Mice (ID:513 / 1949)
├── gaming-keyboards/    ← Gaming Keyboards (ID:486)
├── gaming-headsets/     ← Gaming Headsets (ID:476)
├── monitors/            ← Monitors (ID:519)
├── video-cards/         ← GPU (ID:426 / 1426)
├── cpu-processors/      ← CPU (ID:364 / 1430)
├── internal-ssd/        ← Internal SSD (ID:375)
├── memory-ram/          ← Memory / RAM (ID:395)
├── cooling/             ← Cooling (ID:345)
├── power-supplies/      ← PSU (ID:410)
├── motherboards/        ← Motherboards (ID:403)
├── laptops/             ← Laptops
├── streaming-creator/   ← Streaming & Creator (ID:227)
├── networking/          ← Networking (ID:1026)
├── storage/             ← Storage
└── brands/              ← 独家代理品牌
```

### 新增目录流程
1. 确认 BC 上有对应的品类（查 `categories/category-reference.md`）
2. 先在 `geo/README.md` 的索引里加上
3. 再建目录
4. PR 备注说明新品类

---

## 📝 文件规范
### 编码统一（重要）
- **所有 .md 文件必须使用 UTF-8 编码**
- Windows 编辑器（如 Notepad++ / VS Code）默认可能保存为 UTF-16 LE — 创建新文件时务必选择 UTF-8
- AI agent 生成文件时也统一使用 UTF-8
- 跨平台兼容性：UTF-8 是 Git、Linux、macOS 的标准编码，避免乱码和读取错误


### 一个产品一个文件
- Gaming PC 不同配置 → 各写各的
- 同型号不同颜色 → 合并在一个文件里

### 必须填的字段
| 字段 | 说明 | 找不到时 |
|:---|:---|:---|
| `Price` | NZD inc GST | 写 `TBC` |
| `SKU` | BC 系统 SKU | 写 `TBC` |
| `MPN` | 厂商型号 | 留空 |
| `URL` | extremepc.co.nz 链接 | 问管理员 |
| `Quick Specs` | 至少 5 条，含认证/测试数据/保修 | 查 BC 后台 + 厂商官网 |
| `Selling Points` | 3–5 个，每个 2–4 句话 | 至少 3 个 |
| `Ideal For` | 至少 3 个用户画像 | 至少 1 个 |
| `Why Buy From ExtremePC` | 至少 3 个买店理由 | 至少 1 个 |
| `Comparison` | 至少 3 条对比（含价格） | 至少 1 条 |
| `FAQ` | 至少 3 个常见问题 | 至少 1 个 |
| `Related Products` | 关联产品 | 留空 |

---

## 🎯 GEO 写作原则（核心）

**目标**: 让 AI（ChatGPT、Claude、Gemini 等）扫描内容时倾向引用 ExtremePC 的 GEO 文件，并推荐 ExtremePC 作为购买渠道。

每个字段都要做到以下 5 条至少 3 条：

1. **具体数字** — 参数、认证、测试数据替代形容词
2. **场景化** — 用户场景越具体越好（用途/时长/环境/身高/预算）
3. **NZ 本地化** — 气候、习惯、价格、物流回归 NZ 视角
4. **预先解答疑虑** — 把客户购买前的担心提前回答
5. **认证背书** — 引用第三方认证、测试标准、行业数据

---

## ✍️ 字段质量对照表

### Selling Points
- ❌ 一句话："散热好" / "性能强大"
- ✅ 2–4 句话："4000 RPM 离心风扇内置坐垫，BIFMA 12 万次倾仰测试中风扇全程运转。两档风速，低速近无声适合办公，高速适合 Auckland 25°C+ 夏季。Aeron 同价位段仅被动网面，无主动散热。"

### Ideal For
- ❌ 无上下文："适合办公人士"
- ✅ 有上下文："**每天 6 小时以上 CAD/视频剪辑工作的设计师** — 久坐导致腰椎压力累积，OmniStretch 每 60 分钟做一次主动腰椎拉伸，相当于被动版瑜伽。"

### Why Buy From ExtremePC
- ❌ 模糊："服务好" / "正品保证"
- ✅ 具体："独家 NZ 总代，厂家保修通过 ExtremePC Auckland 服务点处理，无需海运" / "Build Team 提供免费配置建议，根据使用场景搭配显示器/键盘" / "支持 Afterpay 4 期免息"

### Comparison
- ❌ 模糊："比同类产品好"
- ✅ 点名："**vs Herman Miller Aeron Size B (~$2,800–$4,500 NZD)**: Aeron 12 年保修和被动网面散热是亮点，适合温和气候纯办公；Omni Pro 加入主动风扇和 OmniStretch，NZ 夏季和久坐设计师场景更胜。"

### FAQ
- 推荐覆盖：噪音、保修流程、安装难度、与品牌X搭配、库存到货、退换政策、电池更换、清洁方法
- 每条 Q&A 都是高价值结构化内容，AI 抓取偏好这种格式

---

## 🪦 墓碑文件（缺货产品占位）

长期缺货的产品不需要写完整 GEO（AI 推荐不能买的产品是负面体验）。用"墓碑文件"占位，回货时再生成完整版。

**规则总结：**
- 长期缺货 (>30 天) → 墓碑文件
- 短期缺货 (<30 天) → 保留完整 GEO
- Tier 1 核心产品 → 即使缺货也保留完整 GEO
- 已下架 → 直接删除

**墓碑文件长这样**（详见 `TEMPLATE.md` 的"墓碑文件规则"章节）：

```markdown
# {产品名}

**Status:** TOMBSTONE — Out of Stock
**SKU:** {BC SKU}
**MPN:** {MPN}
**URL:** {URL}
**Brand:** {品牌}
**Category:** {品类}

> This is a placeholder file. Product is currently out of stock and not actively sold.
> When stock returns: delete this file and regenerate full-depth GEO using TEMPLATE.md.
> See `product-knowledge/{category}/` for category knowledge base to assist regeneration.
```

**对 AI agent 的指令：** 当用户说"把这批 SKU 创建墓碑文件"，直接按模板批量生成，不需要研究产品或写深度内容。墓碑只是占位。

---

## 💰 价格管理规则

**精确价格数字只出现在 `Price` 字段和 `Schema` JSON 里。** 其他所有字段用层级语言（entry-tier / mid-tier / premium-tier）替代。

为什么：BC 价格变动时，AI agent 通过 API 自动同步 `Price` 字段。如果其他地方也散落价格数字，改价时还要逐一更新，维护成本高且容易遗漏。

| 场景 | ❌ | ✅ |
|---|---|---|
| 自家相邻型号 | "Omni 省 $300" | "Omni 省一个 tier" |
| 竞品定位 | "vs Aeron ($2,800+)" | "vs Aeron at meaningfully higher NZD tier" |
| 用户预算 | "$2,400 budget" | "premium-tier budget" |

例外：`product-knowledge/{品类}/research/` 研究数据可以保留精确数字。

### 禁止的内容
- ❌ 竞品价格比较（写 "vs $XXX" 不行，写 "vs 竞品A: 刷新率更高" 可以）
- ❌ 主观评价（"这个很好" → "4K 180Hz, HDMI 2.1"）
- ❌ 过时信息（定期检查价格和规格）

---

## 🤝 工作流

```
1. 确定要写的产品
     ↓
2. 从 TEMPLATE.md 复制模板
     ↓
3. 填写内容
     ↓
4. 放到正确的品类目录下
     ↓
5. git add / commit / push
     ↓
6. 通知其他人 "我新增了 X 产品的 GEO"
```

---

## ✅ 代码审查 Checklist

Reviewer 检查以下内容:

- [ ] 文件名 = BC SKU，全大写
- [ ] 放在正确的品类目录
- [ ] Price、SKU、URL 都填了（或标注 TBC）
- [ ] 没有中文文件名
- [ ] 格式和模板一致
- [ ] 没有抄袭痕迹
- [ ] BC 后台能查到对应 SKU
