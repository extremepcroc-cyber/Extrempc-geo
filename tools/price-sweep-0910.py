import json, os, re
cache={}
for x in json.load(open(os.path.expanduser('~/AppData/Local/hermes/profiles/exie-web/workspace/EVAcache/2026-09-10/products.json')))['products']:
    cache[x['sku']]=x
KBROOT=os.path.expanduser('~/Documents/GitHub/Extrempc-geo/product-knowledge')
DIRS=['computer-cases','cooling','motherboards','power-supplies','gpus','ram','ssds','keyboards','mice','headsets','monitors']
SKU=re.compile(r'\*\*SKU:\*\*[^\n]*?([A-Za-z0-9][A-Za-z0-9\-_\.]*)')
PRICE=re.compile(r'\*\*Price:\*\*\s*NZD\s*\$([\d,]+(?:\.\d+)?)', re.I)
OOS=re.compile(r'OUT\s+OF\s+STOCK|REMOVED|REPLACED|DELISTED', re.I)
stale=[]
checked=0
for d in DIRS:
    p=os.path.join(KBROOT,d)
    if not os.path.isdir(p): continue
    for fn in sorted(os.listdir(p)):
        if not fn.endswith('.md'): continue
        t=open(os.path.join(p,fn),encoding='utf-8').read()
        m=SKU.search(t); 
        if not m: continue
        sku=m.group(1)
        if sku not in cache: continue  # OOS/delisted — not in OH cache, skip
        if OOS.search(t.split('##')[0]): continue  # flagged OOS, skip
        pr=PRICE.search(t)
        if not pr: continue
        checked+=1
        old=float(pr.group(1).replace(',',''))
        new=round(cache[sku]['price_nzd_inc_gst'],2)
        if abs(old-new)>0.05:
            stale.append((f"{d}/{fn}",sku,old,new))
print(f"in-stock KB files with a Price line checked: {checked}")
print(f"STALE prices (KB != BC calc×1.15): {len(stale)}")
for f,s,o,n in sorted(stale):
    print(f"   {f:52} {s:18} KB ${o:>10} -> BC ${n:>10}")
