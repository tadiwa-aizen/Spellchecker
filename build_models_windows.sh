#!/bin/bash
# Build ARPA language models from character corpora using KenLM
# Run this on Windows with Git Bash or WSL

set -e

echo "=========================================="
echo "Building KenLM ARPA Language Models"
echo "=========================================="
echo

# Paths
LMPLZ="vcpkg_installed/x64-windows/tools/kenlm/lmplz.exe"
INPUT_DIR="character_corpora"
OUTPUT_DIR="models"
ORDER=5

# Check if lmplz exists
if [ ! -f "$LMPLZ" ]; then
    echo "[ERROR] lmplz.exe not found at: $LMPLZ"
    echo "Please ensure you're in the Spellchecker directory"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Build isiZulu model
echo "Building isiZulu model..."
echo "  Input:  $INPUT_DIR/isiZuluUCorpus.txt"
echo "  Output: $OUTPUT_DIR/isiZuluUModel.arpa"
echo "  Order:  ${ORDER}-gram"
"$LMPLZ" -o $ORDER < "$INPUT_DIR/isiZuluUCorpus.txt" > "$OUTPUT_DIR/isiZuluUModel.arpa" 2>&1
if [ -f "$OUTPUT_DIR/isiZuluUModel.arpa" ]; then
    SIZE=$(du -h "$OUTPUT_DIR/isiZuluUModel.arpa" | cut -f1)
    echo "  [OK] Model built! Size: $SIZE"
else
    echo "  [ERROR] Failed to build model"
fi
echo

# Build isiXhosa model
echo "Building isiXhosa model..."
echo "  Input:  $INPUT_DIR/isiXhosaUCorpus.txt"
echo "  Output: $OUTPUT_DIR/isiXhosaUModel.arpa"
echo "  Order:  ${ORDER}-gram"
"$LMPLZ" -o $ORDER < "$INPUT_DIR/isiXhosaUCorpus.txt" > "$OUTPUT_DIR/isiXhosaUModel.arpa" 2>&1
if [ -f "$OUTPUT_DIR/isiXhosaUModel.arpa" ]; then
    SIZE=$(du -h "$OUTPUT_DIR/isiXhosaUModel.arpa" | cut -f1)
    echo "  [OK] Model built! Size: $SIZE"
else
    echo "  [ERROR] Failed to build model"
fi
echo

# Build isiNdebele model
echo "Building isiNdebele model..."
echo "  Input:  $INPUT_DIR/isiNdebeleUCorpus.txt"
echo "  Output: $OUTPUT_DIR/isiNdebeleUModel.arpa"
echo "  Order:  ${ORDER}-gram"
"$LMPLZ" -o $ORDER < "$INPUT_DIR/isiNdebeleUCorpus.txt" > "$OUTPUT_DIR/isiNdebeleUModel.arpa" 2>&1
if [ -f "$OUTPUT_DIR/isiNdebeleUModel.arpa" ]; then
    SIZE=$(du -h "$OUTPUT_DIR/isiNdebeleUModel.arpa" | cut -f1)
    echo "  [OK] Model built! Size: $SIZE"
else
    echo "  [ERROR] Failed to build model"
fi
echo

# Build siSwati model
echo "Building siSwati model..."
echo "  Input:  $INPUT_DIR/siSwatiUCorpus.txt"
echo "  Output: $OUTPUT_DIR/siSwatiUModel.arpa"
echo "  Order:  ${ORDER}-gram"
"$LMPLZ" -o $ORDER < "$INPUT_DIR/siSwatiUCorpus.txt" > "$OUTPUT_DIR/siSwatiUModel.arpa" 2>&1
if [ -f "$OUTPUT_DIR/siSwatiUModel.arpa" ]; then
    SIZE=$(du -h "$OUTPUT_DIR/siSwatiUModel.arpa" | cut -f1)
    echo "  [OK] Model built! Size: $SIZE"
else
    echo "  [ERROR] Failed to build model"
fi
echo

echo "=========================================="
echo "Complete! Models saved to: $OUTPUT_DIR/"
echo "=========================================="
echo
ls -lh "$OUTPUT_DIR"/*.arpa 2>/dev/null || echo "No models found"
