#!/usr/bin/env python3
"""
Create character-level corpora from cleaned word-level corpora.
Converts each unique word into space-separated characters for KenLM training.

This script replicates the logic from vcpkg_installed/x64-windows/tools/kenlm/process.py
"""

import re
from pathlib import Path


def create_character_corpus(input_file, output_file):
    """
    Process a cleaned corpus file and create a character-level version.
    Uses the same logic as the original process.py script.
    
    Args:
        input_file: Path to cleaned corpus (word-level)
        output_file: Path to output character corpus
    """
    print(f"Processing: {input_file}")
    
    unique_words = set()
    
    # Extract unique words from the corpus (same logic as original process.py)
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if line_num % 10000 == 0:
                print(f"  Processed {line_num} lines, found {len(unique_words)} unique words...")
            
            words = line.strip().split()
            for word in words:
                # Clean punctuation (same as original)
                cleaned_word = re.sub(r'[^\w\s]', '', word)
                
                # Skip words with numbers (same as original)
                if any(char.isdigit() for char in cleaned_word):
                    continue
                
                # Add to unique set if not empty and not already present
                if cleaned_word and cleaned_word not in unique_words:
                    unique_words.add(cleaned_word)
    
    print(f"  Found {len(unique_words)} unique words total")
    print(f"  Writing character corpus to: {output_file}")
    
    # Write character-separated words (same as original)
    with open(output_file, 'w', encoding='utf-8') as f:
        for word in sorted(unique_words):
            # Convert word to space-separated characters
            spaced_word = ' '.join(list(word))
            f.write(spaced_word + '\n')
    
    print(f"  ✓ Complete: {output_file}\n")


def main():
    """Process all language corpora."""
    
    # Define input/output directories
    input_dir = Path('cleaned_corpora')
    output_dir = Path('character_corpora')
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Define language files
    languages = [
        ('isiZulu.txt', 'isiZuluUCorpus.txt'),
        ('isiXhosa.txt', 'isiXhosaUCorpus.txt'),
        ('isiNdebele.txt', 'isiNdebeleUCorpus.txt'),
        ('siSwati.txt', 'siSwatiUCorpus.txt'),
    ]
    
    print("=" * 60)
    print("Creating Character-Level Corpora")
    print("=" * 60)
    print()
    
    for input_name, output_name in languages:
        input_path = input_dir / input_name
        output_path = output_dir / output_name
        
        if not input_path.exists():
            print(f"⚠ Warning: {input_path} not found, skipping...")
            continue
        
        create_character_corpus(input_path, output_path)
    
    print("=" * 60)
    print("All character corpora created successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Use lmplz to build language models from character corpora")
    print("2. Example: lmplz -o 3 < character_corpora/isiZuluUCorpus.txt > isiZuluUModel.arpa")


if __name__ == '__main__':
    main()
