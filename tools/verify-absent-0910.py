import json, os, re, urllib.request, urllib.parse
for envp in [os.path.expanduser('~/Documents/GitHub/Extrempc-geo/.env'),
             os.path.expanduser('~/AppData/Local/hermes/profiles/exie/extremepc.env')]:
    if os.path.exists(envp):
        for line in open(envp):
            line=line.strip()
            if line.startswith('BC_ACCESS_TOKEN='): TOKEN=line.split('=',1)[1]
            if line.startswith('BC_API_BASE='): BASE=line.split('=',1)[1]
cache = {x['sku']:x for x in json.load(open(os.path.expanduser('~/AppData/Local/hermes/profiles/exie-web/workspace/EVAcache/2026-09-10/products.json')))['products']}
KBROOT=os.path.expanduser('~/Documents/GitHub/Extrempc-geo/product-knowledge')
DIRS=['computer-cases','cooling','motherboards','power-supplies','gpus','ram','ssd','ssds','keyboards','mice','headsets','monitors']
SKU_RE=re.compile(r'\*\*SKU:\*\*\s*([A-Za-z0-9]+)')
OOS_RE=re.compile(r'OUT\s+OF\s+STOCK|Out\s+of\s+stock|REMOVED', re.I)
def bc(sku):
    url=f"{BASE}/catalog/products?sku={urllib.parse.quote(sku)}&include_fields=id,name,inventory_level,is_visible&limit=1"
    try:
        req=urllib.request.Request(url,headers={'X-Auth-Token':TOKEN,'Accept':'application/json'})
        with urllib.request.urlopen(req,timeout=30) as r: d=json.load(r)
        if not d.get('data'): return ('GONE',None)
        p=d['data'][0]; return ('OK',p['inventory_level'])
    except Exception as e:
        return ('ERR',str(e)[:40])
cands=[]
for dirn in DIRS:
    p=os.path.join(KBROOT,dirn)
    if not os.path.isdir(p): continue
    for fn in sorted(os.listdir(p)):
        if not fn.endswith('.md'): continue
        full=os.path.join(p,fn)
        text=open(full,encoding='utf-8').read()
        m=SKU_RE.search(text)
        if not m: continue
        if m.group(1) not in cache and not OOS_RE.search(text.split('##')[0]):
            cands.append((dirn+'/'+fn,m.group(1)))
from collections import Counter
res=Counter()
gone=[]; oos=[]; ok=[]; err=[]
for f,s in cands:
    st,inv=bc(s)
    if st=='GONE': res['gone']+=1; gone.append((f,s))
    elif st=='OK':
        if inv==0: res['oos']+=1; oos.append((f,s))
        else: res['exists']+=1; ok.append((f,s,inv))
    else: res['err']+=1; err.append((f,s,st))
print("TOTAL absent-SKU KB files:",len(cands), dict(res))
print("\n=== STILL EXISTS (inv>0) — SKU likely variant/wrong, do NOT OOS-flag ===")
for f,s,inv in ok: print(f"   {f:50} {s:20} inv={inv}")
print("\n=== OOS (inv=0) — flag out of stock ===")
for f,s in oos: print(f"   {f:50} {s}")
print("\n=== SKU GONE from BC (renamed/removed) — needs manual SKU recheck ===")
for f,s in gone: print(f"   {f:50} {s}")
print("\n=== ERR ===")
for f,s,e in err: print(f"   {f:50} {s} {e}")
