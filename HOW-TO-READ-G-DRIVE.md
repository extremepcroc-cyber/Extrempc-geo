# 🚀 G: 盘文件读取指南（给 AI Agent 看）

> **适用对象**: 所有在 Windows 上需要读 G: 盘（Google Drive 映射盘）的 AI Agent
>
> **TL;DR**: 别用 `read_file` 工具，用 Python 的 `open()` 绕路

---

## ❌ 错误做法（读不到）

如果你的工具集里有个 `read_file` 或类似的"读文件"工具，直接给它 G: 盘路径会报错：

```
read_file(path='G:\\My Drive\\...\\README.md')
→ File not found ❌
```

原因是 G: 盘是 Google Drive 映射的虚拟文件系统，工具不一定认识这种重解析点。

---

## ✅ 正确做法（能读到）

用 Python 的 `open()` 直接绕开工具层，走系统底层 API：

### 方法一：用 `execute_code` 工具（推荐）

```python
# 读一个文件
with open(r'G:\My Drive\openclaw\workspace\tasks\extremepc\geo\README.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 可以读完之后截断显示，避免上下文爆炸
print(content[:2000])
```

### 方法二：用 `terminal` 工具执行 Python

```bash
python -c "
with open(r'G:\My Drive\openclaw\workspace\tasks\extremepc\geo\README.md', 'r', encoding='utf-8') as f:
    print(f.read()[:2000])
"
```

---

## 📁 这个仓库的文件结构

```
G:\My Drive\openclaw\workspace\tasks\extremepc\geo\
├── AI-README.md          ← AI 先读我
├── README.md             ← 目录索引
├── TEMPLATE.md           ← 产品文件模板
├── CONTRIBUTING.md       ← 协作规范
├── CLAUDE.md             ← Claude 配置
├── .env                  ← BC API 凭据（不用读）
├── gaming-pcs/           ← Gaming PCs
├── gaming-mice/          ← Gaming Mice
├── gaming-keyboards/     ← Gaming Keyboards
├── gaming-headsets/      ← Gaming Headsets
├── monitors/             ← Monitors
├── video-cards/          ← GPU
├── cpu-processors/       ← CPU
├── internal-ssd/         ← Internal SSD
├── memory-ram/           ← Memory / RAM
├── cooling/              ← Cooling
├── power-supplies/       ← PSU
├── motherboards/         ← Motherboards
├── laptops/              ← Laptops
├── streaming-creator/    ← Streaming & Creator
├── networking/           ← Networking
├── storage/              ← Storage
└── brands/               ← 独家代理品牌
```

---

## 🔁 通用模板（复制即用）

```python
import os

def read_gdrive(relative_path):
    """从 G: 盘 GEO 仓库读取文件"""
    base = r'G:\My Drive\openclaw\workspace\tasks\extremepc\geo'
    full_path = os.path.join(base, relative_path)
    
    with open(full_path, 'r', encoding='utf-8') as f:
        return f.read()

# 使用示例
content = read_gdrive('README.md')
print(content[:2000])
```

---

## 📝 注意事项

1. **路径用 `r'...'` 原始字符串** — 避免反斜杠转义问题
2. **编码用 `utf-8`** — 文件都是 UTF-8 编码
3. **文件内容是 Markdown** — 每个产品一个 `.md` 文件，文件名 = BC SKU（全大写）
4. **太多内容记得截断** — `print(content[:2000])` 防止刷爆上下文
5. **`os.listdir()` 也可以正常用** — 列目录、找文件都没问题

---

*最后更新: 2026-06-29*
*编写: Hermes Agent @ ExtremePC GEO Team*
