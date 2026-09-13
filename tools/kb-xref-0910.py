import json, os, re, collections

KBROOT = os.path.expanduser('~/Documents/GitHub/Extrempc-geo/product-knowledge')
CACHE = os.path.expanduser('~/AppData/Local/hermes/profiles/exie-web/workspace/EVAcache/2026-09-09')

d = json.load(open(CACHE + '/products.json'))
cache_by_sku = {p['sku']: p for p in d['products']}
print("cache in-stock SKUs:", len(cache_by_sku))

dirs = ['computer-cases','cooling','motherboards','power-supplies','gpus','ram','ssd','ssds',
        'keyboards','gaming-keyboards','mice','headsets','monitors','cpus','hdd','chairs']
kb_files = {}
sku_re = re.compile(r'\b([A-Z0-9][A-Z0-9/-]{6,20})\b')
for dirn in dirs:
    p = os.path.join(KBROOT, dirn)
    if not os.path.isdir(p): continue
    for fn in os.listdir(p):
        if not fn.endswith('.md'): continue
        text = open(os.path.join(p, fn), encoding='utf-8').read()
        skus = set(sku_re.findall(text))
        kb_files[os.path.join(dirn, fn)] = {'skus': skus, 'text': text}

all_kb_skus = set()
for v in kb_files.values(): all_kb_skus |= v['skus']
print("KB files:", len(kb_files), "| distinct SKUs in KB:", len(all_kb_skus))

in_cache  = all_kb_skus & set(cache_by_sku)
not_in_cache = all_kb_skus - set(cache_by_sku)
print("KB SKUs still in cache:", len(in_cache))
print("KB SKUs NOT in cache (OOS candidates):", len(not_in_cache))
print(sorted(not_in_cache))

# Price mismatch check for SKUs in cache: extract price from KB file
# Look for a primary SKU per file (the one that matches filename if present, else first)
def file_price(text):
    m = re.search(r'\*\*Price:\*\*\s*NZD\s*\$([0-9,]+(?:\.[0-9]{1,2})?)', text)
    if not m: return None
    return float(m.group(1).replace(',', ''))

mismatches = []
for path, v in kb_files.items():
    for sku in v['skus']:
        if sku in cache_by_sku:
            cp = cache_by_sku[sku]['price_nzd_inc_gst']
            fp = file_price(v['text'])
            if fp is None: continue
            # Only compare if this sku appears to be the file's primary sku (in filename)
            if sku.lower() in path.lower():
                if abs(cp - fp) > 0.05:
                    mismatches.append((path, sku, fp, cp, cache_by_sku[sku]['name']))
print("\nPRICE MISMATCHES (file price vs cache, primary SKU):", len(mismatches))
for m in mismatches:
    print("  %-45s %-16s KB=$%8.2f  CACHE=$%8.2f  %s" % (m[0], m[1], m[2], m[3], m[4][:40]))

# Files that are OOS-flagged but SKU back in cache (stale OOS)
print("\nSTALE OOS FLAGS (file says OOS but SKU in cache):")
for path, v in kb_files.items():
    t = v['text']
    if re.search(r'OUT\s+OF\s+STOCK|Out\s+of\s+stock', t) and v['skus'] & set(cache_by_sku):
        present = sorted(v['skus'] & set(cache_by_sku))
        print("  %s -> in-cache SKUs: %s" % (path, present))
