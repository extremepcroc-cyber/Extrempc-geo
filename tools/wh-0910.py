import json, os, urllib.request
for envp in [os.path.expanduser('~/Documents/GitHub/Extrempc-geo/.env'),
             os.path.expanduser('~/AppData/Local/hermes/profiles/exie/extremepc.env')]:
    if os.path.exists(envp):
        for line in open(envp):
            line=line.strip()
            if line.startswith('BC_ACCESS_TOKEN='): TOKEN=line.split('=',1)[1]
            if line.startswith('BC_API_BASE='): BASE=line.split('=',1)[1]
def wh(sku):
    url=f"{BASE}/catalog/products?sku={sku}&include_fields=id,name,inventory_level&include[]=inventory_locations&limit=1"
    req=urllib.request.Request(url,headers={'X-Auth-Token':TOKEN,'Accept':'application/json'})
    with urllib.request.urlopen(req,timeout=30) as r: d=json.load(r)
    if not d.get('data'): return "EMPTY"
    p=d['data'][0]
    locs=p.get('inventory_locations') or []
    return f"total_inv={p.get('inventory_level')} | " + " ".join(f"{l.get('location_code')}={l.get('level')}" for l in locs)
for s in ['MOSMCHK7UWG','COOTMRPV36AB','MONAOC27E40L']:
    print(f"{s:16} -> {wh(s)}")
