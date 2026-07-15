#!/usr/bin/env python3
"""
publish-blog.py — Publish or update a blog post to BC from a markdown file.

Usage:
    python tools/publish-blog.py blog/how-much-does-a-pc-cost-in-new-zealand.md
    python tools/publish-blog.py blog/how-much-does-a-pc-cost-in-new-zealand.md --draft
    python tools/publish-blog.py blog/how-much-does-a-pc-cost-in-new-zealand.md --update 42

Reads BC_BLOG_TOKEN from extremepc.env (same pattern as other tools).

Blog post markdown frontmatter format:
    # Title here
    **BC URL:** https://www.extremepc.co.nz/blog/{slug}/
    **目标问题:** ...
    **状态:** draft / published
    **发布日期:** YYYY-MM-DD
    **Meta Description:** ...
    **Tags:** tag1, tag2

    ---

    Body content starts here...
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

# === Load credentials ===
_env_candidates = [
    Path(os.environ.get("HERMES_PROFILE_DIR", "")) / "extremepc.env",
    Path.home() / "AppData/Local/hermes/profiles/exie/extremepc.env",
]
for _p in _env_candidates:
    if _p.exists():
        with open(_p) as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _k, _v = _line.split("=", 1)
                    os.environ.setdefault(_k.strip(), _v.strip())

STORE = os.environ.get("BC_STORE_HASH", "ms4wz8cgi2")
TOKEN = os.environ.get("BC_BLOG_TOKEN", "")
if not TOKEN:
    print("Error: BC_BLOG_TOKEN not set.", file=sys.stderr)
    print("Add BC_BLOG_TOKEN=your_token to extremepc.env", file=sys.stderr)
    sys.exit(1)

BASE = f"https://api.bigcommerce.com/stores/{STORE}/v2"
HEADERS = {
    "X-Auth-Token": TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# === Args ===
args = sys.argv[1:]
draft_mode = "--draft" in args
args = [a for a in args if not a.startswith("--draft")]

update_id = None
if "--update" in args:
    idx = args.index("--update")
    update_id = int(args[idx + 1])
    args = [a for a in args if a != "--update" and a != str(update_id)]

if not args:
    print("Usage: python tools/publish-blog.py <blog-file.md> [--draft] [--update <post_id>]")
    sys.exit(1)

md_file = Path(args[0])
if not md_file.exists():
    print(f"Error: file not found: {md_file}")
    sys.exit(1)


# === Parse markdown file ===
def parse_blog_md(path):
    content = path.read_text(encoding="utf-8")

    def extract_field(label):
        m = re.search(rf'\*\*{label}:\*\*\s*(.+)', content)
        return m.group(1).strip() if m else ""

    # Title = first H1
    title_m = re.search(r'^#\s+(.+)', content, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else path.stem

    # Body = everything after the --- separator
    parts = re.split(r'\n---\n', content, maxsplit=1)
    body_md = parts[1].strip() if len(parts) > 1 else content

    # Convert basic markdown to HTML (BC accepts HTML body)
    body_html = md_to_html(body_md)

    # Extract slug from BC URL field
    url_field = extract_field("BC URL")
    slug_m = re.search(r'/blog/([^/]+)/', url_field)
    slug = slug_m.group(1) if slug_m else path.stem

    meta_desc = extract_field("Meta Description")
    tags_raw  = extract_field("Tags")
    tags = [t.strip() for t in tags_raw.split(",")] if tags_raw else []
    raw_date  = extract_field("发布日期")
    if raw_date and re.match(r'^\d{4}-\d{2}-\d{2}$', raw_date):
        pub_date = time.strftime("%a, %d %b %Y %H:%M:%S +0000",
                                 time.strptime(raw_date, "%Y-%m-%d"))
    else:
        pub_date = time.strftime("%a, %d %b %Y %H:%M:%S +0000")

    return {
        "title":            title,
        "body":             body_html,
        "url":              slug,
        "meta_description": meta_desc,
        "tags":             tags,
        "published_date":   pub_date,
        "is_published":     not draft_mode,
        "author":           "ExtremePC",
    }


def md_to_html(md):
    """Minimal markdown → HTML conversion for BC blog body."""
    lines = md.split("\n")
    html_lines = []
    in_ul = False
    in_table = False

    for line in lines:
        # Headings
        if line.startswith("### "):
            if in_ul: html_lines.append("</ul>"); in_ul = False
            html_lines.append(f"<h3>{line[4:].strip()}</h3>")
        elif line.startswith("## "):
            if in_ul: html_lines.append("</ul>"); in_ul = False
            html_lines.append(f"<h2>{line[3:].strip()}</h2>")
        elif line.startswith("# "):
            if in_ul: html_lines.append("</ul>"); in_ul = False
            html_lines.append(f"<h1>{line[2:].strip()}</h1>")
        # Table rows
        elif line.startswith("|"):
            if not in_table:
                html_lines.append("<table>")
                in_table = True
            cells = [c.strip() for c in line.strip("|").split("|")]
            if all(re.match(r'^[-:]+$', c) for c in cells if c):
                continue  # skip separator row
            tag = "th" if not any("<td>" in l for l in html_lines[-3:]) else "td"
            row = "".join(f"<{tag}>{c}</{tag}>" for c in cells)
            html_lines.append(f"<tr>{row}</tr>")
        else:
            if in_table:
                html_lines.append("</table>")
                in_table = False
            # List items
            if line.startswith("- ") or line.startswith("* "):
                if not in_ul:
                    html_lines.append("<ul>")
                    in_ul = True
                item = inline_md(line[2:].strip())
                html_lines.append(f"<li>{item}</li>")
            else:
                if in_ul:
                    html_lines.append("</ul>")
                    in_ul = False
                if line.strip() == "":
                    html_lines.append("")
                else:
                    html_lines.append(f"<p>{inline_md(line)}</p>")

    if in_ul:   html_lines.append("</ul>")
    if in_table: html_lines.append("</table>")

    return "\n".join(html_lines)


def inline_md(text):
    """Convert inline markdown (bold, italic, links) to HTML."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*',     r'<em>\1</em>', text)
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    return text


# === API calls ===
def api_request(method, path, data=None):
    url = f"{BASE}{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"  [API Error {e.code}] {e.read().decode()}", file=sys.stderr)
        return None


# === Main ===
print(f"\n=== BC Blog Publisher ===")
print(f"  File   : {md_file}")
print(f"  Mode   : {'DRAFT' if draft_mode else 'PUBLISH'}")
if update_id:
    print(f"  Update : post ID {update_id}")
print()

post = parse_blog_md(md_file)
print(f"  Title  : {post['title']}")
print(f"  Slug   : {post['url']}")
print(f"  Tags   : {', '.join(post['tags']) or '(none)'}")
print()

if update_id:
    print(f"  Updating post {update_id}...")
    result = api_request("PUT", f"/blog/posts/{update_id}", post)
    action = "Updated"
else:
    print(f"  Creating new post...")
    result = api_request("POST", "/blog/posts", post)
    action = "Created"

if result:
    post_id  = result.get("id", "?")
    post_url = f"https://www.extremepc.co.nz/blog/{post['url']}/"
    print(f"  OK: {action} successfully!")
    print(f"  BC Post ID : {post_id}")
    print(f"  URL        : {post_url}")
    print()
    print(f"  Tip: to update later, run:")
    print(f"  python tools/publish-blog.py {md_file} --update {post_id}")
else:
    print(f"  FAILED. Check the error above.")
    sys.exit(1)
