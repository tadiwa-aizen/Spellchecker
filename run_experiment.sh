#!/usr/bin/env bash
set -euo pipefail

# Root-relative paths
TOOLS_DIR="vcpkg_installed/x64-windows/tools/kenlm"
OUT_DIR="results"
REPORT="$OUT_DIR/EXPERIMENT_REPORT.md"

mkdir -p "$OUT_DIR"

TS=$(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date +%Y-%m-%d_%H-%M-%S)

echo "[INFO] Running character-level spell tests..."
python "$TOOLS_DIR/run_spell_tests.py" > "$OUT_DIR/char_results.txt" 2>&1 || true

echo "[INFO] Running isiZulu sentence perplexity check..."
python "$TOOLS_DIR/test_perplexity.py" > "$OUT_DIR/perplexity.txt" 2>&1 || true

echo "[INFO] Creating report..."
{
  echo "# Spellchecker Experiment Report"
  echo
  echo "Date: $TS"
  echo
  echo "## Commands"
  echo
  echo '```'
  echo "python $TOOLS_DIR/run_spell_tests.py"
  echo "python $TOOLS_DIR/test_perplexity.py"
  echo '```'
  echo
  echo "## Character-level Results"
  echo
  echo '```'
  cat "$OUT_DIR/char_results.txt" || true
  echo '```'
  echo
  echo "## Sentence Perplexity (isiZulu)"
  echo
  echo '```'
  cat "$OUT_DIR/perplexity.txt" || true
  echo '```'
} > "$REPORT"

echo "[INFO] Report written to: $REPORT"

