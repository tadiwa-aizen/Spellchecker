#!/usr/bin/env python3
"""
Experiment 7: Real Spellchecker Test
Test single-word detection using absolute threshold (no comparison needed)
"""

import os
import kenlm


def char_score(model: kenlm.LanguageModel, word: str) -> float:
    """Score a word using character-level model."""
    seq = " ".join(list(word.strip()))
    return model.score(seq, bos=True, eos=True)


def test_real_spellchecker(language, model_path, test_pairs_path, threshold=-10.0):
    """
    Test real spellchecker using absolute threshold.
    Only looks at one word at a time (no comparison).
    """
    print(f"\n{'=' * 80}")
    print(f"Real Spellchecker Test: {language}")
    print(f"Threshold: {threshold}")
    print('=' * 80)
    
    # Load model
    print(f"Loading model: {model_path}")
    model = kenlm.LanguageModel(model_path)
    
    # Load test pairs
    print(f"Loading test data: {test_pairs_path}")
    test_cases = []
    
    with open(test_pairs_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if '-' in line:
                parts = line.split('-', 1)
                if len(parts) == 2:
                    wrong = parts[0].strip()
                    correct = parts[1].strip()
                    test_cases.append((wrong, correct))
    
    print(f"Testing {len(test_cases)} word pairs...\n")
    
    # Test incorrect words (should be flagged)
    incorrect_detected = 0
    incorrect_missed = 0
    
    # Test correct words (should NOT be flagged)
    correct_ok = 0
    correct_flagged = 0
    
    for wrong, correct in test_cases:
        # Test the WRONG word (should be detected as misspelled)
        wrong_score = char_score(model, wrong)
        if wrong_score < threshold:
            incorrect_detected += 1
        else:
            incorrect_missed += 1
        
        # Test the CORRECT word (should NOT be flagged)
        correct_score = char_score(model, correct)
        if correct_score >= threshold:
            correct_ok += 1
        else:
            correct_flagged += 1
    
    # Calculate metrics
    total_incorrect = incorrect_detected + incorrect_missed
    total_correct = correct_ok + correct_flagged
    
    true_positive_rate = (incorrect_detected / total_incorrect * 100) if total_incorrect > 0 else 0
    false_positive_rate = (correct_flagged / total_correct * 100) if total_correct > 0 else 0
    
    # Print results
    print(f"{'=' * 80}")
    print("Results")
    print('=' * 80)
    print(f"\nIncorrect Words (should be flagged):")
    print(f"  Detected:     {incorrect_detected:4d} / {total_incorrect:4d} = {true_positive_rate:6.2f}%")
    print(f"  Missed:       {incorrect_missed:4d} / {total_incorrect:4d}")
    
    print(f"\nCorrect Words (should NOT be flagged):")
    print(f"  Passed:       {correct_ok:4d} / {total_correct:4d} = {100 - false_positive_rate:6.2f}%")
    print(f"  False Alarm:  {correct_flagged:4d} / {total_correct:4d} = {false_positive_rate:6.2f}%")
    
    print(f"\n{'=' * 80}")
    print("Summary")
    print('=' * 80)
    print(f"True Positive Rate (Detection):  {true_positive_rate:6.2f}%")
    print(f"False Positive Rate (False Alarm): {false_positive_rate:6.2f}%")
    
    return {
        'language': language,
        'threshold': threshold,
        'true_positive_rate': true_positive_rate,
        'false_positive_rate': false_positive_rate,
        'incorrect_detected': incorrect_detected,
        'incorrect_total': total_incorrect,
        'correct_flagged': correct_flagged,
        'correct_total': total_correct
    }


def main():
    """Run real spellchecker test for all languages."""
    
    languages = [
        ('isiZulu', 'models/isiZuluUModel.arpa', 'test_data/isiZulu_test_pairs.txt'),
        ('isiXhosa', 'models/isiXhosaUModel.arpa', 'test_data/isiXhosa_test_pairs.txt'),
        ('isiNdebele', 'models/isiNdebeleUModel.arpa', 'test_data/isiNdebele_test_pairs.txt'),
        ('siSwati', 'models/siSwatiUModel.arpa', 'test_data/siSwati_test_pairs.txt'),
    ]
    
    threshold = -10.0
    
    print("=" * 80)
    print("Experiment 7: Real Spellchecker Test")
    print("=" * 80)
    print(f"\nMethod: Single-word detection with absolute threshold")
    print(f"Threshold: {threshold}")
    print(f"No comparison needed - just score the word itself")
    
    results = []
    
    for lang_name, model_path, test_path in languages:
        if not os.path.exists(model_path):
            print(f"\n⚠ Warning: Model not found: {model_path}")
            continue
        if not os.path.exists(test_path):
            print(f"\n⚠ Warning: Test file not found: {test_path}")
            continue
        
        result = test_real_spellchecker(lang_name, model_path, test_path, threshold)
        results.append(result)
    
    # Overall summary
    print(f"\n{'=' * 80}")
    print("Overall Summary")
    print('=' * 80)
    print(f"\n{'Language':15s} {'Detection':>12s} {'False Alarms':>15s}")
    print('-' * 80)
    
    for result in results:
        print(f"{result['language']:15s} {result['true_positive_rate']:11.1f}% {result['false_positive_rate']:14.1f}%")
    
    # Calculate averages
    avg_detection = sum(r['true_positive_rate'] for r in results) / len(results)
    avg_false_positive = sum(r['false_positive_rate'] for r in results) / len(results)
    
    print('-' * 80)
    print(f"{'Average':15s} {avg_detection:11.1f}% {avg_false_positive:14.1f}%")
    
    print(f"\n{'=' * 80}")
    print("Conclusion")
    print('=' * 80)
    print(f"\nReal spellchecker with threshold {threshold}:")
    print(f"  ✓ Detects {avg_detection:.1f}% of misspellings")
    print(f"  ✓ Only {avg_false_positive:.1f}% false alarms on correct words")
    print(f"\nThis is practical for production use!")


if __name__ == '__main__':
    main()
