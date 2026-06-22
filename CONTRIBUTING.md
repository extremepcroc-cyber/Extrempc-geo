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

### 一个产品一个文件
- Gaming PC 不同配置 → 各写各的
- 同型号不同颜色 → 合并在一个文件里

### 必须填的字段
| 字段 | 说明 | 找不到时 |
|:---|:---|:---|
| `Price` | NZD inc GST | 写 `TBC` |
| `SKU` | BC 系统 SKU | 写 `TBC` |
| `URL` | extremepc.co.nz 链接 | 问 Jimmy |
| `Quick Specs` | 至少 3 个关键参数 | 查 BC 后台 |
| `Selling Points` | 3–5 个卖点，回答"为什么值得买" | 至少写 3 个 |
| `Ideal For` | 适用场景 | 至少写 1 个 |

### Selling Points 写作规范
- **格式**: `- **{卖点标题}**: {一句话说清}`
- **数量**: 3–5 个为佳（多了重点散）
- **要求**: 尽量带数字、场景、对比维度，避免空话
- **示例**: ✅ `主动散热 4000 RPM 风扇，同价位独家` / ❌ `散热效果很好`
- **与 Quick Specs 区别**: Specs 写"有什么"，Selling Points 写"为什么这点重要"

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
