import json, os, re, collections

KBROOT = os.path.expanduser('~/Documents/GitHub/Extrempc-geo/product-knowledge')
CACHE909 = os.path.expanduser('~/AppData/Local/hermes/profiles/exie-web/workspace/EVAcache/2026-09-09')
CACHE910 = os.path.expanduser('~/AppData/Local/hermes/profiles/exie-web/workspace/EVAcache/2026-09-10')

def load(p):
    d=json.load(open(p+'/products.json'))
    return {x['sku']:x for x in d['products']}
c909=load(CACHE909); c910=load(CACHE910)
print("09-09 in-stock:",len(c909),"| 09-10 in-stock:",len(c910))

added = set(c910)-set(c909)   # appeared today
removed = set(c909)-set(c910) # gone today
print("\n=== ADDED today (new arrivals candidates):",len(added))
for s in sorted(added): print("  +",s,"|",c910[s]['name'][:60],"| cats",c910[s]['categories'],"| OH",c910[s]['oh_stock'],"| $",c910[s]['price_nzd_inc_gst'])
print("\n=== REMOVED today (OOS/restock candidates):",len(removed))
for s in sorted(removed): print("  -",s,"|",c909[s]['name'][:60],"| wasOH",c909[s]['oh_stock'],"| was$",c909[s]['price_nzd_inc_gst'])

# price/stock changes for SKUs present both days
changed_price=[]
for s in set(c909)&set(c910):
    if abs(c909[s]['price_nzd_inc_gst']-c910[s]['price_nzd_inc_gst'])>0.005:
        changed_price.append((s,c909[s]['price_nzd_inc_gst'],c910[s]['price_nzd_inc_gst'],c910[s]['name'][:45]))
print("\n=== PRICE CHANGED day-over-day:",len(changed_price))
for s,a,b,n in sorted(changed_price): print(f"   {s:20} ${a:>9.2f} -> ${b:>9.2f}  {n}")
