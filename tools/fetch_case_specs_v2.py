#!/usr/bin/env python3
"""Fetch compatibility specs for remaining computer cases from ExtremePC product pages - improved version."""
import json, os, re, urllib.request, time

BASE_DIR = os.path.expanduser('~/Documents/GitHub/Extrempc-geo')
CASES_DIR = os.path.join(BASE_DIR, 'computer-cases')
CACHE_DIR = os.path.expanduser('~/AppData/Local/hermes/profiles/exie-web/workspace/EVAcache/2026-07-15')

# Load cases from EVAcache
with open(os.path.join(CACHE_DIR, 'products.json')) as f:
    data = json.load(f)
products = data['products']
cases = [p for p in products if 'case' in p['name'].lower() and any(kw in p['name'].lower() for kw in ['tower', 'mid', 'full', 'mini', 'micro', 'itx'])]

# Filter out non-cases
cases = [c for c in cases if not ('switch' in c['name'].lower() or 'network' in c['name'].lower())]

# Get existing GEO files
existing_skus = set(os.path.splitext(f)[0] for f in os.listdir(CASES_DIR) if f.endswith('.md'))

# Filter to only cases that need GEO files
remaining = [c for c in cases if c['sku'] not in existing_skus]
print(f"Cases needing GEO files: {len(remaining)}")

def fetch_page(url):
    """Fetch a product page and return text content."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f"  ERROR fetching {url}: {e}")
        return None

def clean_text(text):
    """Remove HTML tags and JavaScript artifacts."""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'document\.[^\s;]+', '', text)
    text = re.sub(r'className\s*=\s*[^\s;]+', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_specs_from_text(text):
    """Extract compatibility specs from product page text."""
    specs = {}
    
    # GPU Length - improved patterns
    gpu_patterns = [
        r'(?:gpu|graphics\s+card|vga|video\s+card)\s+(?:length|limit|clearance|support|maximum)[^\n]*?\s*(\d+)\s*mm',
        r'max(?:imum)?.*?(?:gpu|graphics|vga)[^\d]*?(\d+)\s*mm',
        r'(?:gpu|vga).{0,30}?up\s*to\s*(\d+)\s*mm',
    ]
    for pat in gpu_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            specs['gpu_length'] = f"{m.group(1)}mm"
            break
    
    # CPU Cooler Height - improved patterns
    cooler_patterns = [
        r'(?:cpu\s+cooler|cooler)\s+(?:height|limit|support|clearance|maximum)[^\d]*?(\d+)\s*mm',
        r'(?:cooler|height).{0,30}?up\s*to\s*(\d+)\s*mm',
        r'max(?:imum)?.*?cooler\s*height[^\d]*?(\d+)\s*mm',
    ]
    for pat in cooler_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            specs['cooler_height'] = f"{m.group(1)}mm"
            break
    
    # PSU Length
    psu_patterns = [
        r'(?:psu|power\s+supply)\s+(?:length|limit)[^\d]*?(\d+)\s*mm',
        r'max(?:imum)?.*?(?:psu|power).{0,30}?(\d+)\s*mm',
    ]
    for pat in psu_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            specs['psu_length'] = f"{m.group(1)}mm"
            break
    
    # Motherboard Support - cleaner extraction
    mb_patterns = [
        r'motherboard\s+support[^\n]*?(ATX|E-ATX|M-ATX|Mini-ITX|Micro-ATX)[^\n]*?(?:ATX|E-ATX|M-ATX|Mini-ITX|Micro-ATX)[^\n]*?(?:ATX|E-ATX|M-ATX|Mini-ITX|Micro-ATX)?',
        r'(ATX|E-ATX|M-ATX|Mini-ITX|Micro-ATX)\s*/\s*(ATX|E-ATX|M-ATX|Mini-ITX|Micro-ATX)',
    ]
    for pat in mb_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            specs['motherboard'] = m.group(0).strip()[:80]
            break
    
    # Radiator Support
    rad_patterns = [
        r'(?:radiator\s+support|cooling\s+capacity)[^\n]*?(\d+\s*mm[^\n]*)',
        r'(?:240|280|360)\s*mm\s*radiator[^\n]*?(\d+\s*mm[^\n]*)',
    ]
    for pat in rad_patterns:
        m = re.search(pat, text, re.IGNORECASE | re.MULTILINE)
        if m:
            specs['radiator'] = m.group(1).strip()[:120]
            break
    
    # Dimensions
    dim_patterns = [
        r'(?:dimensions|size|product\s+dimensions)[^\d]*?(\d+\s*[×x]\s*\d+\s*[×x]\s*\d+)\s*mm',
        r'(\d+\s*\d+\s*\d+)\s*mm',
    ]
    for pat in dim_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            specs['dimensions'] = m.group(1)
            break
    
    # Fan Support
    fan_patterns = [
        (r'(?:fan\s+support|pre-?installed\s+fan)[^\n]*?(\d+\s*[×x]\s*\d+\s*mm[^\n]*)', 1),
        (r'(?:top|front|rear|bottom).{0,20}?([\d]+\s*[×x]\s*[\d]+\s*mm)', 1),
    ]
    for pat, group_idx in fan_patterns:
        m = re.search(pat, text, re.IGNORECASE | re.MULTILINE)
        if m:
            specs['fans'] = m.group(group_idx).strip()[:120]
            break
    
    return specs

def create_geo_file(case, specs):
    """Create a GEO file for a case."""
    sku = case['sku']
    name = case['name']
    price = case['price_nzd_inc_gst']
    url = case['url']
    stock = case['oh_stock']
    
    # Stock status
    if stock > 5:
        stock_status = "Plenty in stock"
    elif stock > 0:
        stock_status = "Only a few left"
    else:
        stock_status = "Out of stock"
    
    # Build Quick Specs
    quick_specs = []
    if 'gpu_length' in specs:
        quick_specs.append(f"Max GPU Length: {specs['gpu_length']}")
    if 'cooler_height' in specs:
        quick_specs.append(f"Max CPU Cooler Height: {specs['cooler_height']}")
    if 'psu_length' in specs:
        quick_specs.append(f"Max PSU Length: {specs['psu_length']}")
    if 'motherboard' in specs:
        quick_specs.append(f"Motherboard Support: {specs['motherboard']}")
    if 'radiator' in specs:
        quick_specs.append(f"Radiator Support: {specs['radiator']}")
    if 'dimensions' in specs:
        quick_specs.append(f"Dimensions: {specs['dimensions']}")
    if 'fans' in specs:
        quick_specs.append(f"Fan Support: {specs['fans']}")
    
    # Default specs if not found
    if not quick_specs:
        quick_specs = ["Compatibility specs pending - check product page for details"]
    
    content = f"""# {name}

