#!/usr/bin/env python3
"""
Threshold Analysis - Find optimal detection thresholds for real spellchecking.
Analyzes score distributions of correct vs incorrect words.
"""

import os
import kenlm
import random
import numpy as np
from pathlib import Path


def char_score(model: kenlm.LanguageModel, word: str) -> float:
    """Score a word using character-level model."""
    seq = " ".join(list(word.strip()))
    return model.score(seq, bos=True, eos=True)


def analyze_threshold(language, model_path, corpus_path, test_pairs_path, num_correct_samples=1000):
    """
    Analyze score distributions to find optimal threshold.
    
    Args:
        language: Language name
        model_path: Path to ARPA model
        corpus_path: Path to corpus (for correct words)
        test_pairs_path: Path to test pairs file
        num_correct_samples: Number of correct words to sample
    """
    print(f"\n{'=' * 80}")
    print(f"Threshold Analysis: {language}")
    print('=' * 80)
    
    # Load model
    print(f"Loading model: {model_path}")
    model = kenlm.LanguageModel(model_path)
    
    # Sample correct words from corpus
    print(f"\nSampling {num_correct_samples} correct words from corpus...")
    correct_words = set()
    with open(corpus_path, 'r', encoding='utf-8') as f:
        for line in f:
            words = line.strip().split()
            for word in words:
                # Clean word
                word = ''.join(c for c in word if c.isalpha())
                if len(word) >= 4 and not any(c.isdigit() for c in word):
                    correct_words.add(word)
                if len(correct_words) >= num_correct_samples * 2:
                    break
            if len(correct_words) >= num_correct_samples * 2:
                break
    
    correct_words = random.sample(list(correct_words), min(num_correct_samples, len(correct_words)))
    
    # Score correct words
    print(f"Scoring {len(correct_words)} correct words...")
    correct_scores = []
    for word in correct_words:
        score = char_score(model, word)
        correct_scores.append(score)
    
    # Load and score incorrect words
    print(f"\nLoading incorrect words from: {test_pairs_path}")
    incorrect_words = []
    correct_versions = []
    
    with open(test_pairs_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if '-' in line:
                parts = line.split('-', 1)
                if len(parts) == 2:
                    wrong = parts[0].strip()
                    correct = parts[1].strip()
                    incorrect_words.append(wrong)
                    correct_versions.append(correct)
    
    print(f"Scoring {len(incorrect_words)} incorrect words...")
    incorrect_scores = []
    correct_version_scores = []
    score_differences = []
    
    for wrong, correct in zip(incorrect_words, correct_versions):
        wrong_score = char_score(model, wrong)
        correct_score = char_score(model, correct)
        
        incorrect_scores.append(wrong_score)
        correct_version_scores.append(correct_score)
        score_differences.append(correct_score - wrong_score)
    
    # Calculate statistics
    print(f"\n{'=' * 80}")
    print("Score Distribution Statistics")
    print('=' * 80)
    
    print(f"\nCorrect Words (n={len(correct_scores)}):")
    print(f"  Mean:   {np.mean(correct_scores):8.3f}")
    print(f"  Median: {np.median(correct_scores):8.3f}")
    print(f"  Std:    {np.std(correct_scores):8.3f}")
    print(f"  Min:    {np.min(correct_scores):8.3f}")
    print(f"  Max:    {np.max(correct_scores):8.3f}")
    print(f"  25%:    {np.percentile(correct_scores, 25):8.3f}")
    print(f"  75%:    {np.percentile(correct_scores, 75):8.3f}")
    
    print(f"\nIncorrect Words (n={len(incorrect_scores)}):")
    print(f"  Mean:   {np.mean(incorrect_scores):8.3f}")
    print(f"  Median: {np.median(incorrect_scores):8.3f}")
    print(f"  Std:    {np.std(incorrect_scores):8.3f}")
    print(f"  Min:    {np.min(incorrect_scores):8.3f}")
    print(f"  Max:    {np.max(incorrect_scores):8.3f}")
    print(f"  25%:    {np.percentile(incorrect_scores, 25):8.3f}")
    print(f"  75%:    {np.percentile(incorrect_scores, 75):8.3f}")
    
    print(f"\nScore Differences (correct - incorrect):")
    print(f"  Mean:   {np.mean(score_differences):8.3f}")
    print(f"  Median: {np.median(score_differences):8.3f}")
    print(f"  Std:    {np.std(score_differences):8.3f}")
    print(f"  Min:    {np.min(score_differences):8.3f}")
    print(f"  Max:    {np.max(score_differences):8.3f}")
    print(f"  25%:    {np.percentile(score_differences, 25):8.3f}")
    print(f"  75%:    {np.percentile(score_differences, 75):8.3f}")
    
    # Find optimal threshold
    print(f"\n{'=' * 80}")
    print("Threshold Analysis")
    print('=' * 80)
    
    # Test different thresholds
    thresholds = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
    
    print(f"\nTesting thresholds (score_difference > threshold = misspelling detected):")
    print(f"{'Threshold':>10s} {'Detected':>10s} {'Accuracy':>10s} {'Precision':>10s} {'Recall':>10s} {'F1':>10s}")
    print('-' * 80)
    
    best_f1 = 0
    best_threshold = 1.5
    
    for threshold in thresholds:
        # Count detections
        detected = sum(1 for diff in score_differences if diff > threshold)
        accuracy = detected / len(score_differences) * 100
        
        # Calculate precision and recall
        true_positives = detected
        false_positives = 0  # We don't have false positives in this test (all are actual errors)
        false_negatives = len(score_differences) - detected
        
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        print(f"{threshold:10.1f} {detected:10d} {accuracy:9.1f}% {precision:9.1f}% {recall:9.1f}% {f1:9.3f}")
        
        if f1 > best_f1:
            best_f1 = f1
            best_threshold = threshold
    
    print(f"\nBest threshold: {best_threshold} (F1={best_f1:.3f})")
    
    # Absolute score threshold analysis
    print(f"\n{'=' * 80}")
    print("Absolute Score Threshold Analysis")
    print('=' * 80)
    print("\nTesting absolute score thresholds (score < threshold = misspelling):")
    
    abs_thresholds = [-15, -12, -10, -8, -6, -5, -4]
    
    print(f"{'Threshold':>10s} {'Correct':>12s} {'Incorrect':>12s} {'FP Rate':>10s} {'TP Rate':>10s}")
    print('-' * 80)
    
    for threshold in abs_thresholds:
        correct_flagged = sum(1 for score in correct_scores if score < threshold)
        incorrect_flagged = sum(1 for score in incorrect_scores if score < threshold)
        
        fp_rate = correct_flagged / len(correct_scores) * 100
        tp_rate = incorrect_flagged / len(incorrect_scores) * 100
        
        print(f"{threshold:10.1f} {correct_flagged:12d} {incorrect_flagged:12d} {fp_rate:9.1f}% {tp_rate:9.1f}%")
    
    # Return results
    return {
        'language': language,
        'correct_scores': correct_scores,
        'incorrect_scores': incorrect_scores,
        'score_differences': score_differences,
        'best_threshold': best_threshold,
        'best_f1': best_f1,
        'stats': {
            'correct_mean': np.mean(correct_scores),
            'incorrect_mean': np.mean(incorrect_scores),
            'diff_mean': np.mean(score_differences),
            'diff_median': np.median(score_differences)
        }
    }


def main():
    """Run threshold analysis for all languages."""
    
    languages = [
        ('isiZulu', 'models/isiZuluUModel.arpa', 'cleaned_corpora/isiZulu.txt', 'test_data/isiZulu_test_pairs.txt'),
        ('isiXhosa', 'models/isiXhosaUModel.arpa', 'cleaned_corpora/isiXhosa.txt', 'test_data/isiXhosa_test_pairs.txt'),
        ('isiNdebele', 'models/isiNdebeleUModel.arpa', 'cleaned_corpora/isiNdebele.txt', 'test_data/isiNdebele_test_pairs.txt'),
        ('siSwati', 'models/siSwatiUModel.arpa', 'cleaned_corpora/siSwati.txt', 'test_data/siSwati_test_pairs.txt'),
    ]
    
    print("=" * 80)
    print("Threshold Analysis for Real Spellchecking")
    print("=" * 80)
    
    results = []
    
    for lang_name, model_path, corpus_path, test_path in languages:
        if not Path(model_path).exists():
            print(f"\n⚠ Warning: Model not found: {model_path}")
            continue
        if not Path(test_path).exists():
            print(f"\n⚠ Warning: Test file not found: {test_path}")
            continue
        
        result = analyze_threshold(lang_name, model_path, corpus_path, test_path, num_correct_samples=1000)
        results.append(result)
    
    # Summary
    print(f"\n{'=' * 80}")
    print("Summary: Recommended Thresholds")
    print('=' * 80)
    print(f"\n{'Language':15s} {'Best Threshold':>15s} {'F1 Score':>10s} {'Mean Diff':>12s}")
    print('-' * 80)
    
    for result in results:
        print(f"{result['language']:15s} {result['best_threshold']:15.1f} {result['best_f1']:10.3f} {result['stats']['diff_mean']:12.3f}")
    
    print(f"\n{'=' * 80}")
    print("Conclusion")
    print('=' * 80)
    print("\nFor real-world spellchecking:")
    print("- Use score difference method: score(correct) - score(wrong) > threshold")
    print("- Recommended threshold range: 1.5 - 2.5")
    print("- Language-specific thresholds may improve accuracy")
    print("- Consider using absolute score thresholds for single-word detection")


if __name__ == '__main__':
    main()
