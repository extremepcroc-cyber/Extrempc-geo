#!/usr/bin/env python3
"""Fetch compatibility specs for computer cases from ExtremePC product pages."""
import json, os, re, urllib.request, time, sys
from html.parser import HTMLParser

BASE_DIR = os.path.expanduser('~/Documents/GitHub/Extrempc-geo')
CASES_DIR = os.path.join(BASE_DIR, 'computer-cases')
CACHE_DIR = os.path.expanduser('~/AppData/Local/hermes/profiles/exie-web/workspace/EVAcache/2026-07-15')

os.makedirs(CASES_DIR, exist_ok=True)

# Load cases from EVAcache
with open(os.path.join(CACHE_DIR, 'products.json')) as f:
    data = json.load(f)
products = data['products']
cases = [p for p in products if 'case' in p['name'].lower() and any(kw in p['name'].lower() for kw in ['tower', 'mid', 'full', 'mini', 'micro', 'itx'])]

# Filter out non-cases
cases = [c for c in cases if not ('switch' in c['name'].lower() or 'network' in c['name'].lower())]

# Sort by stock (highest first)
cases.sort(key=lambda x: x['oh_stock'], reverse=True)

print(f"Total cases to process: {len(cases)}")

def fetch_page(url):
    """Fetch a product page and return text content."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f"  ERROR fetching {url}: {e}")
        return None

def extract_specs_from_text(text):
    """Extract compatibility specs from product page text."""
    specs = {}
    
    # GPU Length
    m = re.search(r'(?:gpu|graphics\s+card)\s+(?:length|limit|clearance|support)[^\n]*?\s*(\d+)\s*mm', text, re.IGNORECASE)
    if m:
        specs['gpu_length'] = f"{m.group(1)}mm"
    
    # CPU Cooler Height
    m = re.search(r'(?:cpu\s+cooler|cooler)\s+(?:height|limit|support|clearance)[^\n]*?\s*(\d+)\s*mm', text, re.IGNORECASE)
    if m:
        specs['cooler_height'] = f"{m.group(1)}mm"
    
    # PSU Length
    m = re.search(r'(?:psu|power\s+supply)\s+(?:length|limit)[^\n]*?\s*(\d+)\s*mm', text, re.IGNORECASE)
    if m:
        specs['psu_length'] = f"{m.group(1)}mm"
    
    # Motherboard Support
    mb_patterns = [
        r'(?:motherboard\s+support|supporting\s+motherboards)[^\n]*?(.*?)$',
        r'(?:atx|e-atx|m-atx|mini-itx|micro-atx)[^\n]*?(?:/|,|and)\s*(.*?)(?:\n|$)',
    ]
    for pat in mb_patterns:
        m = re.search(pat, text, re.IGNORECASE | re.MULTILINE)
        if m:
            specs['motherboard'] = m.group(0).strip()[:100]
            break
    
    # Radiator Support
    rad_patterns = [
        r'(?:radiator\s+support|cooling\s+capacity)[^\n]*?(.*?)$',
        r'(?:240|280|360)\s*mm\s*radiator[^\n]*?(.*?)$',
    ]
    for pat in rad_patterns:
        m = re.search(pat, text, re.IGNORECASE | re.MULTILINE)
        if m:
            specs['radiator'] = m.group(0).strip()[:150]
            break
    
    # Dimensions
    m = re.search(r'(?:dimensions|size)[^\n]*?(\d+\s*[×x]\s*\d+\s*[×x]\s*\d+)\s*mm', text, re.IGNORECASE)
    if m:
        specs['dimensions'] = m.group(1)
    
    # Fan Support
    m = re.search(r'(?:fan\s+support|pre-?installed\s+fan)[^\n]*?(.*?)$', text, re.IGNORECASE | re.MULTILINE)
    if m:
        specs['fans'] = m.group(0).strip()[:150]
    
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
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text)
    
    # Try to find specs section
    specs = extract_specs_from_text(text)
    
    # Also try to find spec tables in the HTML
    table_pattern = re.compile(r'<table[^>]*>(.*?)</table>', re.DOTALL | re.IGNORECASE)
    for table in table_pattern.findall(html):
        # Extract key-value pairs from table cells
        cells = re.findall(r'<(?:td|th)[^>]*>(.*?)</(?:td|th)>', table, re.DOTALL | re.IGNORECASE)
        cell_text = ' '.join(re.sub(r'<[^>]+>', '', c).strip() for c in cells)
        specs.update(extract_specs_from_text(cell_text))
    
    return specs

# Process top cases
max_cases = min(20, len(cases))  # Process up to 20 cases
processed = 0

for i, case in enumerate(cases[:max_cases]):
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
