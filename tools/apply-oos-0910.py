#!/usr/bin/env python3
"""Final OOS applier — re-derives absent-from-OH-cache KB files with FULL SKU,
splits into OOS(inv==0) / gone / hidden-in-stock(inv>0), applies correct flag,
preserves all other fields."""
import json, os, re, sys, urllib.request, urllib.parse
APPLY = '--apply' in sys.argv
for envp in [os.path.expanduser('~/Documents/GitHub/Extrempc-geo/.env'),
             os.path.expanduser('~/AppData/Local/hermes/profiles/exie/extremepc.env')]:
    if os.path.exists(envp):
        for line in open(envp):
            line=line.strip()
            if line.startswith('BC_ACCESS_TOKEN='): TOKEN=line.split('=',1)[1]
            if line.startswith('BC_API_BASE='): BASE=line.split('=',1)[1]
cache = {x['sku'] for x in json.load(open(os.path.expanduser('~/AppData/Local/hermes/profiles/exie-web/workspace/EVAcache/2026-09-10/products.json')))['products']}
KBROOT=os.path.expanduser('~/Documents/GitHub/Extrempc-geo/product-knowledge')
DIRS=['computer-cases','cooling','motherboards','power-supplies','gpus','ram','ssd','ssds','keyboards','mice','headsets','monitors']
# full SKU incl. hyphens/digits
FULL=re.compile(r'\*\*SKU:\*\*[^\n]*?([A-Za-z0-9][A-Za-z0-9\-_\.]*)')
MARK=re.compile(r'OUT\s+OF\s+STOCK|REMOVED|REPLACED|DELISTED|delisted', re.I)
def bc(sku):
    url=f"{BASE}/catalog/products?sku={urllib.parse.quote(sku)}&include_fields=inventory_level,is_visible&limit=1"
    try:
        req=urllib.request.Request(url,headers={'X-Auth-Token':TOKEN,'Accept':'application/json'})
        with urllib.request.urlopen(req,timeout=30) as r: d=json.load(r)
        if not d.get('data'): return 'gone'
        inv=d['data'][0]['inventory_level']
        return 'inv>0' if inv>0 else ('inv==0' if inv==0 else 'other')
    except Exception as e: return f'ERR:{e}'
cands=[]
for dirn in DIRS:
    p=os.path.join(KBROOT,dirn)
    if not os.path.isdir(p): continue
    for fn in sorted(os.listdir(p)):
        if not fn.endswith('.md'): continue
        full=os.path.join(p,fn); text=open(full,encoding='utf-8').read()
        m=FULL.search(text)
        if not m: continue
        if m.group(1) not in cache and not MARK.search(text.split('##')[0]):
            cands.append((dirn+'/'+fn, m.group(1)))
oos=[]; gone=[]; hidden=[]; err=[]
for f,s in cands:
    st=bc(s)
    if st=='inv==0': oos.append((f,s))
    elif st=='inv>0': hidden.append((f,s))
    elif st=='gone': gone.append((f,s))
    else: err.append((f,s,st))
print(f"absent-from-OH-cache (unflagged): {len(cands)}  | OOS(inv==0):{len(oos)} hidden(inv>0):{len(hidden)} gone:{len(gone)} err:{len(err)}")
print("HIDDEN in-stock (leave as-is):"); [print(f"   {f}  {s}") for f,s in hidden]
print("GONE from BC (individual handling):"); [print(f"   {f}  {s}") for f,s in gone]
def flag_oos(path,sku):
    text=open(path,encoding='utf-8').read(); lines=text.split('\n')
    if MARK.search('\n'.join(lines[:12])): return 'skip'
    # update existing Stock/Status in-stock line, else insert after first SKU/Price/URL line
    done=False
    for i,l in enumerate(lines):
        if re.match(r'\*\*(Stock|Status|Availability):\*\*',l):
            lines[i]='**Stock:** OUT OF STOCK (verified 2026-09-10, BC API inventory=0; Onehunga not available online)'
            done=True;break
    if not done:
        idx=0
        for i,l in enumerate(lines):
            if re.match(r'\*\*(SKU|Price|URL):\*\*',l): idx=i
        lines.insert(idx+1,'**Stock:** OUT OF STOCK (verified 2026-09-10, BC API inventory=0; Onehunga not available online)')
    if APPLY: open(path,'w',encoding='utf-8',newline='\r\n').write('\n'.join(lines))
    return 'flag'
res={'flag':0,'skip':0}
for f,s in oos:
    r=flag_oos(os.path.join(KBROOT,f),s); res[r]+=1
print(f"\nAPPLIED: {res}  (apply={APPLY})")
print("OOS-flagged files:")
for f,s in oos: print(f"   {f}")
