# audit-geo-hermes.ps1
# Hermes Agent version — scans all GEO markdown files, compares Price and Stock against BC API.
# Outputs change-report.json with files that need updating.
#
# Usage:
#   .\tools\audit-geo-hermes.ps1
#   .\tools\audit-geo-hermes.ps1 -CategoryDir "power-supplies"   # single category
#   .\tools\audit-geo-hermes.ps1 -DryRun                         # show report, no file write
#
# Output: tools\change-report.json
#
# Stock logic:
#   BC stores stock in custom fields, NOT inventory_level.
#   Fields: __Stock Available Onehunga (OH), __Stock Available Wellington (WL),
#           __Stock Available St Lukes (SL), __Stock Available Supplier (SU)
#   Total = OH + WL + SL + SU

param(
    [string]$CategoryDir = "",
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# --- Config ---
$BC_STORE   = "ms4wz8cgi2"
$BC_TOKEN   = "iedxfd72bgz2h46qz2pyc7ghsllrw01"
$BASE_URL   = "https://api.bigcommerce.com/stores/$BC_STORE/v3"
$GEO_ROOT   = $PSScriptRoot | Split-Path   # geo/ root
$REPORT_OUT = Join-Path $PSScriptRoot "change-report.json"

$headers = @{
    "X-Auth-Token" = $BC_TOKEN
    "Accept"       = "application/json"
}

# --- Helpers ---
function Get-BCProduct([string]$sku) {
    $url = "$BASE_URL/catalog/products?sku=$([uri]::EscapeDataString($sku))&include_fields=id,name,sku,price,availability,is_visible"
    $r = Invoke-RestMethod -Uri $url -Headers $headers -Method GET
    return $r.data | Select-Object -First 1
}

function Get-BCStock([int]$productId) {
    $url = "$BASE_URL/catalog/products/$productId/custom-fields"
    $r = Invoke-RestMethod -Uri $url -Headers $headers -Method GET
    $cf = $r.data

    function Get-Field([string]$name) {
        $val = ($cf | Where-Object { $_.name -eq $name } | Select-Object -First 1).value
        if ($null -eq $val -or $val -eq "") { return 0 }
        $n = 0
        if ([int]::TryParse($val, [ref]$n)) { return $n } else { return 0 }
    }

    return @{
        OH    = Get-Field "__Stock Available Onehunga"
        WL    = Get-Field "__Stock Available Wellington"
        SL    = Get-Field "__Stock Available St Lukes"
        SU    = Get-Field "__Stock Available Supplier"
        Total = (Get-Field "__Stock Available Onehunga") +
                (Get-Field "__Stock Available Wellington") +
                (Get-Field "__Stock Available St Lukes") +
                (Get-Field "__Stock Available Supplier")
    }
}

function Parse-GeoFile([string]$path) {
    $content = Get-Content $path -Raw -Encoding UTF8
    $result  = @{ Path = $path; SKU = $null; PriceNZD = $null }

    # **SKU:** PSUTMRKG850W
    if ($content -match '\*\*SKU:\*\*\s+([A-Z0-9\-]+)') {
        $result.SKU = $Matches[1].Trim()
    }
    # **Price:** $179.00 inc GST  (also handles TOMBSTONE files with no price)
    if ($content -match '\*\*Price:\*\*\s+\$([0-9]+(?:\.[0-9]{1,2})?)') {
        $result.PriceNZD = [decimal]$Matches[1]
    }
    # Detect tombstone
    if ($content -match '\*\*Status:\*\*\s+TOMBSTONE') {
        $result.Tombstone = $true
    } else {
        $result.Tombstone = $false
    }

    return $result
}

# --- Scan GEO files ---
Write-Host ""
Write-Host "=== ExtremePC GEO Audit ===" -ForegroundColor Cyan
Write-Host "Root: $GEO_ROOT"
Write-Host ""

if ($CategoryDir) {
    $searchRoot = Join-Path $GEO_ROOT $CategoryDir
    Write-Host "Category filter: $CategoryDir"
} else {
    $searchRoot = $GEO_ROOT
}

$mdFiles = Get-ChildItem -Path $searchRoot -Filter "*.md" -Recurse |
    Where-Object { $_.FullName -notmatch '\\(brands|product-knowledge|tools)\\' -and
                   $_.Name -ne "README.md" -and
                   $_.Name -ne "TEMPLATE.md" -and
                   $_.Name -ne "CLAUDE.md" }

Write-Host "Found $($mdFiles.Count) GEO files to audit"
Write-Host ""

$report    = @()
$callCount = 0
$skipped   = 0

foreach ($file in $mdFiles) {
    $geo = Parse-GeoFile $file.FullName

    # Skip files with no parseable SKU
    if (-not $geo.SKU) {
        Write-Host "  SKIP (no SKU): $($file.Name)" -ForegroundColor DarkGray
        $skipped++
        continue
    }

    # Skip tombstones - they intentionally have no full content
    if ($geo.Tombstone) {
        Write-Host "  TOMB: $($geo.SKU)" -ForegroundColor DarkGray
        $skipped++
        continue
    }

    Write-Host "  Checking $($geo.SKU) ..." -NoNewline

    # --- BC API: product ---
    try {
        $bc = Get-BCProduct $geo.SKU
        $callCount++
    } catch {
        Write-Host " ERROR (product lookup)" -ForegroundColor Red
        $report += [ordered]@{
            sku        = $geo.SKU
            file       = $file.FullName.Replace($GEO_ROOT, "").TrimStart("\")
            error      = "BC API product lookup failed: $($_.Exception.Message)"
            needs_update = $false
        }
        continue
    }

    if (-not $bc) {
        Write-Host " NOT FOUND in BC" -ForegroundColor Yellow
        $report += [ordered]@{
            sku          = $geo.SKU
            file         = $file.FullName.Replace($GEO_ROOT, "").TrimStart("\")
            error        = "SKU not found in BC catalog"
            needs_update = $false
        }
        continue
    }

    # --- BC API: custom fields (stock) ---
    # Rate-limit: pause every 40 calls (BC limit ~150 req/30s)
    if ($callCount -gt 0 -and $callCount % 40 -eq 0) {
        Write-Host ""
        Write-Host "  [Rate limit pause 3s after $callCount calls]" -ForegroundColor DarkYellow
        Start-Sleep -Seconds 3
    }

    try {
        $stock = Get-BCStock $bc.id
        $callCount++
    } catch {
        Write-Host " ERROR (custom fields)" -ForegroundColor Red
        $report += [ordered]@{
            sku        = $geo.SKU
            file       = $file.FullName.Replace($GEO_ROOT, "").TrimStart("\")
            error      = "BC API custom-fields lookup failed: $($_.Exception.Message)"
            needs_update = $false
        }
        continue
    }

    # --- Compare price ---
    $bcPriceNZD   = [math]::Round([decimal]$bc.price * 1.15, 2)
    $geoPriceNZD  = $geo.PriceNZD
    $priceDelta   = if ($geoPriceNZD) { [math]::Abs($bcPriceNZD - $geoPriceNZD) } else { 9999 }
    $priceChanged = ($priceDelta -gt 0.05)  # more than 5c difference → flag

    # --- Stock assessment ---
    $totalStock    = $stock.Total
    $wasOOS        = ($totalStock -eq 0)
    $stockSummary  = "OH=$($stock.OH) WL=$($stock.WL) SL=$($stock.SL) SU=$($stock.SU) | Total=$totalStock"

    # GEO file stock hint: try to detect if GEO says "supplier only" vs "retail"
    $geoContent     = Get-Content $file.FullName -Raw -Encoding UTF8
    $geoHasRetail   = $geoContent -match 'Onehunga|Wellington|St Lukes' -and $geoContent -notmatch 'supplier \(3'
    $bcHasRetail    = ($stock.OH + $stock.WL + $stock.SL) -gt 0
    $stockShifted   = ($geoHasRetail -ne $bcHasRetail)

    # Tombstone trigger: total stock = 0
    $needsTombstone = ($totalStock -eq 0)

    $needsUpdate = ($priceChanged -or $stockShifted -or $needsTombstone)

    # Status indicator
    if ($needsTombstone) {
        $status = "OOS"
        $color  = "Red"
    } elseif ($needsUpdate) {
        $status = "CHANGED"
        $color  = "Yellow"
    } else {
        $status = "OK"
        $color  = "Green"
    }

    Write-Host " [$status]" -ForegroundColor $color

    if ($needsUpdate) {
        Write-Host "    GEO price: `$$geoPriceNZD  →  BC price: `$$bcPriceNZD" -ForegroundColor DarkYellow
        Write-Host "    Stock: $stockSummary" -ForegroundColor DarkYellow
    }

    $report += [ordered]@{
        sku             = $geo.SKU
        file            = $file.FullName.Replace($GEO_ROOT, "").TrimStart("\")
        needs_update    = $needsUpdate
        needs_tombstone = $needsTombstone
        price_geo_nzd   = $geoPriceNZD
        price_bc_nzd    = $bcPriceNZD
        price_changed   = $priceChanged
        stock           = $stockSummary
        stock_shifted   = $stockShifted
        bc_name         = $bc.name
    }
}

# --- Summary ---
$changed   = @($report | Where-Object { $_.needs_update -eq $true })
$tombstone = @($report | Where-Object { $_.PSObject.Properties['needs_tombstone'] -and $_.needs_tombstone -eq $true })
$errors    = @($report | Where-Object { $_.Contains('error') })
$ok        = @($report | Where-Object { $_.needs_update -eq $false -and -not $_.Contains('error') })

Write-Host ""
Write-Host "=== Summary ===" -ForegroundColor Cyan
Write-Host "  Total files scanned : $($mdFiles.Count)"
Write-Host "  Skipped (no SKU/tomb): $skipped"
Write-Host "  OK (no changes)     : $($ok.Count)" -ForegroundColor Green
Write-Host "  Needs update        : $($changed.Count)" -ForegroundColor Yellow
Write-Host "  Needs tombstone     : $($tombstone.Count)" -ForegroundColor Red
Write-Host "  Errors              : $($errors.Count)" -ForegroundColor Red
Write-Host "  BC API calls made   : $callCount"
Write-Host ""

if (-not $DryRun) {
    $reportData = [ordered]@{
        generated    = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
        geo_root     = $GEO_ROOT
        summary      = [ordered]@{
            total_scanned   = $mdFiles.Count
            ok              = $ok.Count
            needs_update    = $changed.Count
            needs_tombstone = $tombstone.Count
            errors          = $errors.Count
        }
        changes = $report | Where-Object { $_.needs_update -eq $true -or $_.Contains('error') }
    }

    $reportData | ConvertTo-Json -Depth 5 | Out-File $REPORT_OUT -Encoding UTF8
    Write-Host "Report written: $REPORT_OUT" -ForegroundColor Cyan
} else {
    Write-Host "[DryRun] Report NOT written." -ForegroundColor DarkGray
}

Write-Host ""
if ($changed.Count -gt 0) {
    Write-Host "Files needing update:" -ForegroundColor Yellow
    $report | Where-Object { $_.needs_update -eq $true } | ForEach-Object {
        $flag = if ($_.needs_tombstone) { "[OOS→TOMBSTONE]" } elseif ($_.price_changed) { "[PRICE]" } else { "[STOCK]" }
        Write-Host "  $flag $($_.sku) - $($_.file)"
    }
}
