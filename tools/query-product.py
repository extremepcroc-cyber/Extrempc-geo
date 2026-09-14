#!/usr/bin/env python3
"""
query-product.py — 按 SKU / 型号查产品全景（EVA 实时查询用）

一次调用拿到回答客人所需的一切：价格（含 GST）、库存（OH）、保修、URL、
GEO 知识文件位置、品牌资料位置。目标是替掉 EVA 现写 python -c 单行命令的做法。

Usage:
    python tools/query-product.py COOTMRAS120VB                 # 单个 SKU
    python tools/query-product.py SKU1,SKU2,SKU3                # 多个 SKU（一次 API 调用）
    python tools/query-product.py --search "assassin spirit"    # 按名称模糊搜索

数据来源：
    - BC Catalog API v3（价格 / 计算价 / 库存 custom fields / Subtitle 保修 / URL）
    - 本地 GEO 知识库（product-knowledge/**/{SKU}.md、brands/{brand}.md）

⚠️ 库存：脚本输出真实数字（内部参考），对客必须模糊化：
    0 台 → "Sorry, currently out of stock"
    1-5  → "Only a few left in stock"
    >5   → "We have plenty in stock"
"""

import glob
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

GST = 1.15
GEO_REPO = pathlib.Path(__file__).resolve().parent.parent

# === Credentials ===
_env_candidates = [
    pathlib.Path(os.environ.get("HERMES_PROFILE_DIR", "")) / "extremepc.env",
    pathlib.Path.home() / "AppData/Local/hermes/profiles/exie/extremepc.env",
    GEO_REPO / ".env",
]
for _p in _env_candidates:
    if _p.exists():
        with open(_p, encoding="utf-8") as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _k, _v = _line.split("=", 1)
                    os.environ.setdefault(_k.strip(), _v.strip())

STORE = os.environ.get("BC_STORE_HASH", "")
TOKEN = os.environ.get("BC_ACCESS_TOKEN", "")
if not STORE or not TOKEN:
    print("Error: BC_STORE_HASH / BC_ACCESS_TOKEN not set.", file=sys.stderr)
    sys.exit(1)

BASE = f"https://api.bigcommerce.com/stores/{STORE}/v3"
HEADERS = {"X-Auth-Token": TOKEN, "Accept": "application/json"}


