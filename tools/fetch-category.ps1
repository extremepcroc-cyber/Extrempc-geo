# fetch-category.ps1
# Fetches all in-stock products from a BC category and outputs a JSON file
# ready for AI agents to use when writing GEO files.
#
# Usage:
#   .\tools\fetch-category.ps1 -CategoryId 351
#   .\tools\fetch-category.ps1 -CategoryId 349 -IncludeOOS
#   .\tools\fetch-category.ps1 -CategoryId 347 -OutputFile "tools\fans.json"
#
# Output: tools\category-{id}-products.json  (or -OutputFile path)
#
# Each product entry contains everything needed to write a GEO file:
#   sku, name, mpn, price_nzd_inc_gst, url, stock (OH/WL/SL/SU),
#   brand, description_html, custom_fields (all of them)

param(
    [Parameter(Mandatory)]
    [int]$CategoryId,

    [switch]$IncludeOOS,   # include products with zero stock (default: skip)

    [string]$OutputFile = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# --- Config ---
$BC_STORE = "ms4wz8cgi2"
$BC_TOKEN = "iedxfd72bgz2h46qz2pyc7ghsllrw01"
$BASE_URL = "https://api.bigcommerce.com/stores/$BC_STORE/v3"

$headers = @{
    "X-Auth-Token" = $BC_TOKEN
    "Accept"       = "application/json"
}

if ($OutputFile -eq "") {
    $OutputFile = Join-Path $PSScriptRoot "category-$CategoryId-products.json"
}

# --- Helpers ---
function Get-AllPages([string]$url) {
    # Follows BC pagination, returns all data items across pages
    $allData = @()
    $page = 1
    do {
        $paged = "$url&page=$page&limit=50"
        $r = Invoke-RestMethod -Uri $paged -Headers $headers -Method GET
        if ($r.data) { $allData += $r.data }
        $totalPages = [math]::Ceiling($r.meta.pagination.total / $r.meta.pagination.per_page)
        $page++
    } while ($page -le $totalPages -and $r.data.Count -gt 0)
    return $allData
}

function Get-CustomFields([int]$productId) {
    $url = "$BASE_URL/catalog/products/$productId/custom-fields"
    $r = Invoke-RestMethod -Uri $url -Headers $headers -Method GET
    $result = [ordered]@{}
    foreach ($cf in $r.data) {
        $result[$cf.name] = $cf.value
    }
    return $result
}

function Get-Stock([hashtable]$cf) {
    # Only OH (Onehunga) = customer-available stock. WL/SL/SU are internal and do not
    # represent stock customers can actually receive — do not sum them.
    $v = $cf["__Stock Available Onehunga"]
    $oh = 0
    if ($v -and $v -ne "") { [int]::TryParse($v, [ref]$oh) | Out-Null }
    return [ordered]@{
        OH    = $oh
        total = $oh
    }
}

# --- Main ---
Write-Host ""
Write-Host "=== BC Category Fetch ===" -ForegroundColor Cyan
Write-Host "Category ID : $CategoryId"
Write-Host "Include OOS : $IncludeOOS"
Write-Host ""

# Step 1: fetch product list for category
Write-Host "Fetching product list..." -NoNewline
$listUrl = "$BASE_URL/catalog/products?categories:in=$CategoryId&include_fields=id,name,sku,mpn,price,brand_id,custom_url,availability,is_visible&include=custom_fields"
$products = Get-AllPages $listUrl
Write-Host " $($products.Count) products found" -ForegroundColor Green

# Step 2: fetch brands lookup (id -> name)
Write-Host "Fetching brand list..." -NoNewline
$brandsUrl = "$BASE_URL/catalog/brands?limit=250"
$brandData = Invoke-RestMethod -Uri $brandsUrl -Headers $headers -Method GET
$brandMap = @{}
foreach ($b in $brandData.data) { $brandMap[$b.id] = $b.name }
Write-Host " $($brandMap.Count) brands cached" -ForegroundColor Green
Write-Host ""

$results  = @()
$callCount = 0
$skipped  = 0

foreach ($p in $products) {
    Write-Host "  [$($p.sku)] $($p.name)" -NoNewline

    # Rate limit: pause every 40 calls
    if ($callCount -gt 0 -and $callCount % 40 -eq 0) {
        Write-Host ""
        Write-Host "  [Rate limit pause 3s after $callCount calls]" -ForegroundColor DarkYellow
        Start-Sleep -Seconds 3
    }

    # Custom fields (stock + specs)
    try {
        $cf = Get-CustomFields $p.id
        $callCount++
    } catch {
        Write-Host " ERROR (custom-fields)" -ForegroundColor Red
        continue
    }

    $stock = Get-Stock $cf

    # Skip OOS unless -IncludeOOS (OOS = OH stock = 0)
    if ($stock.total -eq 0 -and -not $IncludeOOS) {
        Write-Host " [OOS - skipped]" -ForegroundColor DarkGray
        $skipped++
        continue
    }

    # Price: BC price is ex-GST, multiply x1.15 for NZD inc GST
    # Output as plain integer (no commas, no decimals) to avoid PowerShell formatting bugs
    $priceNZD = [int][math]::Round([decimal]$p.price * 1.15)

    # URL: use custom_url if present, else build from slug
    $slug = if ($p.custom_url -and $p.custom_url.url) { $p.custom_url.url.Trim('/') } else { "" }
    $url  = if ($slug) { "https://www.extremepc.co.nz/$slug/" } else { "TBC" }

    # Brand name
    $brand = if ($brandMap.ContainsKey($p.brand_id)) { $brandMap[$p.brand_id] } else { "TBC" }

    # MPN
    $mpn = if ($p.mpn -and $p.mpn -ne "") { $p.mpn } else { "TBC" }

    $entry = [ordered]@{
        sku                = $p.sku
        name               = $p.name
        mpn                = $mpn
        brand              = $brand
        price_nzd_inc_gst  = $priceNZD
        url                = $url
        stock              = $stock
        custom_fields      = $cf
    }

    $stockStr = "OH=$($stock.OH)"
    Write-Host " [IN STOCK: $stockStr] `$$priceNZD" -ForegroundColor Green

    $results += $entry
}

# --- Output ---
Write-Host ""
Write-Host "=== Summary ===" -ForegroundColor Cyan
Write-Host "  Total found  : $($products.Count)"
Write-Host "  OOS skipped  : $skipped" -ForegroundColor DarkGray
Write-Host "  Exported     : $($results.Count)" -ForegroundColor Green
Write-Host "  API calls    : $callCount"
Write-Host ""

$output = [ordered]@{
    generated   = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    category_id = $CategoryId
    in_stock_only = (-not $IncludeOOS)
    count       = $results.Count
    products    = $results
}

$output | ConvertTo-Json -Depth 10 | Out-File $OutputFile -Encoding UTF8
Write-Host "Output written: $OutputFile" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next step: give this JSON to the AI agent to write GEO files." -ForegroundColor White
