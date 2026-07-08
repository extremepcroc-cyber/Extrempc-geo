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
# Optimisations vs naive approach:
#   - Server-side filter: availability=available&is_visible=true  → skips hidden/disabled products
#   - include=custom_fields in product list query → custom fields inline, no per-product calls
#   - Only OH (Onehunga) read for stock — WL/SL/SU are internal, not customer-available
#   - Net result: 2 API calls total (product list + brands), regardless of category size

param(
    [Parameter(Mandatory)]
    [int]$CategoryId,

    [switch]$IncludeOOS,   # include products with OH=0 (default: skip)

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
    $allData = @()
    $page = 1
    do {
        $paged = "$url&page=$page&limit=250"
        $r = Invoke-RestMethod -Uri $paged -Headers $headers -Method GET
        if ($r.data) { $allData += $r.data }
        $totalPages = $r.meta.pagination.total_pages
        $page++
    } while ($page -le $totalPages -and $r.data.Count -gt 0)
    return $allData
}

function Get-OH([array]$customFields) {
    # Only Onehunga = customer-available stock
    $cf = $customFields | Where-Object { $_.name -eq "__Stock Available Onehunga" } | Select-Object -First 1
    $oh = 0
    if ($cf -and $cf.value -ne "") { [int]::TryParse($cf.value, [ref]$oh) | Out-Null }
    return $oh
}

function Get-CF-Map([array]$customFields) {
    $result = [ordered]@{}
    foreach ($cf in $customFields) { $result[$cf.name] = $cf.value }
    return $result
}

# --- Main ---
Write-Host ""
Write-Host "=== BC Category Fetch ===" -ForegroundColor Cyan
Write-Host "Category ID : $CategoryId"
Write-Host "Include OOS : $IncludeOOS"
Write-Host ""

# Single paginated call — products + custom_fields inline, hidden/disabled filtered server-side
Write-Host "Fetching products..." -NoNewline
$listUrl = "$BASE_URL/catalog/products" +
           "?categories:in=$CategoryId" +
           "&availability=available" +
           "&is_visible=true" +
           "&include_fields=id,name,sku,mpn,price,brand_id,custom_url" +
           "&include=custom_fields"
$products = Get-AllPages $listUrl
Write-Host " $($products.Count) visible products" -ForegroundColor Green

# Brand lookup (one call)
Write-Host "Fetching brands..." -NoNewline
$brandData = Invoke-RestMethod -Uri "$BASE_URL/catalog/brands?limit=250" -Headers $headers -Method GET
$brandMap  = @{}
foreach ($b in $brandData.data) { $brandMap[$b.id] = $b.name }
Write-Host " $($brandMap.Count) brands cached" -ForegroundColor Green
Write-Host ""

$results = @()
$skipped = 0

foreach ($p in $products) {
    $oh = Get-OH $p.custom_fields

    if ($oh -eq 0 -and -not $IncludeOOS) {
        $skipped++
        continue
    }

    $priceNZD = [int][math]::Round([decimal]$p.price * 1.15)
    $slug     = if ($p.custom_url -and $p.custom_url.url) { $p.custom_url.url.Trim('/') } else { "" }
    $url      = if ($slug) { "https://www.extremepc.co.nz/$slug/" } else { "TBC" }
    $brand    = if ($brandMap.ContainsKey($p.brand_id)) { $brandMap[$p.brand_id] } else { "TBC" }
    $mpn      = if ($p.mpn -and $p.mpn -ne "") { $p.mpn } else { "TBC" }

    $status = if ($oh -eq 0) { "[OOS]" } else { "[OH=$oh]" }
    Write-Host "  $status $($p.sku)  `$$priceNZD  $($p.name)" -ForegroundColor $(if ($oh -gt 0) { "Green" } else { "DarkGray" })

    $results += [ordered]@{
        sku               = $p.sku
        name              = $p.name
        mpn               = $mpn
        brand             = $brand
        price_nzd_inc_gst = $priceNZD
        url               = $url
        stock             = [ordered]@{ OH = $oh }
        custom_fields     = Get-CF-Map $p.custom_fields
    }
}

# --- Output ---
Write-Host ""
Write-Host "=== Summary ===" -ForegroundColor Cyan
Write-Host "  Visible products : $($products.Count)"
Write-Host "  OOS skipped      : $skipped" -ForegroundColor DarkGray
Write-Host "  Exported         : $($results.Count)" -ForegroundColor Green
Write-Host "  API calls made   : 2  (products + brands)" -ForegroundColor Green
Write-Host ""

$output = [ordered]@{
    generated     = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    category_id   = $CategoryId
    in_stock_only = (-not $IncludeOOS)
    count         = $results.Count
    products      = $results
}

$output | ConvertTo-Json -Depth 10 | Out-File $OutputFile -Encoding UTF8
Write-Host "Output written: $OutputFile" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next step: give this JSON to the AI agent to write GEO files." -ForegroundColor White
