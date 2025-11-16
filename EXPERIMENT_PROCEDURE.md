# Spellchecker Experiment Procedure

**Purpose:** Test character-level language models for African language spellchecking  

---

## Purpose

This experiment series evaluates character-level language models for African language spellchecking and addresses critical questions about methodology and real-world applicability. The experiments build new models from larger corpora, generate realistic test data, test cross-language detection capabilities, and determine optimal thresholds for production spellcheckers. The goal is to move from artificial testing methods (comparing correct vs incorrect words side-by-side) to practical single-word detection that can be deployed in real applications.

Experiments 1-2 document which corpus files build which models and establish the complete training pipeline. Experiment 3 generates 1000+ test cases per language using a spelling wrecker tool with realistic error types (substitution, deletion, insertion, transposition, phonetic). Experiment 4 tests each language on its own model for baseline performance. Experiment 5 runs all test files against all models to create a cross-language confusion matrix. Experiment 6 scores correct words from corpora and incorrect words from test pairs to find score distributions and optimal thresholds. Experiment 7 tests single-word detection using absolute score thresholds (score < -10 = misspelled) instead of comparing correct vs incorrect pairs, achieving 78% detection with 3% false positives.

---

## Generate Character Corpora

The cleaned and raw models where sourced from the sadilar Autshumato Corpora


**What:** Convert word-level corpora in cleaned/corpra to character-level format for model training

**Command:**
```bash
python3 create_character_corpora.py
```

**Input:**
- `cleaned_corpora/isiZulu.txt`
- `cleaned_corpora/isiXhosa.txt`
- `cleaned_corpora/isiNdebele.txt`
- `cleaned_corpora/siSwati.txt`

**Output:**
- `character_corpora/isiZuluUCorpus.txt`
- `character_corpora/isiXhosaUCorpus.txt`
- `character_corpora/isiNdebeleUCorpus.txt`
- `character_corpora/siSwatiUCorpus.txt`

---

##Build Language Models

**What:** Train 5-gram character-level models using KenLM

**Commands:**
```cmd
mkdir models

vcpkg_installed\x64-windows\tools\kenlm\lmplz.exe -o 5 < character_corpora\isiZuluUCorpus.txt > models\isiZuluUModel.arpa

vcpkg_installed\x64-windows\tools\kenlm\lmplz.exe -o 5 --discount_fallback < character_corpora\isiXhosaUCorpus.txt > models\isiXhosaUModel.arpa

vcpkg_installed\x64-windows\tools\kenlm\lmplz.exe -o 5 --discount_fallback < character_corpora\isiNdebeleUCorpus.txt > models\isiNdebeleUModel.arpa

vcpkg_installed\x64-windows\tools\kenlm\lmplz.exe -o 5 --discount_fallback < character_corpora\siSwatiUCorpus.txt > models\siSwatiUModel.arpa
```

**Input:** Character corpora from Experiment 1  
**Output:** 4 ARPA model files in `models/`

---

## Generate Test Data

**What:** Create realistic spelling errors for testing

So for this we used a wreckign script, spelling_wrecker.py, 
The spelling wrecker generates typos using five error types. It reads correct words from the corpus (minimum 4 characters, no numbers), then randomly applies one error per word. Substitution replaces a character with a keyboard-adjacent key (e.g., 'a' → 's', 'q', 'w', or 'z' based on QWERTY layout). Deletion removes a random character from the word. Insertion adds either a keyboard-adjacent character or duplicates an existing character at a random position. Transposition swaps two adjacent characters. Phonetic replaces characters with phonetically similar ones common in African languages (b↔p, d↔t, g↔k, v↔f, z↔s, c↔k). The tool samples random words from the corpus, applies one random error type to each, and outputs either "wrong - correct" pairs or just the wrecked words. It tracks error type distribution and ensures actual errors were created (wrecked word differs from original).


**Command:**
```bash
python3 spelling_wrecker.py
```

**Input:** Cleaned corpora  
**Output:**
- `test_data/isizulu_with_errors` (100 wrecked words)
- `test_data/isiZulu_test_pairs.txt` (1000 test pairs)
- Same for isiXhosa, isiNdebele, siSwati

**Error Types Generated:**
- Substitution (23%)
- Deletion (22%)
- Insertion (22%)
- Transposition (22%)
- Phonetic (11%)

---

## Experiment 1: Baseline Testing



**What:** Test each language on its own model


