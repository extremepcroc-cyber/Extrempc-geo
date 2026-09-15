# Skill: ExtremePC Blog Writing & Publishing

**Trigger:** Any task involving writing or publishing a blog post to extremepc.co.nz. Unrelated to GEO product files — do not read this for a product-writing task, and don't read `hermes-skill-geo-writing.md` for a blog task, they don't overlap.

---

## File Structure

```
blog/
  TEMPLATE.md                  ← start every new post from here
  内容选题清单.md               ← topic priorities (P1–P5)
  {slug}.md                    ← one file per post, named by BC URL slug
tools/
  publish-blog.py              ← publishes/updates post to BC Blog API
```

---

## Publish Workflow

1. Copy `blog/TEMPLATE.md` → `blog/{slug}.md`
2. Fill in frontmatter (Title H1, BC URL, 发布日期, Meta Description, Tags)
3. Write body in HTML (not markdown — BC strips most HTML tags except `<p>`, `<table>`, `<ul>/<li>`, `<strong>`, `<em>`, `<pre>`, `<hr>`)
4. Publish: `python tools/publish-blog.py blog/{slug}.md --draft` (preview first)
5. Review on BC admin, then: `python tools/publish-blog.py blog/{slug}.md --update {post_id}`
6. `git add` → `git commit` → `git push`

Requires `BC_BLOG_TOKEN` (Content permission scope) set in `extremepc.env`. **Never commit this token to git.**

---

## BC HTML Tag Restrictions — Verified Behavior

BC's blog editor strips or ignores these tags — **do not use them**:

| Tag | Behavior |
|---|---|
| `<h1>` `<h2>` `<h3>` | **Stripped entirely** — content becomes unstyled body text |
| `<a href="...">` | Rendered but links often 404 — **forbidden** unless Jimmy verifies the URL |

**Use instead:**
- Section headings → `<p style="font-size:24px; font-weight:700; margin:48px 0 14px 0; ...">` (see TEMPLATE.md)
- Links → plain text only

---

## Known Issues Fixed

- **BOM encoding**: PowerShell writes UTF-8 with BOM by default — `publish-blog.py` reads with `utf-8-sig` to strip it. Always write `.md` files with UTF-8 no-BOM.
- **H2 stripped**: BC removes `<h2>` tags. Use styled `<p>` tags for all section headings.
- **HTML pass-through**: `publish-blog.py` detects if body starts with `<` and skips the markdown converter — body must be pure HTML, not mixed.
- **Date format**: BC Blog API requires RFC-2822 (`Tue, 15 Jul 2026 00:00:00 +0000`). Script converts from `YYYY-MM-DD` automatically.

---

## Blog Writing Rules

1. One question per post — deep analysis, not a list of answers
2. Open with the user's pain point; second paragraph introduces ExtremePC's perspective
3. Always include a comparison table with blue/green color coding (see TEMPLATE.md)
4. Scenario-based sections (by budget / resolution / use case)
5. Clear recommendation at the end — no hedging
6. Inline CSS only — no external stylesheets
7. **No `<a href>` links** in body — plain text only. Exception: Jimmy-verified URLs only, annotated with "已验证"
8. No `<h2>` / `<h3>` tags — use styled `<p>` for headings
