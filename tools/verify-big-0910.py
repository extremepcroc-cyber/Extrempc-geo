import json, os, urllib.request, urllib.parse
for envp in [os.path.expanduser('~/Documents/GitHub/Extrempc-geo/.env'),
             os.path.expanduser('~/AppData/Local/hermes/profiles/exie/extremepc.env')]:
    if os.path.exists(envp):
        for line in open(envp):
            line=line.strip()
            if line.startswith('BC_ACCESS_TOKEN='): TOKEN=line.split('=',1)[1]
            if line.startswith('BC_API_BASE='): BASE=line.split('=',1)[1]
def bc(sku):
    url=f"{BASE}/catalog/products?sku={urllib.parse.quote(sku)}&include_fields=id,name,sku,price,calculated_price,inventory_level,is_visible&limit=1"
    req=urllib.request.Request(url,headers={'X-Auth-Token':TOKEN,'Accept':'application/json'})
    with urllib.request.urlopen(req,timeout=30) as r: d=json.load(r)
    if not d.get('data'): return "REMOVED/EMPTY"
    p=d['data'][0]; inc=round((p.get('calculated_price') or p.get('price'))*1.15,2)
    return f"inv={p['inventory_level']} vis={p.get('is_visible')} calc_ex={p.get('calculated_price')} list_ex={p.get('price')} inc={inc} | {p['name'][:45]}"
# largest jumps (KB -> cache) + removed-today
big=[('SSDHPFX900P512',99,229),('SSDSAM9100P4',1679,1999),('GPUASU5070TP16',2099,2519),
     ('PSUABEPT2000',799,1099),('GPUMSI57V2OB',1410,1699),('MONACEXZ270U',339,379),
     ('RAMGSKM5360RB',828.99,859),('COOJONCR1000V2PRW',58.99,28.75),
     ('COOTMRPV36AB','removed-today','?'),('MONAOC27E40L','removed-today','?'),('MOSMCHK7UWG','removed-today','?')]
for s,kb,tgt in big:
    print(f"{s:22} KB={kb} cache={tgt}  ==>  {bc(s)}")
