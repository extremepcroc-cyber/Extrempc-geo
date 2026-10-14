#!/usr/bin/env python3
"""GEO file linter (rules only, no BC access).

Usage:
  python tools/geo-lint.py FILE [FILE ...]       lint specific files
  python tools/geo-lint.py --category cooling    lint one category directory
  python tools/geo-lint.py --all                 lint every GEO file
  python tools/geo-lint.py --all --summary       per-rule counts only
  python tools/geo-lint.py --all --rule R3       only show one rule

Exit code 1 if any ERROR is found. WARN = needs a human/BC check.
"""
import argparse
import collections
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {'tools', 'product-knowledge', 'brands', 'blog', 'company', '2-EOL products', 'node_modules'}
SKIP_NAMES = {'README', 'PROGRESS', 'QUEUE', 'TEMPLATE', 'CLAUDE', 'CONTRIBUTING', 'HERMES'}


def geo_files(category=None):
    out = []
    for d in sorted(p for p in ROOT.iterdir() if p.is_dir() and not p.name.startswith('.') and p.name not in SKIP_DIRS):
        if category and d.name != category:
            continue
        for f in sorted(d.glob('*.md')):
            if f.stem.upper() == f.stem and f.stem not in SKIP_NAMES:
                out.append(f)
    return out


def all_stems():
    s = set()
    for p in ROOT.rglob('*.md'):
        if '.git' in p.parts:
            continue
        s.add(p.stem.upper())
    return s


def eol_stems():
    return {p.stem.upper() for p in (ROOT / '2-EOL products').rglob('*.md')} if (ROOT / '2-EOL products').exists() else set()


def section(text, name):
    m = re.search(r'^## ' + name + r'[^\n]*\n(.*?)(?=^## |\Z)', text, flags=re.M | re.S)
    return m.group(1) if m else ''


def body_without_header_and_schema(text):
    t = re.sub(r'^## Schema.*', '', text, flags=re.M | re.S)
    return '\n'.join(l for l in t.split('\n') if not re.match(r'\*\*(Price|SKU|MPN|URL|Status|Brand|Category):\*\*', l))


# (id, level, description, regex over body lines)
LINE_RULES = [
    ('R3', 'ERROR', 'hardcoded dollar amount in prose (use tier language)', re.compile(r'\$\s?\d')),
    ('R4', 'ERROR', 'in-store testing / inspection promise', re.compile(r'(tested|test(ing)?|inspected|checked) (in[- ]store|before (dispatch|pickup|sale|shipping))|we (test|inspect)|in-store (test|demo)', re.I)),
    ('R5', 'ERROR', 'unverified store/stock claim (Wellington, warehouse, unit counts)', re.compile(r'Wellington|\b\d+ units\b|warehouse (stock|availability)|Last verified|Pricing at ExtremePC', re.I)),
    ('R6', 'WARN', 'store-range / market superlative (needs evidence)', re.compile(r'\b(cheapest|most affordable|lowest[- ]priced?|best[- ]value|one of the best|best[^.\n]{0,25}on the (NZ )?market|(NZ|New Zealand)[- ]market|only NZ retailer|undercuts|unbeatable|class-leading|longest (warranty|in))\b', re.I)),
    ('R7', 'WARN', 'invented-measurement phrasing', re.compile(r'real-world (usage|battery|life)|approximately \d+(\.\d+)? ?(hours|hrs|dB|mm|g)\b|\bestimated\b|~\s?\d', re.I)),
    ('R9', 'ERROR', 'scientific-notation or malformed price', re.compile(r'\$\s?\d+(\.\d+)?e[+-]?\d+|\$\d{1,3},\d{3}\.\d{2}', re.I)),
]
WARRANTY_ON = False  # R13 is opt-in: --warranty or --rule R13
WARRANTY = re.compile(r'(\d+|one|two|three|five|six|ten)[\s-]*(years?|yrs?|months?)\b[^.\n]{0,40}warrant|warrant[^.\n]{0,60}?(\d+|one|two|three|five|six|ten)[\s-]*(years?|yrs?|months?)\b', re.I)
NEUTRAL_W = re.compile(r'term set by the manufacturer', re.I)


