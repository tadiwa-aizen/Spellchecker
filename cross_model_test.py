#!/usr/bin/env python3
"""
Cross-model testing: Test each language's test file against all 4 models.
Creates a confusion matrix showing which models detect which language errors.
"""

import os
import kenlm


# Model and test file paths
TOOLS_DIR = "vcpkg_installed/x64-windows/tools/kenlm"

MODELS = {
    "isiZulu": "isiZuluUModel.arpa",
    "isiXhosa": "isiXhosaUModel.arpa",
    "isiNdebele": "isiNdebeleUModel.arpa",
    "siSwati": "siSwatiUModel.arpa",
}

TEST_FILES = {
    "isiZulu": "isiZulu_test.txt",
    "isiXhosa": "isiXhosa_test.txt",
    "isiNdebele": "isiNdebele_test.txt",
    "siSwati": "siSwati_test.txt",
}


def char_score(model: kenlm.LanguageModel, word: str) -> float:
    """Score a word using character-level model."""
    seq = " ".join(list(word.strip()))
    return model.score(seq, bos=True, eos=True)


def test_file_on_model(test_file_path: str, model: kenlm.LanguageModel, margin: float = 1.5):
    """Test a file against a model and return accuracy."""
    total = 0
    correct = 0
    
    with open(test_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or '-' not in line:
                continue
            
            parts = line.split('-', 1)
            if len(parts) != 2:
                continue
                
            wrong, correct_word = [w.strip() for w in parts]
            s_wrong = char_score(model, wrong)
            s_correct = char_score(model, correct_word)
            
            if (s_correct - s_wrong) > margin:
                correct += 1
            total += 1
    
    return correct, total


def main():
    print("=" * 80)
    print("Cross-Model Testing Matrix")
    print("=" * 80)
    print()
    
    # Load all models
    print("Loading models...")
    loaded_models = {}
    for lang_name, model_file in MODELS.items():
        model_path = os.path.join(TOOLS_DIR, model_file)
        if os.path.exists(model_path):
            print(f"  Loading {lang_name} model...")
            loaded_models[lang_name] = kenlm.LanguageModel(model_path)
        else:
            print(f"  [WARN] {lang_name} model not found: {model_path}")
    
    print()
    print("=" * 80)
    print("Testing each language test file against all models...")
    print("=" * 80)
    print()
    
    # Results matrix
    results = {}
    
    # Test each test file against each model
    for test_lang, test_file in TEST_FILES.items():
        test_path = os.path.join(TOOLS_DIR, test_file)
        
        if not os.path.exists(test_path):
            print(f"[WARN] Test file not found: {test_path}")
            continue
        
        results[test_lang] = {}
        
        print(f"Testing {test_lang} test data:")
        for model_lang, model in loaded_models.items():
            correct, total = test_file_on_model(test_path, model)
            accuracy = (correct / total * 100.0) if total > 0 else 0.0
            results[test_lang][model_lang] = (correct, total, accuracy)
            print(f"  vs {model_lang:12s} model: {correct:2d}/{total:2d} = {accuracy:6.2f}%")
        print()
    
    # Print matrix
    print("=" * 80)
    print("CONFUSION MATRIX")
    print("=" * 80)
    print()
    
    # Header
    print(f"{'Test Data':<15s}", end="")
    for model_lang in MODELS.keys():
        print(f"{model_lang:>12s}", end="")
    print()
    print("-" * 80)
    
    # Rows
    for test_lang in TEST_FILES.keys():
        if test_lang not in results:
            continue
        print(f"{test_lang:<15s}", end="")
        for model_lang in MODELS.keys():
            if model_lang in results[test_lang]:
                correct, total, accuracy = results[test_lang][model_lang]
                print(f"{accuracy:11.1f}%", end="")
            else:
                print(f"{'N/A':>12s}", end="")
        print()
    
    print()
    print("=" * 80)
    print("Analysis:")
    print("=" * 80)
    print()
    
    # Diagonal (same language) performance
    print("Same-language performance (diagonal):")
    for lang in TEST_FILES.keys():
        if lang in results and lang in results[lang]:
            correct, total, accuracy = results[lang][lang]
            print(f"  {lang}: {accuracy:.1f}%")
    
    print()
    print("Cross-language detection:")
    for test_lang in TEST_FILES.keys():
        if test_lang not in results:
            continue
        print(f"  {test_lang} errors detected by:")
        for model_lang in MODELS.keys():
            if model_lang != test_lang and model_lang in results[test_lang]:
                correct, total, accuracy = results[test_lang][model_lang]
                print(f"    {model_lang}: {accuracy:.1f}%")


if __name__ == "__main__":
    main()
