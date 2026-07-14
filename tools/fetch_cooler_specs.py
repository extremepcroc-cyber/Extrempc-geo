#!/usr/bin/env python3
"""Fetch compatibility specs for CPU coolers and AIOs from ExtremePC product pages."""
import json, os, re, urllib.request, time

BASE_DIR = os.path.expanduser('~/Documents/GitHub/Extrempc-geo')
COOLING_DIR = os.path.join(BASE_DIR, 'cooling')
CACHE_DIR = os.path.expanduser('~/AppData/Local/hermes/profiles/exie-web/workspace/EVAcache/2026-07-15')

os.makedirs(COOLING_DIR, exist_ok=True)

# Load products from EVAcache
with open(os.path.join(CACHE_DIR, 'products.json')) as f:
    data = json.load(f)
products = data['products']

# Filter for actual CPU coolers and AIOs
coolers = []
for p in products:
    name = p.get('name', '')
    name_lower = name.lower()
    
    # Must contain cooler-related terms
    has_cooler = any(kw in name_lower for kw in ['cpu cooler', 'air cooler', 'aio', 'liquid cooling', 'water cooling'])
    
    # Must NOT be a non-cooler item
    is_not_cooler = any(kw in name_lower for kw in ['case', 'tower', 'psu', 'power supply', 'frame', 'mining', 'rig', 'motherboard', 'monitor', 'oled', 'network', 'wifi', 'router', 'switch', 'xpc', 'gaming pc', 'pre-built'])
    
    if has_cooler and not is_not_cooler:
        coolers.append(p)

print(f"Actual CPU Coolers/AIOs: {len(coolers)}")

# Get existing GEO files
existing_skus = set(os.path.splitext(f)[0] for f in os.listdir(COOLING_DIR) if f.endswith('.md'))
remaining = [c for c in coolers if c['sku'] not in existing_skus]
print(f"Coolers needing GEO files: {len(remaining)}")

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

def extract_cooler_specs(text):
    """Extract CPU cooler compatibility specs."""
    specs = {}
    
    # Type (Air or AIO/Liquid)
    if any(kw in text.lower() for kw in ['aio', 'liquid', 'water cooling', 'all-in-one']):
        specs['type'] = 'AIO Liquid Cooler'
    elif 'air' in text.lower() or 'tower' in text.lower():
        specs['type'] = 'Air Cooler'
    
    # Socket Support
    socket_patterns = [
        (r'(?:socket|support|compatible)[^\n]*?(AM4|AM5|LGA1700|LGA1851|LGA1200|Intel|AMD)', 1),
        (r'(AM4|AM5|LGA1700|LGA1851|LGA1200)', 1),
    ]
    for pat, gidx in socket_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            specs['socket'] = m.group(gidx).strip()
            break
    
    # Height (for air coolers)
    height_patterns = [
        (r'(?:height|heigth)[^\d]*?(\d+)\s*mm', 1),
    ]
    for pat, gidx in height_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            specs['height'] = f"{m.group(gidx)}mm"
            break
    
    # Radiator Size (for AIOs)
    rad_patterns = [
        (r'(\d{3})\s*mm\s*(?:radiator|aio)', 1),
        (r'(?:240|280|360)\s*mm', 0),
    ]
    for pat, gidx in rad_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            specs['radiator'] = m.group(gidx).strip()
            break
    
    # TDP Rating
    tdp_patterns = [
        (r'(?:tdp|heat\s+design\s+power)[^\d]*?(\d+)\s*W', 1),
    ]
    for pat, gidx in tdp_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            specs['tdp'] = f"{m.group(gidx)}W"
            break
    
    # Fan Size
    fan_patterns = [
        (r'(\d{2,3})\s*mm\s*fan', 1),
    ]
    for pat, gidx in fan_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            specs['fan_size'] = f"{m.group(gidx)}mm"
            break
    
    return specs

def create_cooler_geo_file(cooler, specs):
    """Create a GEO file for a CPU cooler."""
    sku = cooler['sku']
    name = cooler['name']
    price = cooler['price_nzd_inc_gst']
    url = cooler['url']
    stock = cooler['oh_stock']
    
    # Stock status
    if stock > 5:
        stock_status = "Plenty in stock"
    elif stock > 0:
        stock_status = "Only a few left"
    else:
        stock_status = "Out of stock"
    
    # Build Quick Specs
    quick_specs = []
    if 'type' in specs:
        quick_specs.append(f"Type: {specs['type']}")
    if 'socket' in specs:
        quick_specs.append(f"Socket Support: {specs['socket']}")
    if 'height' in specs:
        quick_specs.append(f"Height: {specs['height']}")
    if 'radiator' in specs:
        quick_specs.append(f"Radiator Size: {specs['radiator']}")
    if 'tdp' in specs:
        quick_specs.append(f"TDP Rating: {specs['tdp']}")
    if 'fan_size' in specs:
        quick_specs.append(f"Fan Size: {specs['fan_size']}")
    
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
This CPU cooler is available at ExtremePC in Auckland, NZ. For detailed compatibility questions, visit the product page or contact the store.

## Why Buy From ExtremePC
- Local NZ stock with fast availability
- In-store pickup at Onehunga or Wellington
- Expert build service available ($80 build fee)
- 2-year NZ warranty support
"""
    
    filepath = os.path.join(COOLING_DIR, f"{sku}.md")
    with open(filepath, 'w') as f:
        f.write(content)
    return filepath

def fetch_specs_from_url(url):
    """Fetch page and extract specs."""
    html = fetch_page(url)
    if not html:
        return {}
    
    text = clean_text(html)
    specs = extract_cooler_specs(text)
    
    # Also check tables
    table_pattern = re.compile(r'<table[^>]*>(.*?)</table>', re.DOTALL | re.IGNORECASE)
    for table in table_pattern.findall(html):
        cells = re.findall(r'<(?:td|th)[^>]*>(.*?)</(?:td|th)>', table, re.DOTALL | re.IGNORECASE)
        cell_text = ' '.join(clean_text(c) for c in cells)
        specs.update(extract_cooler_specs(cell_text))
    
    return specs

# Process coolers
max_coolers = len(remaining)  # Process all remaining coolers
processed = 0

for i, cooler in enumerate(remaining[:max_coolers]):
    sku = cooler['sku']
    existing = os.path.join(COOLING_DIR, f"{sku}.md")
    
    if os.path.exists(existing):
        print(f"[{i+1}/{max_coolers}] SKIP {sku} - already exists")
        processed += 1
        continue
    
    print(f"[{i+1}/{max_coolers}] Processing {sku}...")
    specs = fetch_specs_from_url(cooler['url'])
    
    if specs:
        print(f"  Found specs: {list(specs.keys())}")
    else:
        print(f"  No specs extracted from page")
    
    filepath = create_cooler_geo_file(cooler, specs)
    print(f"  Created: {filepath}")
    processed += 1
    
    time.sleep(1)

print(f"\nCompleted: {processed}/{max_coolers} coolers processed")
print(f"GEO files created in: {COOLING_DIR}")
