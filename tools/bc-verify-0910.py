import json, os, re, urllib.request, urllib.parse

# load token
base = None
for envp in [
  os.path.expanduser('~/Documents/GitHub/Extrempc-geo/.env'),
  os.path.expanduser('~/AppData/Local/hermes/profiles/exie/extremepc.env'),
]:
    if os.path.exists(envp):
        for line in open(envp):
            line=line.strip()
            if line.startswith('BC_ACCESS_TOKEN='):
                TOKEN=line.split('=',1)[1]
            if line.startswith('BC_API_BASE='):
                BASE=line.split('=',1)[1]
print("base",BASE)

def bc(sku):
    url=f"{BASE}/catalog/products?sku={urllib.parse.quote(sku)}&include_fields=id,name,sku,price,calculated_price,custom_url,inventory_level&limit=1"
    req=urllib.request.Request(url, headers={'X-Auth-Token':TOKEN,'Accept':'application/json'})
    with urllib.request.urlopen(req,timeout=30) as r:
        d=json.load(r)
    if not d.get('data'): return None
    p=d['data'][0]
    inc = round((p.get('calculated_price') or p.get('price'))*1.15,2)
    return {'name':p['name'],'inv':p['inventory_level'],
            'ex':p.get('calculated_price'),'exlist':p.get('price'),'inc':inc,
            'url':(p.get('custom_url') or {}).get('url')}

# sample of mismatches (spread across categories + the big outliers)
sample=['CASJOND200W','MBASRW90WE','MBASUPAX870ECWF','COOTMRAS120V2P','CASJONN3','COOSEGIM360B','CASZALI3NEOB','COOVALV360W','CASJONBO400G','MBASRB850CWF']
for s in sample:
    try:
        r=bc(s)
        print(f"{s:20} -> {json.dumps(r,ensure_ascii=False)}")
    except Exception as e:
        print(f"{s:20} -> ERROR {e}")
