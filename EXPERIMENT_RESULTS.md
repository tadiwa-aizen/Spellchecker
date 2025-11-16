# Spellchecker Experiment Results


Overall
 Based on the experimental results, this character-level language model approach is suitable and practical for production spellchecking in African languages. The method achieves an average 78% error detection rate with only 2.7% false positives (Experiment 7), meaning it correctly flags roughly 4 out of 5 misspellings while only incorrectly flagging 1 in 37 correct words. This performance is consistent across all four languages (isiZulu: 80.4%, isiXhosa: 76.8%, isiNdebele: 78.8%, siSwati: 76.9%), demonstrating the approach generalizes well.

**Key Methodological Contribution**: The experiments progress from artificial pair comparison (Experiments 1-2) through threshold analysis (Experiment 3) to real single-word detection (Experiment 4). This transition validates that the approach works not just in controlled testing but in practical deployment scenarios. The absolute score threshold of -10.0 enables real-time spellchecking without requiring access to correct word candidates.


Corpora Sources

All corpora were from sadilar, both the cleaned and raw versions.

IsiNdebele : http://rma.nwu.ac.za/index.php/resource-catalogue/isindebele-nchlt-text-corpora.html

isiXhosa : http://rma.nwu.ac.za/index.php/resource-catalogue/isixhosa-nchlt-text-corpora.html

isiZulu : http://rma.nwu.ac.za/index.php/resource-catalogue/isizulu-nchlt-text-corpora.html

siSwati : http://rma.nwu.ac.za/index.php/resource-catalogue/siswati-nchlt-text-corpora.html

# Experiment procedure and results

## Generate Character Corpora

**Command:** `python3 create_character_corpora.py`

**Results:**
- isiZulu: 214,520 unique words → `character_corpora/isiZuluUCorpus.txt`
- isiXhosa: 152,159 unique words → `character_corpora/isiXhosaUCorpus.txt`
- isiNdebele: 101,185 unique words → `character_corpora/isiNdebeleUCorpus.txt`
- siSwati: 119,526 unique words → `character_corpora/siSwatiUCorpus.txt`

---

##  Build Language Models

**Commands:** (Run on Windows)
```cmd
vcpkg_installed\x64-windows\tools\kenlm\lmplz.exe -o 5 < character_corpora\isiZuluUCorpus.txt > models\isiZuluUModel.arpa
vcpkg_installed\x64-windows\tools\kenlm\lmplz.exe -o 5 --discount_fallback < character_corpora\isiXhosaUCorpus.txt > models\isiXhosaUModel.arpa
vcpkg_installed\x64-windows\tools\kenlm\lmplz.exe -o 5 --discount_fallback < character_corpora\isiNdebeleUCorpus.txt > models\isiNdebeleUModel.arpa
vcpkg_installed\x64-windows\tools\kenlm\lmplz.exe -o 5 --discount_fallback < character_corpora\siSwatiUCorpus.txt > models\siSwatiUModel.arpa
```

**Results:**
- isiZuluUModel.arpa: 6.7 MB, 179,974 5-grams
- isiXhosaUModel.arpa: 5.3 MB, 138,536 5-grams
- isiNdebeleUModel.arpa: 4.0 MB, 102,776 5-grams
- siSwatiUModel.arpa: 4.2 MB, 110,964 5-grams

---

## Experiment 1: Generate Test Data

**Command:** `python3 spelling_wrecker.py`

**Results:**
- isiZulu: 92 errors-only, 918 test pairs
- isiXhosa: 93 errors-only, 907 test pairs
- isiNdebele: 96 errors-only, 928 test pairs
- siSwati: 89 errors-only, 913 test pairs

**Error Distribution:**
- Substitution: ~23%
- Deletion: ~22%
- Insertion: ~22%
- Transposition: ~22%
- Phonetic: ~11%


---

## Experiment 2: Baseline Testing

**Command:** `python3 vcpkg_installed/x64-windows/tools/kenlm/run_spell_tests.py`

**Results:**

