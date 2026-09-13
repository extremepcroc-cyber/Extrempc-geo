import json, os, re, glob

KB = os.path.expanduser("~/Documents/GitHub/Extrempc-geo/product-knowledge")
base = os.path.expanduser("~/AppData/Local/hermes/profiles/exie-web/workspace/EVAcache")

def load(date):
    d = json.load(open(os.path.join(base, date, "products.json")))
    return {p["sku"]: p for p in d["products"]}

new = load("2026-09-11")
old = load("2026-09-10")

# Category dirs considered "core hardware" (per convention: build KB files)
CORE_DIRS = ["computer-cases","cooling","gpus","motherboards","power-supplies",
             "ram","ssds","ssd","keyboards","gaming-keyboards","mice","headsets","monitors"]
# CPU dirs: OEM tray -> NO KB file by convention
NOFILE_DIRS = ["cpus","hdd","chairs"]

# Build index: file -> set of SKUs found in the file
kb_index = {}  # file -> {sku: linecontext}
sku_to_file = {}  # sku -> [files]

sku_re = re.compile(r"\b([A-Z]{2}[A-Z0-9]{3,})\b")

for cdir in CORE_DIRS + NOFILE_DIRS:
    path = os.path.join(KB, cdir)
    if not os.path.isdir(path): continue
    for f in glob.glob(os.path.join(path, "*.md")):
        txt = open(f, encoding="utf-8", errors="ignore").read()
        skus = set(sku_re.findall(txt))
        # filter obvious false positives (very short or words)
        skus = {s for s in skus if len(s) >= 5}
        kb_index[os.path.relpath(f, KB)] = skus
        for s in skus:
            sku_to_file.setdefault(s, []).append(os.path.relpath(f, KB))

# Also scan root-level files
for f in glob.glob(os.path.join(KB, "*.md")):
    rel = os.path.relpath(f, KB)
    txt = open(f, encoding="utf-8", errors="ignore").read()
    skus = {s for s in sku_re.findall(txt) if len(s)>=5}
    for s in skus:
        sku_to_file.setdefault(s, []).append(rel)

added = sorted(set(new)-set(old))
removed = sorted(set(old)-set(new))
common_price_changed = [s for s in sorted(set(old)&set(new)) if old[s]["price_nzd_inc_gst"]!=new[s]["price_nzd_inc_gst"] or old[s]["on_sale"]!=new[s]["on_sale"]]

def kb_for(sku):
    return sku_to_file.get(sku, [])

print("########## ADDED — KB file status ##########")
for s in added:
    print(f"\n{s} | {new[s]['name'][:60]} | ${new[s]['price_nzd_inc_gst']} OH={new[s]['oh_stock']}")
    print(f"   KB files: {kb_for(s) if kb_for(s) else 'NONE (candidate for new file)'}")

print("\n\n########## REMOVED — KB file status ##########")
for s in removed:
    print(f"{s} | {old[s]['name'][:60]} | KB files: {kb_for(s) if kb_for(s) else 'none'}")

print("\n\n########## COMMON price-changed — KB file status ##########")
for s in common_price_changed:
    f = kb_for(s)
    if f:
        print(f"⚠ {s} | {new[s]['name'][:50]} | ${old[s]['price_nzd_inc_gst']} -> ${new[s]['price_nzd_inc_gst']} | KB: {f}")

print("\n\n########## KB file totals ##########")
print(f"core-hardware dirs KB .md files: {sum(1 for f in kb_index if f.split('/')[0] in CORE_DIRS)}")
