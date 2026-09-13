import json, os, urllib.request

env = {}
for line in open(os.path.expanduser("~/Documents/GitHub/Extrempc-geo/.env")):
    line=line.strip()
    if "=" in line and not line.startswith("#"):
        k,v=line.split("=",1); env[k]=v
TOKEN=env["BC_ACCESS_TOKEN"]; BASE=env["BC_API_BASE"].rstrip("/")

def bc_batch(skus):
    url=f"{BASE}/catalog/products?sku:in={','.join(skus)}&include_fields=id,name,sku,price,calculated_price,custom_url,inventory_level,availability&include=custom_fields&limit=100"
    req=urllib.request.Request(url, headers={"X-Auth-Token":TOKEN,"Accept":"application/json"})
    d=json.load(urllib.request.urlopen(req, timeout=40))
    out={}
    for p in d.get("data",[]):
        cf=p.get("custom_fields") or []
        oh=None
        for c in cf:
            if c.get("name") in ("__Stock Available Onehunga","Onehunga"):
                oh=c.get("value")
        out[p["sku"]]={"id":p["id"],"name":p["name"],"price":p.get("price"),
                       "calc":p.get("calculated_price"),"url":(p.get("custom_url") or {}).get("url"),
                       "inv":p.get("inventory_level"),"oh":oh}
    return out

candidates=["MONACEX27UX1","MONACEX32X5","MONACEX34X5",
            "KEYAULH68HBM","KEYAULH68HWS","KEYAULN75WI","MOSAULSC620B"]
r=bc_batch(candidates)
for s in candidates:
    if s not in r: print(f"\n=== {s}: NOT FOUND / delisted ==="); continue
    p=r[s]
    def gst(x): return round(x*1.15,2) if x is not None else None
    print(f"\n=== {s} ===")
    print(f"  name: {p['name']}")
    print(f"  id={p['id']}")
    print(f"  price(list)={p['price']} -> ${gst(p['price'])} incl GST")
    print(f"  calc={p['calc']} -> ${gst(p['calc'])} incl GST   on_sale={p['calc'] is not None and p['calc'] is not None and p['calc'] < p['price']}")
    print(f"  inventory_level={p['inv']}  OH(custom_field)={p['oh']}")
    print(f"  URL: {p['url']}")
