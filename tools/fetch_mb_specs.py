#!/usr/bin/env python3
"""Fetch compatibility specs for motherboards from ExtremePC product pages."""
import json, os, re, urllib.request, time

BASE_DIR = os.path.expanduser('~/Documents/GitHub/Extrempc-geo')
MB_DIR = os.path.join(BASE_DIR, 'motherboards')
CACHE_DIR = os.path.expanduser('~/AppData/Local/hermes/profiles/exie-web/workspace/EVAcache/2026-07-15')

os.makedirs(MB_DIR, exist_ok=True)

# Load motherboards from EVAcache
with open(os.path.join(CACHE_DIR, 'products.json')) as f:
    data = json.load(f)
products = data['products']
mbs = [p for p in products if 'motherboard' in p.get('name', '').lower() or any(kw in p.get('name', '').lower() for kw in ['mb-', 'b550', 'b650', 'z790', 'z690', 'x670', 'x570', 'h610', 'b760', 'z790', 'b560'])]

# Get existing GEO files
existing_skus = set(os.path.splitext(f)[0] for f in os.listdir(MB_DIR) if f.endswith('.md'))
remaining = [m for m in mbs if m['sku'] not in existing_skus]
print(f"Motherboards needing GEO files: {len(remaining)}")

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
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_mb_specs(text):
    """Extract motherboard compatibility specs."""
    specs = {}
    
    # Socket
    socket_patterns = [
        (r'(?:socket|cpu\s+socket)[^\n]*?(AM4|AM5|LGA1700|LGA1851|LGA1200|LGA1700|LGA1851|Intel|AMD)', 1),
    ]
    for pat, gidx in socket_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            specs['socket'] = m.group(gidx).strip()
            break
    
    # Chipset
    chipset_patterns = [
        (r'(?:chipset|series)[^\n]*?(B550|B650|B850|Z790|Z690|X670|X570|H610|B760|Z790|B560|H810|A520|A620|B450)', 1),
    ]
    for pat, gidx in chipset_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            specs['chipset'] = m.group(gidx).strip()
            break
    
    # Memory Type
    mem_patterns = [
        (r'(?:memory|ram|mem)[^\n]*?(DDR4|DDR5|DDR4/DDR5)', 1),
    ]
    for pat, gidx in mem_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            specs['memory_type'] = m.group(gidx).strip()
            break
    
    # Max Memory
    max_mem_patterns = [
        (r'max(?:imum)?.*?(?:memory|ram)[^\d]*?(\d+)\s*GB', 1),
    ]
    for pat, gidx in max_mem_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            specs['max_memory'] = f"{m.group(gidx)}GB"
            break
    
    # Memory Slots
    slot_patterns = [
        (r'(\d+)\s*\S*\s*DIMM', 1),
        (r'(\d+)\s*\S*\s*slots?', 1),
    ]
    for pat, gidx in slot_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            specs['memory_slots'] = f"{m.group(gidx)} slots"
            break
    
    # M.2 Slots
    m2_patterns = [
        (r'(\d+)\s*M\.?2', 1),
    ]
    for pat, gidx in m2_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            specs['m2_slots'] = f"{m.group(gidx)} M.2 slots"
            break
    
    # Form Factor
    form_patterns = [
        (r'(ATX|Micro-ATX|mATX|Mini-ITX|E-ATX|Extended ATX)', 1),
    ]
    for pat, gidx in form_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            specs['form_factor'] = m.group(gidx).strip()
            break
    
    return specs

def create_mb_geo_file(mb, specs):
    """Create a GEO file for a motherboard."""
    sku = mb['sku']
    name = mb['name']
    price = mb['price_nzd_inc_gst']
    url = mb['url']
    stock = mb['oh_stock']
    
    # Stock status
    if stock > 5:
        stock_status = "Plenty in stock"
    elif stock > 0:
        stock_status = "Only a few left"
    else:
        stock_status = "Out of stock"
    
    # Build Quick Specs
    quick_specs = []
    if 'socket' in specs:
        quick_specs.append(f"CPU Socket: {specs['socket']}")
    if 'chipset' in specs:
        quick_specs.append(f"Chipset: {specs['chipset']}")
    if 'memory_type' in specs:
        quick_specs.append(f"Memory Type: {specs['memory_type']}")
    if 'max_memory' in specs:
        quick_specs.append(f"Max Memory: {specs['max_memory']}")
    if 'memory_slots' in specs:
        quick_specs.append(f"Memory Slots: {specs['memory_slots']}")
    if 'm2_slots' in specs:
        quick_specs.append(f"M.2 Slots: {specs['m2_slots']}")
    if 'form_factor' in specs:
        quick_specs.append(f"Form Factor: {specs['form_factor']}")
    
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
This motherboard is available at ExtremePC in Auckland, NZ. For detailed compatibility questions, visit the product page or contact the store.

## Why Buy From ExtremePC
- Local NZ stock with fast availability
- In-store pickup at Onehunga or Wellington
- Expert build service available ($80 build fee)
- 2-year NZ warranty support
"""
    
    filepath = os.path.join(MB_DIR, f"{sku}.md")
    with open(filepath, 'w') as f:
        f.write(content)
    return filepath

def fetch_specs_from_url(url):
    """Fetch page and extract specs."""
    html = fetch_page(url)
    if not html:
        return {}
    
    text = clean_text(html)
    specs = extract_mb_specs(text)
    
    # Also check tables
    table_pattern = re.compile(r'<table[^>]*>(.*?)</table>', re.DOTALL | re.IGNORECASE)
    for table in table_pattern.findall(html):
        cells = re.findall(r'<(?:td|th)[^>]*>(.*?)</(?:td|th)>', table, re.DOTALL | re.IGNORECASE)
        cell_text = ' '.join(clean_text(c) for c in cells)
        specs.update(extract_mb_specs(cell_text))
    
    return specs

# Process motherboards
max_mbs = min(36, len(remaining))
processed = 0

for i, mb in enumerate(remaining[:max_mbs]):
    sku = mb['sku']
    existing = os.path.join(MB_DIR, f"{sku}.md")
    
    if os.path.exists(existing):
        print(f"[{i+1}/{max_mbs}] SKIP {sku} - already exists")
        processed += 1
        continue
    
    print(f"[{i+1}/{max_mbs}] Processing {sku}...")
    specs = fetch_specs_from_url(mb['url'])
    
    if specs:
        print(f"  Found specs: {list(specs.keys())}")
    else:
        print(f"  No specs extracted from page")
    
    filepath = create_mb_geo_file(mb, specs)
    print(f"  Created: {filepath}")
    processed += 1
    
    time.sleep(1)

print(f"\nCompleted: {processed}/{max_mbs} motherboards processed")
print(f"GEO files created in: {MB_DIR}")
