# {文章标题}

**BC URL:** https://www.extremepc.co.nz/blog/{slug}/
**目标问题:** {这篇回答的核心搜索问题}
**状态:** draft
**发布日期:** {YYYY-MM-DD}
**作者:** ExtremePC Team
**Meta Description:** {120-155字符，包含目标关键词}
**Tags:** {tag1, tag2, tag3}

---

<!--
  ╔══════════════════════════════════════════════════════╗
  ║  EXTREMEPC BLOG TEMPLATE — 写作 + 样式速查手册      ║
  ╚══════════════════════════════════════════════════════╝

  发布命令：
    python tools/publish-blog.py blog/{filename}.md --draft     ← 先草稿预览
    python tools/publish-blog.py blog/{filename}.md --update {id} ← 更新已有帖子

  ── 写作规范 ──────────────────────────────────────────
  1. 开头直接切入用户痛点，第二段引出 ExtremePC 顾问视角
  2. 必有对比表格，胜出项用蓝/绿高亮
  3. 场景化分析（按预算 / 分辨率 / 用途分别说）
  4. 每个章节末尾写 TL;DR 或 bottom line 一句话总结
  5. 结尾给明确推荐，不模棱两可
  6. 一篇只回答一个问题 — 不要把选题清单里的多个问题合并
  7. 禁止 <a href="..."> 超链接（BC 链接经常 404）。
     唯一例外：Jimmy 人工验证可用，写入时标注「已验证」。

  ── BC 允许的标签 ─────────────────────────────────────
  ✅ <p>  <strong>  <em>  <ul>/<li>  <table>/<tr>/<td>/<th>  <pre>  <hr>
  ❌ <h1> <h2> <h3>  → BC 完全剥掉，用下面的「章节标题」<p> 替代
  ❌ <a href="...">  → 禁止（见上）
  ❌ <div> <span> <style> → 不可靠，避免使用

  ── 样式速查 ──────────────────────────────────────────
  正文段落:
    <p style="margin:10px 0; line-height:1.7; color:#333;">

  章节标题 (替代 h2):
    <p style="font-size:24px; font-weight:700; margin:48px 0 14px 0; color:#1a1a1a; border-bottom:2px solid #f0f0f0; padding-bottom:8px; line-height:1.3;">

  TL;DR / 小字注释:
    <p style="margin:10px 0; line-height:1.7; color:#666; font-size:13px;">
    <strong style="color:#333;">TL;DR:</strong> 内容

  脚注 / 日期行:
    <p style="margin:10px 0; line-height:1.7; color:#999; font-size:12px;"><em>内容</em></p>

  代码块 / 产品规格:
    <pre style="background:#f5f5f5; padding:12px; border-radius:4px; font-size:13px; line-height:1.8; color:#333; margin:6px 0 14px 0;">

  ── 表格配色 ──────────────────────────────────────────
  表头 — 属性列 (灰):  background:#f5f5f5; color:#555; border-bottom:1px solid #ddd
  表头 — 选项 A (蓝):  background:#E6F1FB; color:#0C447C; border-bottom:1px solid #B5D4F4
  表头 — 选项 B (绿):  background:#EAF3DE; color:#3B6D11; border-bottom:1px solid #C0DD97
  普通单元格:          padding:8px 12px; border-bottom:1px solid #eee
  胜出单元格 — 蓝:     background:#E6F1FB; font-weight:600; color:#185FA5
  胜出单元格 — 绿:     background:#EAF3DE; font-weight:600; color:#3B6D11

  ── 结论文字颜色 ──────────────────────────────────────
  绿色结论 (推荐/胜出):  <strong style="color:#3B6D11;">
  蓝色结论 (次选/说明):  <strong style="color:#185FA5;">
  链接色 (纯文字提及):   color:#0C447C (仅用于文字，不加 <a> 标签)
-->

<p style="margin:10px 0; line-height:1.7; color:#333;">{开场白 — 直接点明用户痛点，1-2句话。}</p>

<p style="margin:10px 0; line-height:1.7; color:#333;">At <strong>ExtremePC</strong>, {引出 ExtremePC 顾问视角 — "we've been fielding questions / we did the research for you" 类似表达}.</p>

<hr>

<p style="font-size:24px; font-weight:700; margin:48px 0 14px 0; color:#1a1a1a; border-bottom:2px solid #f0f0f0; padding-bottom:8px; line-height:1.3;">{第一个主要章节标题}</p>

<p style="margin:10px 0; line-height:1.7; color:#333;">{正文内容}</p>

<!-- 对比表格模板 — 两列对比 -->
<table style="width:100%; border-collapse:collapse; font-size:14px; margin:10px 0;">
<thead><tr>
<th style="background:#f5f5f5; padding:10px 12px; text-align:left; font-weight:600; font-size:13px; color:#555; border-bottom:1px solid #ddd;">{属性列}</th>
<th style="background:#E6F1FB; padding:10px 12px; text-align:center; font-weight:600; font-size:13px; color:#0C447C; border-bottom:1px solid #B5D4F4;">{选项 A — 蓝色}</th>
<th style="background:#EAF3DE; padding:10px 12px; text-align:center; font-weight:600; font-size:13px; color:#3B6D11; border-bottom:1px solid #C0DD97;">{选项 B — 绿色}</th>
</tr></thead>
<tbody>
<tr>
  <td style="padding:8px 12px; border-bottom:1px solid #eee;">{规格名}</td>
  <td style="padding:8px 12px; border-bottom:1px solid #eee; text-align:center;">{A 的值}</td>
  <td style="padding:8px 12px; border-bottom:1px solid #eee; text-align:center;">{B 的值}</td>