def lint(path):
    issues = []
    text = path.read_text(encoding='utf-8-sig', errors='replace').replace('\r\n', '\n')
    stem = path.stem

    def add(rid, level, msg, line=0):
        issues.append((rid, level, line, msg))

    if re.search(r'^\*\*Status:\*\*\s*TOMBSTONE', text, flags=re.M):
        return issues

    # R1 header
    sku = re.search(r'^\*\*SKU:\*\*\s*(\S+)', text, flags=re.M)
    for key in ('Price', 'SKU', 'MPN', 'URL'):
        if not re.search(rf'^\*\*{key}:\*\*\s*\S', text, flags=re.M):
            add('R1', 'ERROR', f'missing **{key}:** header line')
    if sku and sku.group(1).upper() != stem:
        add('R1', 'ERROR', f'SKU header {sku.group(1)} != filename {stem}')
    # R2 price format
    pm = re.search(r'^\*\*Price:\*\*\s*(.*)$', text, flags=re.M)
    price_hdr = None
    if pm:
        v = pm.group(1).strip()
        if re.fullmatch(r'\$\d+ inc GST', v):
            price_hdr = int(re.search(r'\d+', v).group(0))
        elif v.upper().startswith('TBC'):
            pass
        else:
            add('R2', 'WARN', f'price not plain-integer form: {v[:40]}')
    # R8 related
    rel = section(text, 'Related Products')
    for m in re.finditer(r'\(([A-Z][A-Z0-9]{5,})\)|^- \**([A-Z][A-Z0-9]{5,})\b', rel, flags=re.M):
        t = m.group(1) or m.group(2)
        if t[:3] not in PREFIXES:
            continue
        if t == stem:
            add('R8', 'ERROR', f'Related Products lists the file itself ({t})')
        elif t not in STEMS and t not in {'NZ', 'NZD', 'GST', 'RGB', 'ARGB', 'LIGHTSPEED', 'HyperSpeed'} and len(t) >= 6:
            add('R8', 'WARN', f'Related SKU {t} has no file in the repo')
        elif t in EOL and t != stem:
            add('R8', 'WARN', f'Related SKU {t} is EOL')
    # R10 schema
    sm = re.search(r'```json\s*(\{.*?\})\s*```', text, flags=re.S)
    if sm:
        sch = sm.group(1)
        pr = re.search(r'"price":\s*"([^"]*)"', sch)
        if pr:
            if not re.fullmatch(r'\d+\.\d{2}', pr.group(1)):
                add('R10', 'ERROR', f'Schema price not decimal string: {pr.group(1)}')
            elif price_hdr is not None and round(float(pr.group(1))) != price_hdr:
                add('R10', 'ERROR', f'Schema price {pr.group(1)} != header ${price_hdr}')
        oos = re.search(r'^\*\*Status:\*\*\s*OUT OF STOCK', text, flags=re.M) is not None
        av = re.search(r'schema\.org/(\w+)', sch)
        if av and ((av.group(1) == 'OutOfStock') != oos):
            add('R10', 'ERROR', f'Status line says {"OOS" if oos else "in stock"} but Schema availability is {av.group(1)}')
        if sku and re.search(r'"sku":\s*"([^"]*)"', sch) and re.search(r'"sku":\s*"([^"]*)"', sch).group(1).upper() != stem:
            add('R10', 'ERROR', 'Schema sku != filename')
    elif '## Schema' in text:
        add('R10', 'WARN', 'Schema block present but no JSON found')
    # R11 sections (informational for lite pages)
    missing = [s for s in ('Selling Points', 'Ideal For', 'Comparison', 'FAQ', 'Related Products', 'Schema') if f'## {s}' not in text]
    if missing:
        add('R11', 'WARN', 'template sections missing: ' + ', '.join(missing))
    # R12 upscaling tech vs vendor (video cards / PCs)
    low = text.lower()
    if re.search(r'\barc\b|intel arc', low) and 'dlss' in low and 'nvidia' not in low and 'geforce' not in low and 'rtx' not in low:
        add('R12', 'ERROR', 'DLSS mentioned on an Intel Arc product (Arc uses XeSS)')
    # R13 warranty
    for i, ln in enumerate(text.split('\n'), 1):
        if WARRANTY_ON and WARRANTY.search(ln) and not NEUTRAL_W.search(ln) and not ln.startswith('vs ') and 'vs ' not in ln[:40]:
            add('R13', 'WARN', 'warranty term stated - confirm it is in BC: ' + ln.strip()[:90], i)
    # line rules on body
    body = body_without_header_and_schema(text)
    for i, ln in enumerate(text.split('\n'), 1):
        if ln not in body.split('\n'):
            continue
        in_schema = False
        for rid, lvl, msg, rx in LINE_RULES:
            m = rx.search(ln)
            if m:
                add(rid, lvl, f'{msg}: "{ln.strip()[:100]}"', i)
    # R14 repeated sentences within file
    sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', body) if len(s.strip()) > 60]
    c = collections.Counter(sents)
    for s, n in c.items():
        if n > 1:
            add('R14', 'WARN', f'sentence repeated {n}x: "{s[:70]}"')
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='*')
    ap.add_argument('--category')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--summary', action='store_true')
    ap.add_argument('--rule')
    ap.add_argument('--warranty', action='store_true', help='also run R13 (warranty terms to verify against BC; noisy)')
    a = ap.parse_args()
    if a.files:
        files = [pathlib.Path(f).resolve() for f in a.files]
    elif a.all or a.category:
        files = geo_files(a.category)
    else:
        ap.error('give files, --category or --all')
    global STEMS, EOL, PREFIXES, WARRANTY_ON
    WARRANTY_ON = a.warranty or a.rule == 'R13'
    STEMS, EOL = all_stems(), eol_stems()
    PREFIXES = {x[:3] for x in STEMS if re.search(r'\d', x)}
    per_rule = collections.Counter()
    files_hit = collections.defaultdict(set)
    errs = 0
    samples = collections.defaultdict(list)
    for f in files:
        iss = [i for i in lint(f) if not a.rule or i[0] == a.rule]
        for rid, lvl, line, msg in iss:
            per_rule[(rid, lvl)] += 1
            files_hit[rid].add(f.stem)
            if len(samples[rid]) < 3:
                samples[rid].append(f'{f.stem}: {msg}'[:160])
            if lvl == 'ERROR':
                errs += 1
        if iss and not a.summary:
            print(f'{f.parent.name}/{f.name}')
            for rid, lvl, line, msg in iss:
                print(f'  {lvl:5} {rid:3} {("L%d " % line) if line else ""}{msg}'.encode('ascii', 'replace').decode())
        elif not iss and not a.summary and len(files) == 1:
            print(f'{f.name}: OK')
    print(f'\n{len(files)} files linted')
    for (rid, lvl), n in sorted(per_rule.items(), key=lambda x: (x[0][0].lstrip("R").zfill(3))):
        print(f'  {rid:3} {lvl:5} {n:5} hits in {len(files_hit[rid]):4} files')
        if a.summary:
            for s in samples[rid]:
                print('        e.g.', s.encode('ascii', 'replace').decode())
    sys.exit(1 if errs else 0)


if __name__ == '__main__':
    main()
