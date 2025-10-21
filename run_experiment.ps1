Param(
  [string]$ToolsDir = "vcpkg_installed\x64-windows\tools\kenlm",
  [string]$OutDir   = "results"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Continue'

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$report = Join-Path $OutDir 'EXPERIMENT_REPORT.md'
$charOut = Join-Path $OutDir 'char_results.txt'
$pplOut  = Join-Path $OutDir 'perplexity.txt'

function Run-Cmd {
  param([string]$Cmd, [string[]]$ArgList, [string]$OutFile)
  Write-Host "[INFO] $Cmd $($ArgList -join ' ')"
  try {
    & $Cmd @ArgList 1> $OutFile 2>&1
  } catch {
    "[WARN] Command failed: $Cmd $($ArgList -join ' ')`n$($_.Exception.Message)" | Out-File -FilePath $OutFile -Encoding utf8
  }
}

$ts = (Get-Date).ToString('u')

# 1) Character-level tests
Run-Cmd -Cmd 'python' -ArgList @("$ToolsDir/run_spell_tests.py") -OutFile $charOut

# 2) Sentence perplexity check
Run-Cmd -Cmd 'python' -ArgList @("$ToolsDir/test_perplexity.py") -OutFile $pplOut

# 3) Build report
$lines = @()
$lines += "# Spellchecker Experiment Report"
$lines += ""
$lines += "Date: $ts"
$lines += ""
$lines += "## Commands"
$lines += ""
$lines += '```'
$lines += "python $ToolsDir/run_spell_tests.py"
$lines += "python $ToolsDir/test_perplexity.py"
$lines += '```'
$lines += ""
$lines += "## Character-level Results"
$lines += ""
$lines += '```'
if (Test-Path $charOut) { $lines += Get-Content -Raw -Encoding UTF8 $charOut } else { $lines += '[no output]' }
$lines += '```'
$lines += ""
$lines += "## Sentence Perplexity (isiZulu)"
$lines += ""
$lines += '```'
if (Test-Path $pplOut) { $lines += Get-Content -Raw -Encoding UTF8 $pplOut } else { $lines += '[no output]' }
$lines += '```'

$lines | Out-File -FilePath $report -Encoding utf8 -Force
Write-Host "[INFO] Report written to: $report"