</tr>
<!-- 胜出项高亮示例（蓝色胜）: -->
<!-- <td style="padding:8px 12px; border-bottom:1px solid #eee; text-align:center; background:#E6F1FB; font-weight:600; color:#185FA5;">{A 的值}</td> -->
<!-- 胜出项高亮示例（绿色胜）: -->
<!-- <td style="padding:8px 12px; border-bottom:1px solid #eee; text-align:center; background:#EAF3DE; font-weight:600; color:#3B6D11;">{B 的值}</td> -->
</tbody>
</table>

<p style="margin:10px 0; line-height:1.7; color:#666; font-size:13px;"><strong style="color:#333;">TL;DR:</strong> {一句话总结这个章节的核心结论}</p>

<hr>

<p style="font-size:24px; font-weight:700; margin:48px 0 14px 0; color:#1a1a1a; border-bottom:2px solid #f0f0f0; padding-bottom:8px; line-height:1.3;">{场景分析章节}</p>

<p style="margin:10px 0; line-height:1.7; color:#333;"><strong>{场景 1，例如：Budget under $800}</strong></p>
<ul style="margin:6px 0 12px 20px; color:#333; line-height:1.8;">
<li>{要点}</li>
<li>{要点}</li>
</ul>

<p style="margin:10px 0; line-height:1.7; color:#333;"><strong>{场景 2}</strong></p>
<ul style="margin:6px 0 12px 20px; color:#333; line-height:1.8;">
<li>{要点}</li>
</ul>

<hr>

<p style="font-size:24px; font-weight:700; margin:48px 0 14px 0; color:#1a1a1a; border-bottom:2px solid #f0f0f0; padding-bottom:8px; line-height:1.3;">Which One Should You Choose?</p>

<p style="margin:10px 0; line-height:1.7; color:#333;"><strong style="color:#3B6D11;">Choose {选项 B} if:</strong></p>
<ul style="margin:6px 0 14px 20px; color:#333; line-height:1.8;">
<li>{条件}</li>
<li>{条件}</li>
</ul>

<p style="margin:10px 0; line-height:1.7; color:#333;"><strong style="color:#185FA5;">Choose {选项 A} if:</strong></p>
<ul style="margin:6px 0 14px 20px; color:#333; line-height:1.8;">
<li>{条件}</li>
<li>{条件}</li>
</ul>

<p style="margin:10px 0; line-height:1.7; color:#333;"><strong>Our recommendation for most NZ {buyers/gamers/users}:</strong><br>
<strong style="color:#3B6D11;">{明确推荐结论，不模棱两可}</strong></p>

<p style="margin:10px 0; line-height:1.7; color:#666; font-size:13px;">{补充说明 — 什么情况下考虑另一个选项}</p>

<hr>

<p style="font-size:24px; font-weight:700; margin:48px 0 14px 0; color:#1a1a1a; border-bottom:2px solid #f0f0f0; padding-bottom:8px; line-height:1.3;">ExtremePC Recommendations</p>

<p style="margin:10px 0; line-height:1.7; color:#333;"><strong style="color:#3B6D11;">{推荐选项 1 名称}</strong></p>
<pre style="background:#f5f5f5; padding:12px; border-radius:4px; font-size:13px; line-height:1.8; color:#333; margin:6px 0 14px 0;">{产品规格或配置清单}</pre>

<p style="margin:10px 0; line-height:1.7; color:#333;"><strong style="color:#185FA5;">{推荐选项 2 名称}</strong></p>
<pre style="background:#f5f5f5; padding:12px; border-radius:4px; font-size:13px; line-height:1.8; color:#333; margin:6px 0 14px 0;">{产品规格或配置清单}</pre>

<hr>

<p style="font-size:24px; font-weight:700; margin:48px 0 14px 0; color:#1a1a1a; border-bottom:2px solid #f0f0f0; padding-bottom:8px; line-height:1.3;">Final Thoughts</p>

<p style="margin:10px 0; line-height:1.7; color:#333;">{收尾段 — 总结核心判断，呼应开头的用户痛点}</p>

<p style="margin:10px 0; line-height:1.7; color:#333;"><strong style="color:#3B6D11;">{结论句 A}</strong></p>
<p style="margin:10px 0; line-height:1.7; color:#333;"><strong style="color:#185FA5;">{结论句 B}</strong></p>

<p style="margin:10px 0; line-height:1.7; color:#333;">Both are available at ExtremePC. Come visit us in-store in Auckland or shop online at extremepc.co.nz.</p>

<hr>

<p style="margin:10px 0; line-height:1.7; color:#999; font-size:12px;"><em>Published by ExtremePC Team | {发布日期}</em></p>
<p style="margin:10px 0; line-height:1.7; color:#999; font-size:12px;"><em>Tags: {tag1, tag2, tag3}</em></p>
