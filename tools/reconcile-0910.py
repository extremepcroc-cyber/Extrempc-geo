import json, os, re, sys

KBROOT = os.path.expanduser('~/Documents/GitHub/Extrempc-geo/product-knowledge')
CACHE = os.path.expanduser('~/AppData/Local/hermes/profiles/exie-web/workspace/EVAcache/2026-09-10')
APPLY = len(sys.argv) > 1 and sys.argv[1] == '--apply'

cache = {x['sku']:x for x in json.load(open(CACHE+'/products.json'))['products']}

DIRS=['computer-cases','cooling','motherboards','power-supplies','gpus','ram','ssd','ssds',
      'keyboards','gaming-keyboards','mice','headsets','monitors','cpus','hdd','chairs']
SKU_RE=re.compile(r'\*\*SKU:\*\*\s*([A-Za-z0-9]+)')
PRICE_RE=re.compile(r'^\*\*Price:\*\*.*$', re.M)
STOCKLINE_RE=re.compile(r'^\*\*(?:Stock|Status):\*\*(.*)$', re.M)
OOS_RE=re.compile(r'OUT\s+OF\s+STOCK|Out\s+of\s+stock|REMOVED FROM CATALOG|BOTH VARIANTS OUT|out of stock', re.I)
def stockline(text):
    m=STOCKLINE_RE.search(text)
    return m.group(1) if m else None

def price_line(c):
    p=c['price_nzd_inc_gst']; l=c['list_price_nzd_inc_gst']
    if c.get('on_sale') and abs(l-p)>0.005:
        return f"NZD ${p:,.2f} (incl. GST) (on sale from ${l:,.2f})"
    return f"NZD ${p:,.2f} (incl. GST)"
def cur_price(text):
    m=re.search(r'NZD\s*\$([0-9,]+(?:\.[0-9]{1,2})?)', text)
    return float(m.group(1).replace(',','')) if m else None

price_updates=[]   # (file, sku, old, new, newline, name)
in_cache_set=set()
for dirn in DIRS:
    p=os.path.join(KBROOT,dirn)
    if not os.path.isdir(p): continue
    for fn in sorted(os.listdir(p)):
        if not fn.endswith('.md'): continue
        full=os.path.join(p,fn)
        text=open(full,encoding='utf-8').read()
        m=SKU_RE.search(text)
        if not m: continue
        sku=m.group(1)
        if sku in cache:
            c=cache[sku]; target=c['price_nzd_inc_gst']
            cur=cur_price(text)
            if PRICE_RE.search(text) and (cur is None or abs(cur-target)>0.05):
                price_updates.append((dirn+'/'+fn,sku,cur,target,price_line(c),c['name'][:45]))
                if APPLY:
                    open(full,'w',encoding='utf-8').write(PRICE_RE.sub("**Price:** "+price_line(c),text,count=1))

print("MODE:", "APPLY" if APPLY else "DRY-RUN")
print("In-cache KB PRICE updates needed:", len(price_updates), "\n")
for f,s,old,new,nl,nm in sorted(price_updates):
    o = "—" if old is None else f"${old:,.2f}"
    print(f"  {f:48} {s:18} {o:>9} -> ${new:>9.2f}   {nm}")

# SKUs in removed/added lists to verify via BC (from delta run) — flagged for OOS check
VERIFY = {
 'COOTMRPV36AB':'Thermalright Peerless Vision 360 ARGB Black AIO (cooling)',
 'MONAOC27E40L':'AOC 27E40L 27 FHD 144Hz (monitors)',
 'MOSMCHK7UWG':'MCHOSE K7 Ultra White Gold (mice)',
}
print("\nRemoved-today SKUs with KB files -> verify OOS via BC:")
for k,v in VERIFY.items(): print("   ", k, v)

# Also list KB files whose primary SKU is NOT in cache (potential OOS) but have no OOS marker
print("\nKB files whose primary SKU is absent from 09-10 cache (OOS candidates to check):")
cnt=0
for dirn in DIRS:
    p=os.path.join(KBROOT,dirn)
    if not os.path.isdir(p): continue
    for fn in sorted(os.listdir(p)):
        if not fn.endswith('.md'): continue
        full=os.path.join(p,fn)
        text=open(full,encoding='utf-8').read()
        m=SKU_RE.search(text)
        if not m: continue
        if m.group(1) not in cache and not OOS_RE.search(stockline(text) or ''):
            print(f"   {dirn+'/'+fn:50} {m.group(1)}")
            cnt+=1
print("   count:",cnt)
if APPLY:
    print(f"\nApplied {len(price_updates)} price rewrites.")
