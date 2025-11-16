#!/usr/bin/env python3
"""
Spelling Wrecker Tool - Generates realistic typos for African languages
Creates test data by introducing common error types into correct words.
"""

import random
import re
from pathlib import Path


class SpellingWrecker:
    """Generate realistic spelling errors for testing."""
    
    def __init__(self, language="isiZulu"):
        self.language = language
        
        # Common keyboard-adjacent characters (QWERTY layout)
        self.adjacent_keys = {
            'a': 'sqwz', 'b': 'vghn', 'c': 'xdfv', 'd': 'serfcx', 'e': 'wrsd',
            'f': 'drtgvc', 'g': 'ftyhbv', 'h': 'gyujnb', 'i': 'ujko', 'j': 'huikmn',
            'k': 'jiolm', 'l': 'kop', 'm': 'njk', 'n': 'bhjm', 'o': 'iklp',
            'p': 'ol', 'q': 'wa', 'r': 'edft', 's': 'awedxz', 't': 'rfgy',
            'u': 'yhji', 'v': 'cfgb', 'w': 'qase', 'x': 'zsdc', 'y': 'tghu',
            'z': 'asx'
        }
        
        # Common character confusions in African languages
        self.phonetic_confusions = {
            'b': 'p', 'p': 'b',
            'd': 't', 't': 'd',
            'g': 'k', 'k': 'g',
            'v': 'f', 'f': 'v',
            'z': 's', 's': 'z',
            'c': 'k', 'k': 'c',
        }
    
    def substitute_char(self, word):
        """Substitute one character with an adjacent key."""
        if len(word) < 2:
            return word
        
        pos = random.randint(0, len(word) - 1)
        char = word[pos].lower()
        
        if char in self.adjacent_keys:
            replacement = random.choice(self.adjacent_keys[char])
            # Preserve case
            if word[pos].isupper():
                replacement = replacement.upper()
            return word[:pos] + replacement + word[pos+1:]
        return word
    
    def delete_char(self, word):
        """Delete a random character."""
        if len(word) <= 2:
            return word
        
        pos = random.randint(0, len(word) - 1)
        return word[:pos] + word[pos+1:]
    
    def insert_char(self, word):
        """Insert a random character."""
        pos = random.randint(0, len(word))
        char = word[pos-1] if pos > 0 else word[0]
        char = char.lower()
        
        # Insert adjacent key or duplicate
        if random.random() < 0.5 and char in self.adjacent_keys:
            insert_char = random.choice(self.adjacent_keys[char])
        else:
            insert_char = char  # Duplicate
        
        return word[:pos] + insert_char + word[pos:]
    
    def transpose_chars(self, word):
        """Swap two adjacent characters."""
        if len(word) < 2:
            return word
        
        pos = random.randint(0, len(word) - 2)
        return word[:pos] + word[pos+1] + word[pos] + word[pos+2:]
    
    def phonetic_error(self, word):
        """Replace with phonetically similar character."""
        if len(word) < 2:
            return word
        
        for i, char in enumerate(word.lower()):
            if char in self.phonetic_confusions and random.random() < 0.3:
                replacement = self.phonetic_confusions[char]
                if word[i].isupper():
                    replacement = replacement.upper()
                return word[:i] + replacement + word[i+1:]
        return word
    
    def wreck_word(self, word, error_types=None):
        """
        Apply a random error to a word.
        
        Args:
            word: The correct word
            error_types: List of error types to use, or None for all
        
        Returns:
            Tuple of (wrecked_word, error_type)
        """
        if error_types is None:
            error_types = ['substitute', 'delete', 'insert', 'transpose', 'phonetic']
        
        error_type = random.choice(error_types)
        
        if error_type == 'substitute':
            return self.substitute_char(word), 'substitution'
        elif error_type == 'delete':
            return self.delete_char(word), 'deletion'
        elif error_type == 'insert':
            return self.insert_char(word), 'insertion'
        elif error_type == 'transpose':
            return self.transpose_chars(word), 'transposition'
        elif error_type == 'phonetic':
            return self.phonetic_error(word), 'phonetic'
        
        return word, 'none'
    
    def wreck_corpus(self, corpus_file, output_file, num_errors=1000, min_word_length=4, format='pairs'):
        """
        Generate wrecked words from a corpus.
        
        Args:
            corpus_file: Path to corpus file
            output_file: Path to output file
            num_errors: Number of error pairs to generate
            min_word_length: Minimum word length to wreck
            format: 'pairs' for "wrong - correct" or 'errors_only' for just wrecked words
        """
        print(f"Reading corpus: {corpus_file}")
        
        # Read and extract unique words
        words = set()
        with open(corpus_file, 'r', encoding='utf-8') as f:
            for line in f:
                # Extract words, remove punctuation
                line_words = re.findall(r'\b\w+\b', line)
                for word in line_words:
                    if len(word) >= min_word_length and not any(c.isdigit() for c in word):
                        words.add(word)
        
        words = list(words)
        print(f"Found {len(words)} unique words (length >= {min_word_length})")
        
        if len(words) < num_errors:
            print(f"Warning: Only {len(words)} words available, generating that many errors")
            num_errors = len(words)
        
        # Generate errors
        print(f"Generating {num_errors} spelling errors...")
        error_pairs = []
        error_stats = {'substitution': 0, 'deletion': 0, 'insertion': 0, 'transposition': 0, 'phonetic': 0}
        
        sampled_words = random.sample(words, num_errors)
        
        for word in sampled_words:
            wrecked, error_type = self.wreck_word(word)
            
            # Make sure we actually created an error
            if wrecked != word:
                error_pairs.append((wrecked, word))
                error_stats[error_type] += 1
        
        # Write to file
        print(f"Writing {len(error_pairs)} errors to: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            if format == 'pairs':
                # Format: wrong - correct
                for wrong, correct in error_pairs:
                    f.write(f"{wrong} - {correct}\n")
            else:
                # Format: just wrecked words (one per line)
                for wrong, correct in error_pairs:
                    f.write(f"{wrong}\n")
        
        print("\nError type distribution:")
        for error_type, count in error_stats.items():
            percentage = (count / len(error_pairs) * 100) if error_pairs else 0
            print(f"  {error_type:15s}: {count:4d} ({percentage:5.1f}%)")
        
        print(f"\n✓ Complete! Generated {len(error_pairs)} test cases")
        return error_pairs


def main():
    """Generate wrecked test data for all languages."""
    
    wrecker = SpellingWrecker()
    
    # Define corpus files and output
    languages = [
        ('isiZulu', 'cleaned_corpora/isiZulu.txt', 'test_data/isizulu_with_errors', 'test_data/isiZulu_test_pairs.txt'),
        ('isiXhosa', 'cleaned_corpora/isiXhosa.txt', 'test_data/isiXhosa_with_errors', 'test_data/isiXhosa_test_pairs.txt'),
        ('isiNdebele', 'cleaned_corpora/isiNdebele.txt', 'test_data/isiNdebele_with_errors', 'test_data/isiNdebele_test_pairs.txt'),
        ('siSwati', 'cleaned_corpora/siSwati.txt', 'test_data/siSwati_with_errors', 'test_data/siSwati_test_pairs.txt'),
    ]
    
    # Create output directory
    Path('test_data').mkdir(exist_ok=True)
    
    print("=" * 80)
    print("Spelling Wrecker - Generating Test Data")
    print("=" * 80)
    print()
    
    for lang_name, corpus_file, errors_file, pairs_file in languages:
        print(f"\n{'=' * 80}")
        print(f"Processing {lang_name}")
        print('=' * 80)
        
        if not Path(corpus_file).exists():
            print(f"⚠ Warning: Corpus file not found: {corpus_file}")
            continue
        
        wrecker.language = lang_name
        
        # Generate errors-only file (like isizulu_with_errors)
        print(f"\nGenerating errors-only file...")
        wrecker.wreck_corpus(corpus_file, errors_file, num_errors=100, min_word_length=4, format='errors_only')
        
        # Generate test pairs file (for testing)
        print(f"\nGenerating test pairs file...")
        wrecker.wreck_corpus(corpus_file, pairs_file, num_errors=1000, min_word_length=4, format='pairs')
    
    print("\n" + "=" * 80)
    print("All test data generated successfully!")
    print("=" * 80)
    print("\nGenerated files:")
    for _, _, errors_file, pairs_file in languages:
        if Path(errors_file).exists():
            print(f"  {errors_file} (errors only, 100 words)")
        if Path(pairs_file).exists():
            print(f"  {pairs_file} (test pairs, 1000 pairs)")


if __name__ == '__main__':
    main()
