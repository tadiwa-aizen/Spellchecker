# Build ARPA language models from character corpora using KenLM
# Run this on Windows in PowerShell from the Spellchecker directory
# Usage: .\BUILD_MODELS_WINDOWS.ps1

$ErrorActionPreference = 'Continue'

Write-Host "=========================================="
Write-Host "Building KenLM ARPA Language Models"
Write-Host "=========================================="
Write-Host ""

# Paths
$lmplz = "vcpkg_installed\x64-windows\tools\kenlm\lmplz.exe"
$inputDir = "character_corpora"
$outputDir = "models"
$order = 5  # Using 5-gram to match previous models

# Check if lmplz exists
if (-not (Test-Path $lmplz)) {
    Write-Host "[ERROR] lmplz.exe not found at: $lmplz"
    Write-Host "Please ensure you're in the Spellchecker directory"
    exit 1
}

# Create output directory
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

# Define languages
$languages = @(
    @{Input = "isiZuluUCorpus.txt"; Output = "isiZuluUModel.arpa"; Name = "isiZulu"},
    @{Input = "isiXhosaUCorpus.txt"; Output = "isiXhosaUModel.arpa"; Name = "isiXhosa"},
    @{Input = "isiNdebeleUCorpus.txt"; Output = "isiNdebeleUModel.arpa"; Name = "isiNdebele"},
    @{Input = "siSwatiUCorpus.txt"; Output = "siSwatiUModel.arpa"; Name = "siSwati"}
)

$successCount = 0

foreach ($lang in $languages) {
    $inputPath = Join-Path $inputDir $lang.Input
    $outputPath = Join-Path $outputDir $lang.Output
    
    Write-Host "Building $($lang.Name) model..."
    Write-Host "  Input:  $inputPath"
    Write-Host "  Output: $outputPath"
    Write-Host "  Order:  ${order}-gram"
    
    if (-not (Test-Path $inputPath)) {
        Write-Host "  [WARN] Input file not found, skipping..."
        Write-Host ""
        continue
    }
    
    try {
        # Use CMD to avoid PowerShell pipe buffer issues with large files
        $cmd = "cmd.exe /c `"$lmplz -o $order < `"$inputPath`" > `"$outputPath`" 2>&1`""
        Invoke-Expression $cmd
        
        if (Test-Path $outputPath) {
            $size = (Get-Item $outputPath).Length / 1MB
            if ($size -gt 0.1) {
                Write-Host "  [OK] Model built! Size: $([math]::Round($size, 2)) MB"
                $successCount++
            } else {
                Write-Host "  [ERROR] Model file is too small (likely failed)"
            }
        } else {
            Write-Host "  [ERROR] Model file not created"
        }
    } catch {
        Write-Host "  [ERROR] Failed: $_"
    }
    
    Write-Host ""
}

Write-Host "=========================================="
Write-Host "Complete: $successCount/4 models built"
Write-Host "=========================================="
Write-Host ""

if ($successCount -eq 4) {
    Write-Host "All models built successfully!"
    Write-Host "Models are in: $outputDir\"
    Write-Host ""
    Write-Host "Optional: Copy to kenlm tools directory:"
    Write-Host "  copy models\*.arpa vcpkg_installed\x64-windows\tools\kenlm\"
}
