# Spellchecker Experiment Report

Date: 2025-10-16

## Objective

Evaluate a KenLM-based cSpellChecker prototype that detects misspellings by comparing language-model likelihoods. Two experiments were run:

- Character-level word discrimination across four languages (isiZulu, isiXhosa, isiNdebele, siSwati).
- Sentence-level sanity check (perplexity) for isiZulu.

## Setup

- Assets directory: `vcpkg_installed\x64-windows\tools\kenlm`
- Python: `3.12.6`
- Models (ARPA):
  - Word-level: `*Model.arpa`
  - Character-level: `*UModel.arpa` (expects words as space-separated characters)
- Test data: `*_test.txt` files, each line `wrong - correct`.

Pre-test adjustments:
- Fixed `test_perplexity.py` to use an existing model and removed a stray path line; added optional ARPA→binary conversion via `build_binary.exe -s`.
- Cleaned console output in helper scripts for readable ASCII.
- Added a consolidated runner: `run_spell_tests.py`.

## What’s Being Tested

1) Character-level cSpellChecker (primary).
   - Goal: flag a word as misspelled if a character-level LM assigns a significantly higher score to the correct spelling than to the wrong one.
   - Method: compute LM scores for both forms as character sequences and compare with a decision margin (default `1.5`).

2) Sentence-level Perplexity (secondary).
   - Goal: verify a word-level LM gives lower perplexity to a correct sentence than to a corrupted one.

## Commands Used

1) Run character-level tests for all languages:

```
python vcpkg_installed\x64-windows\tools\kenlm\run_spell_tests.py
```

What it does:
- Loads each `*UModel.arpa`.
- Parses `wrong - correct` pairs from each `*_test.txt`.
- Scores `"c h a r s"` with `kenlm.LanguageModel.score(..., bos=True, eos=True)`.
- Counts a correct detection if `(score(correct) - score(wrong)) > 1.5`.

2) Run isiZulu sentence-level perplexity check:

```
python vcpkg_installed\x64-windows\tools\kenlm\test_perplexity.py
```

What it does:
- Tries to build a binary from `isiZuluModel.arpa` using `build_binary.exe -s` (if present), then loads with `kenlm.Model`.
- Computes `model.perplexity(sentence)` for a correct and a corrupted sentence.

## Results

Character-level (word discrimination):

```
isiZulu: 20/20 = 100.00%
isiXhosa: 14/20 = 70.00%
isiNdebele: 12/20 = 60.00%
siSwati: 18/20 = 90.00%
Overall: 64/80 = 80.00%
```

Interpretation:
- The cSpellChecker concept is effective for isiZulu and siSwati with the current margin and data; moderate for isiXhosa and isiNdebele.
- Lower-performing languages likely need margin tuning, more/cleaner training text, or alignment of casing/punctuation with training.

Sentence-level perplexity (isiZulu):

```
Correct perplexity: 9738.58
Wrecked perplexity: 7609.36
Outcome: model preferred the wrecked sentence (WARN)
```

Interpretation:
- The word-level LM, as currently trained, did not favor the correct sentence. Potential causes: tokenization/casing mismatch, domain mismatch, or limited corpus size for reliable sentence modeling.

## What the Results Mean for cSpellChecker

- Primary goal (misspelling detection) shows promising accuracy overall (80%) and very strong performance for two languages.
- Focus next on per-language calibration (decision margin) and data quality to lift isiXhosa/isiNdebele.
- Sentence-level behavior needs refinement if it’s part of the product scope; it does not block character-level word detection.

## Optional Speed-ups and Next Steps

- Convert frequently used ARPAs to binaries for faster loads, e.g.:

```
vcpkg_installed\x64-windows\tools\kenlm\build_binary.exe -s \
  vcpkg_installed\x64-windows\tools\kenlm\isiZuluUModel.arpa \
  vcpkg_installed\x64-windows\tools\kenlm\isiZuluUModel.binary
```

- Re-run Zulu perplexity with `isiZuluCleanedModel.arpa` and normalized text (lowercase + period).
- Add per-language error analyses to guide margin tuning and corpus improvements.