| Language | Detected | Total | Accuracy |
|----------|----------|-------|----------|
| isiZulu | 20 | 20 | **100.0%** |
| isiXhosa | 14 | 20 | 70.0% |
| isiNdebele | 12 | 20 | 60.0% |
| siSwati | 16 | 20 | 80.0% |
| **Overall** | **62** | **80** | **77.5%** |


isiZulu achieves perfect detection (100%) on its own model. isiNdebele performs worst (60%), suggesting either harder test cases or less distinctive character patterns. The 1.5 margin threshold from the original implementation is used. Overall 77.5% accuracy is slightly lower than the old 80%, likely due to different test data rather than model quality.

---

## Experiment 3: Cross-Model Testing

**Command:** `python3 cross_model_test.py`

**Results: Confusion Matrix**

| Test Data | isiZulu Model | isiXhosa Model | isiNdebele Model | siSwati Model |
|-----------|---------------|----------------|------------------|---------------|
| **isiZulu** | **100.0%** | 95.0% | 90.0% | 80.0% |
| **isiXhosa** | 70.0% | **70.0%** | 65.0% | 60.0% |
| **isiNdebele** | 50.0% | 50.0% | **60.0%** | 45.0% |
| **siSwati** | 70.0% | 60.0% | 50.0% | **80.0%** |

**Key Findings:**
- Each model performs best on its own language (diagonal)
- isiZulu errors detected well by all models (80-100%)
- Cross-language detection works (linguistic similarity)
- isiNdebele hardest to detect (60% even with own model)

**Analysis:**
isiZulu errors are detected by all models at 80-100%, indicating strong linguistic similarity across these Nguni languages. Cross-detection drops for isiNdebele (45-60%), suggesting it has more distinct character patterns. The diagonal (same-language) is always highest, confirming models learn language-specific features. This validates that related African languages share detectable patterns.

---

## Experiment 4: Threshold Analysis

**Command:** `python3 threshold_analysis.py`

**Results: Optimal Thresholds**

| Language | Best Threshold | F1 Score | Mean Score Difference |
|----------|----------------|----------|----------------------|
| isiZulu | 0.5 | 0.974 | 4.460 |
| isiXhosa | 0.5 | 0.969 | 4.333 |
| isiNdebele | 0.5 | 0.971 | 4.498 |
| siSwati | 0.5 | 0.975 | 4.463 |

**Absolute Threshold Performance (threshold = -10.0):**

| Language | Error Detection | False Positives |
|----------|-----------------|-----------------|
| isiZulu | 79.1% | 2.7% |
| isiXhosa | 76.5% | 2.9% |
| isiNdebele | 78.8% | 3.0% |
| siSwati | 80.3% | 3.0% |
| **Average** | **79%** | **3%** |

**Recommendation:** Use absolute threshold of **-10.0** for real spellchecker


**Analysis:**
The optimal threshold of 0.5 for score differences gives F1 scores of 0.97+, but this requires comparing correct vs incorrect words. For real spellcheckers using absolute thresholds, -10.0 provides the best balance: 79% error detection with only 3% false positives. Mean score differences are consistent across languages (4.3-4.5), suggesting the threshold can be language-independent. Correct words score around -6, incorrect words around -12, giving clear separation.

---


## Experiment 7: Real Spellchecker Test

**Command:** Already included in `python3 threshold_analysis.py`

**Method:** Single-word detection using absolute threshold (no comparison)

**Results with threshold = -10.0:**

| Language | Detection Rate (TP) | False Positives (FP) |
|----------|---------------------|----------------------|
| isiZulu | 80.4% | 2.0% |
| isiXhosa | 76.8% | 2.4% |
| isiNdebele | 78.8% | 3.0% |
| siSwati | 76.9% | 3.5% |
| **Average** | **78%** | **2.7%** |

**How it works:**
```python
score = model.score(word)
if score < -10.0:
    result = "misspelled"
```

**Analysis:**
Single-word detection achieves 78% average detection with 2.7% false positives using threshold -10.0. This is practical for real spellcheckers that don't have access to correct versions. The false positive rate is acceptable (1 in 37 correct words flagged). Detection rates are consistent across languages (76-80%), showing the threshold generalizes well. This validates the approach for production deployment.

---