**Price:** NZD ${price} (incl. GST)
**SKU:** {sku}
**URL:** {url}
**Stock:** {stock_status}

## Quick Specs
{chr(10).join('- ' + s for s in quick_specs)}

## Compatibility Notes
This case is available at ExtremePC in Auckland, NZ. For detailed compatibility questions, visit the product page or contact the store.

## Why Buy From ExtremePC
- Local NZ stock with fast availability
- In-store pickup at Onehunga or Wellington
- Expert build service available ($80 build fee)
- 2-year NZ warranty support
"""
    
    filepath = os.path.join(CASES_DIR, f"{sku}.md")
    with open(filepath, 'w') as f:
        f.write(content)
    return filepath

def fetch_specs_from_url(url):
    """Fetch page and extract specs using multiple methods."""
    html = fetch_page(url)
    if not html:
        return {}
    
    # Extract text content (remove HTML tags)
    text = clean_text(html)
    
    # Try to find specs section
    specs = extract_specs_from_text(text)
    
    # Also try to find spec tables in the HTML
    table_pattern = re.compile(r'<table[^>]*>(.*?)</table>', re.DOTALL | re.IGNORECASE)
    for table in table_pattern.findall(html):
        # Extract key-value pairs from table cells
        cells = re.findall(r'<(?:td|th)[^>]*>(.*?)</(?:td|th)>', table, re.DOTALL | re.IGNORECASE)
        cell_text = ' '.join(clean_text(c) for c in cells)
        specs.update(extract_specs_from_text(cell_text))
    
    return specs

# Process remaining cases
max_cases = min(24, len(remaining))  # Process up to 24 remaining cases
processed = 0

for i, case in enumerate(remaining[:max_cases]):
    sku = case['sku']
    existing = os.path.join(CASES_DIR, f"{sku}.md")
    
    if os.path.exists(existing):
        print(f"[{i+1}/{max_cases}] SKIP {sku} - already exists")
        processed += 1
        continue
    
    print(f"[{i+1}/{max_cases}] Processing {sku}...")
    specs = fetch_specs_from_url(case['url'])
    
    if specs:
        print(f"  Found specs: {list(specs.keys())}")
    else:
        print(f"  No specs extracted from page")
    
    filepath = create_geo_file(case, specs)
    print(f"  Created: {filepath}")
    processed += 1
    
    # Rate limiting
    time.sleep(1)

print(f"\nCompleted: {processed}/{max_cases} cases processed")
print(f"GEO files created in: {CASES_DIR}")