def api_get(path):
    req = urllib.request.Request(f"{BASE}{path}", headers=HEADERS, method="GET")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(2)
                continue
            print(f"  [API {e.code}] {path}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"  [Err] {e}", file=sys.stderr)
            return None
    return None


def cf_values(custom_fields, key):
    """All values for a custom-field name — BC can have several fields with
    the same name (e.g. two 'Subtitle' fields: one warranty, one upsell)."""
    out = []
    for cf in custom_fields or []:
        if key.lower() in (cf.get("name") or "").lower():
            v = (cf.get("value") or "").strip()
            if v:
                out.append(v)
    return out


def cf_value(custom_fields, key):
    """First value for a custom-field name."""
    vals = cf_values(custom_fields, key)
    return vals[0] if vals else ""


def stock_phrase(oh):
    if oh <= 0:
        return "❌ out of stock → 对客: 'Sorry, currently out of stock'"
    if oh <= 5:
        return f"⚠️ {oh} 台 → 对客: 'Only a few left in stock'"
    return f"✅ {oh} 台 → 对客: 'We have plenty in stock'"


def find_geo_file(sku):
    """Locate GEO knowledge file(s) for this SKU. product-knowledge/ first,
    deduped case-insensitively (repo has both Foo.md and foo.md variants)."""
    sku_up = sku.upper()
    seen, pk, other = set(), [], []
    for p in glob.glob(str(GEO_REPO / "**" / f"{sku_up}.md"), recursive=True):
        rel = pathlib.Path(p).relative_to(GEO_REPO).as_posix()
        key = rel.lower()
        if key in seen:
            continue
        seen.add(key)
        if rel.startswith("2-EOL"):
            rel += "  (已下架/EOL)"
        (pk if rel.startswith("product-knowledge/") else other).append(rel)
    return sorted(pk) + sorted(other)


def find_brand_file(brand):
    """Brand profile file(s), case-insensitive dedupe."""
    if not brand:
        return []
    out, seen = [], set()
    for p in glob.glob(str(GEO_REPO / "brands" / "*.md")):
        stem = pathlib.Path(p).stem
        if stem.lower() == brand.lower() and stem.lower() not in seen:
            seen.add(stem.lower())
            out.append(f"brands/{stem}.md")
    return out


def brand_map(brand_ids):
    """Resolve brand ids → names (single API call)."""
    ids = sorted({i for i in brand_ids if i})
    if not ids:
        return {}
    d = api_get(f"/catalog/brands?id:in={','.join(map(str, ids))}&limit=200")
    return {b["id"]: b["name"] for b in (d or {}).get("data", [])}


def render(p, brands):
    name = p.get("name", "?")
    sku = p.get("sku", "?")
    mpn = p.get("mpn") or "—"
    price_ex = p.get("price") or 0
    calc_ex = p.get("calculated_price")
    calc_ex = calc_ex if calc_ex else price_ex
    price_gst = round(price_ex * GST, 2)
    calc_gst = round(calc_ex * GST, 2)
    on_sale = calc_ex < price_ex

    cfs = p.get("custom_fields", [])
    oh_raw = cf_value(cfs, "Onehunga")
    try:
        oh = int(oh_raw)
    except (TypeError, ValueError):
        oh = 0
    # ExtremePC stores warranty text in a Subtitle field — but products can
    # carry several Subtitle fields (one warranty, one upsell), so pick the
    # one that actually mentions warranty.
    subtitles = cf_values(cfs, "Subtitle")
    warranty = next((s for s in subtitles if "warranty" in s.lower()), "")
    extras = [s for s in subtitles if s != warranty]
    brand = brands.get(p.get("brand_id"), "")
    url = "https://www.extremepc.co.nz" + (p.get("custom_url") or {}).get("url", "")

    lines = [f"=== {sku} ==="]
    lines.append(f"名称:  {name}")
    lines.append(f"MPN:   {mpn}")
    if on_sale:
        save = round(price_gst - calc_gst, 2)
        lines.append(f"价格:  NZD ${calc_gst:.2f} (incl. GST)  [原价 ${price_gst:.2f} — on sale, 省 ${save:.2f}]")
    else:
        lines.append(f"价格:  NZD ${price_gst:.2f} (incl. GST)")
    lines.append(f"库存:  Onehunga {stock_phrase(oh)}")
    if warranty:
        lines.append(f"保修:  {warranty}")
    for e in extras:
        lines.append(f"备注:  {e}")
    lines.append(f"URL:   {url or '—'}")

    geo = find_geo_file(sku)
    lines.append(f"GEO:   {', '.join(geo) if geo else '（无 GEO 文件 — 只有 BC 数据）'}")
    if brand:
        bf = find_brand_file(brand)
        lines.append(f"品牌:  {brand}{' → ' + ', '.join(bf) if bf else '（无品牌资料）'}")
    return "\n".join(lines)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if "--search" in sys.argv:
        i = sys.argv.index("--search")
        if i + 1 >= len(sys.argv):
            print("Usage: --search <keywords>", file=sys.stderr)
            sys.exit(1)
        terms = sys.argv[i + 1]
        d = api_get(
            "/catalog/products?name:like=" + urllib.parse.quote(terms)
            + "&include_fields=id,name,sku,mpn,price,calculated_price,brand_id,custom_url"
            + "&include=custom_fields&limit=20"
        )
        items = (d or {}).get("data", [])
        if not items:
            print(f"未找到匹配 '{terms}' 的产品（BC 全库搜索）")
            return
        print(f"匹配 '{terms}' 的产品 ({len(items)} 个):\n")
        for p in items:
            oh = cf_value(p.get("custom_fields", []), "Onehunga")
            print(f"  {p.get('sku'):20s} ${round((p.get('calculated_price') or p.get('price', 0)) * GST, 2):>9.2f}  OH={oh or '0':>4}  {p.get('name', '')[:70]}")
        print("\n提示: 用 SKU 再查一次可拿全景（保修/GEO文件/品牌资料）")
        return

    if not args:
        print(__doc__)
        sys.exit(1)

    skus = [s.strip() for s in args[0].split(",") if s.strip()]
    d = api_get(
        f"/catalog/products?sku:in={urllib.parse.quote(','.join(skus))}"
        "&include_fields=id,name,sku,mpn,price,calculated_price,brand_id,custom_url"
        "&include=custom_fields&limit=50"
    )
    items = (d or {}).get("data", [])
    if not items:
        print(f"❌ BC 中查不到这些 SKU: {', '.join(skus)}")
        print("   可能已从目录移除（EOL），或 SKU 拼写有误。")
        return

    brands = brand_map([p.get("brand_id") for p in items])
    for p in items:
        print(render(p, brands))
        print()

    found = {p.get("sku", "").upper() for p in items}
    missing = [s for s in skus if s.upper() not in found]
    if missing:
        print(f"⚠️ 未找到: {', '.join(missing)}")


if __name__ == "__main__":
    main()