The run_spell_tests.py script tests baseline spelling detection by comparing correct vs incorrect word pairs. It loads each language model and reads test files containing "wrong - correct" pairs (20 per language). For each pair, it scores both words using character-level sequences (word → "w o r d"). If the correct word scores more than 1.5 points higher than the wrong word (margin threshold), it counts as detected. The script calculates accuracy per language (correct detections / total pairs) and overall accuracy across all 80 test cases. This is the artificial testing method mentioned in Question 4 - it requires both the wrong and correct words to make a comparison, unlike real spellcheckers that only see one word at a time.

**Command:**
```bash
python3 vcpkg_installed/x64-windows/tools/kenlm/run_spell_tests.py
```

**Input:**
- Test files: `vcpkg_installed/x64-windows/tools/kenlm/*_test.txt` (20 pairs each)

**Output:** Accuracy per language (printed to console)

**Expected Results:**
- isiZulu: ~100%
- isiXhosa: ~70%
- isiNdebele: ~60%
- siSwati: ~80%

---

## Experiment 2: Cross-Model Testing


The cross_model_test.py script tests each language's test file against all 4 models to create a confusion matrix. It loads all 4 models (isiZulu, isiXhosa, isiNdebele, siSwati), then runs each language's 20 test pairs against every model using the same 1.5 margin threshold. This creates a 4×4 matrix showing cross-language detection: rows are test data languages, columns are models. The diagonal shows same-language performance (e.g., isiZulu test on isiZulu model = 100%). Off-diagonal cells show if one language's model can detect another language's errors (e.g., isiZulu test on isiXhosa model = 95%). 

**What:** Test each language against all 4 models (confusion matrix)

**Command:**
```bash
python3 cross_model_test.py
```

**Input:**
- All 4 models
- All 4 test files

**Output:** 4x4 confusion matrix showing cross-language detection

**Tests:**
- isiZulu test vs all models
- isiXhosa test vs all models
- isiNdebele test vs all models
- siSwati test vs all models

---

## Experiment 3: Threshold Analysis

The threshold_analysis.py script finds optimal thresholds by comparing score distributions of correct vs incorrect words. It samples 1000 correct words from each corpus and scores them with the model. It loads incorrect words from test pairs and scores both the wrong word and its correct version. For each pair, it calculates the score difference (correct - wrong). It then tests different thresholds (0.5 to 4.0) to see how many errors are detected when score_difference > threshold, calculating accuracy, precision, recall, and F1 score for each. The best threshold is the one with highest F1 score (typically 0.5). It also tests absolute score thresholds (-15 to -4) for single-word detection: if a word's score < threshold, flag it as misspelled. This shows false positive rate (correct words flagged) and true positive rate (incorrect words flagged). The -10 threshold gives good balance: ~78% detection with only ~3% false positives. 


**Command:**
```bash
python3 threshold_analysis.py > threshold_analysis_results.txt
```

**Input:**
- All 4 models
- 1000 correct words sampled from corpora
- 900+ incorrect words from test pairs

**Output:**
- Score distributions (correct vs incorrect)
- Threshold performance table
- Optimal threshold recommendation

**Analysis:**
- Test thresholds: 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0
- Test absolute thresholds: -15, -12, -10, -8, -6, -5, -4
- Calculate: accuracy, precision, recall, F1 score

---

## Experiment 4: Real Spellchecker Test

**What:** Test single-word detection using absolute threshold

**Command:**
```bash
# Already included in Experiment 6
python3 threshold_analysis.py
```

**Method:**
```python
# For each word in test set
score = model.score_character_sequence(word)

if score < -10.0:
    result = "misspelled"
else:
    result = "correct"
```

**Input:** Test pairs from Experiment 3  
**Threshold:** -10.0 (from Experiment 6)  
**Output:** Detection rate and false positive rate per language

**Note:** This test is automatically included in the threshold analysis

---

## Running All Experiment

**Full sequence:**
```bash
# 1. Generate character corpora
python3 create_character_corpora.py

# 2. Build models (on Windows)
# Run commands from Experiment 2

# 3. Generate test data
python3 spelling_wrecker.py

# 4. Baseline testing
python3 vcpkg_installed/x64-windows/tools/kenlm/run_spell_tests.py

# 5. Cross-model testing
python3 cross_model_test.py

# 6. Threshold analysis
python3 threshold_analysis.py > threshold_analysis_results.txt
```

---

## Expected Outputs

**Files Created:**
- `character_corpora/*.txt` (4 files)
- `models/*.arpa` (4 files)
- `test_data/*_with_errors` (4 files)
- `test_data/*_test_pairs.txt` (4 files)
- `threshold_analysis_results.txt`

**Results:**
- Baseline accuracy: 77.5% overall
- Cross-model matrix: 4x4 table
- Optimal threshold: -10.0
- Real spellchecker: 79% detection, 3% false positives

---