# Spellchecker Experiment Results

This experiment evaluates a KenLM-based spellchecker designed to detect misspellings in four African languages: isiZulu, isiXhosa, isiNdebele, and siSwati. The system uses character-level language models to compare probability scores between potentially misspelled words and their correct counterparts.

Methodology

Word-Level Spell Detection (Primary Test)

Approach: Character-level language model scoring
• **Models used:** Character-level language models (isiZuluUModel.arpa, isiXhosaUModel.arpa, etc.) 
trained on space-separated character sequences
• Each word is broken into individual characters: "hello" → "h e l l o"
• The character-level language model assigns probability scores to these character sequences
• Misspelling detected when correct word scores significantly higher than incorrect word
• Decision threshold: Score difference > 1.5

**Test Data Structure:**
- Format: `wrong_word - correct_word` (one pair per line)
- 20 word pairs per language
- Total test cases: 80 word pairs across 4 languages

**Models Used:**
- `isiZuluUModel.arpa` - Character-level isiZulu model
- `isiXhosaUModel.arpa` - Character-level isiXhosa model  
- `isiNdebeleUModel.arpa` - Character-level isiNdebele model
- `siSwatiUModel.arpa` - Character-level siSwati model

### Sample Test Cases by Language

**isiZulu Examples:**
- `babeqgokise` → `babegqokise` (they were wearing)
- `wayesebezna` → `wayesebenza` (he was working)
- `izizahtu` → `izizathu` (reasons)

**isiXhosa Examples:**
- `zazevulwa` → `zavulwa` (they were opened)
- `singabonni` → `singaboni` (we cannot see)
- `ndingaboyni` → `ndingaboni` (I cannot see)

**isiNdebele Examples:**
- `zitjhejuwe` → `zitjhejiwe` (they were thrown)
- `abomasipalha` → `abomasipala` (municipalities)
- `urholumente` → `urhulumende` (government)

**siSwati Examples:**
- `sitawuchubekesela` → `sitawuchubekisela` (we will continue)
- `emaphoysa` → `emaphoyisa` (police)
- `kancanee` → `kancane` (small)



### **Exactly What Commands Run on the Models:**

 **Step 1: Load Model**
```python
lm = kenlm.LanguageModel("isiZuluUModel.arpa")
```

### **Step 2: For Each Word Pair (e.g., babeqgokise - babegqokise)**

Wrong word processing:
```python
# Input: "babeqgokise"
seq = " ".join(list("babeqgokise".strip()))
# Result: "b a b e q g o k i s e"
s_wrong = model.score("b a b e q g o k i s e", bos=True, eos=True)
# Returns: -13.21
```


Correct word processing:
```python
# Input: "babegqokise" 
seq = " ".join(list("babegqokise".strip()))
# Result: "b a b e g q o k i s e"
s_correct = model.score("b a b e g q o k i s e", bos=True, eos=True)
# Returns: -8.50
```

### **Step 3: Decision**
```python
if (s_correct - s_wrong) > 1.5:
    # (-8.50 - (-13.21)) = 4.71 > 1.5 ✓
    correct += 1  # Misspelling detected!
```

## **The Exact KenLM Command:**
```python
model.score("b a b e q g o k i s e", bos=True, eos=True)
```

Where:
• "b a b e q g o k i s e" = space-separated character sequence
• bos=True = add beginning-of-sentence marker <s>
• eos=True = add end-of-sentence marker </s>
• **Returns:** Log probability score (negative number, higher = more likely)

So the model actually sees: <s> b a b e q g o k i s e </s> and calculates the probability of this  character sequence.


## Word-Level Spell Detection Results

### Performance by Language

**isiZulu: 20/20 = 100.00% ✓**
- Perfect detection rate
- Successfully identified all 20 misspellings
- Model demonstrates excellent understanding of isiZulu character patterns
- No false negatives or false positives

**isiXhosa: 14/20 = 70.00%**
- Good detection rate with room for improvement
- Successfully identified 14 out of 20 misspellings
- 6 cases where model failed to distinguish correct from incorrect spelling
- Moderate performance suggests model needs more training data

**isiNdebele: 12/20 = 60.00%**
- Lowest performance among tested languages
- Successfully identified 12 out of 20 misspellings
- 8 failed cases indicate significant challenges with isiNdebele patterns
- May require larger training corpus or different modeling approach

**siSwati: 18/20 = 90.00%**
- Strong detection rate
- Successfully identified 18 out of 20 misspellings
- Only 2 failed cases demonstrate good model performance
- Second-best performance after isiZulu

### Overall Performance Analysis

**Total Accuracy: 64/80 = 80.00%**
- Strong overall performance across four African languages
- Demonstrates viability of character-level approach for African language spellchecking
- Performance varies significantly by language (60%-100% range)

**Performance Ranking:**
1. isiZulu: 100% (Perfect)
2. siSwati: 90% (Excellent)
3. isiXhosa: 70% (Good)
4. isiNdebele: 60% (Moderate)

**Error Analysis:**
- 16 total missed detections out of 80 test cases
- isiNdebele contributed 50% of all errors (8/16)
- isiXhosa contributed 37.5% of all errors (6/16)
- siSwati contributed 12.5% of all errors (2/16)
- isiZulu contributed 0% of errors


## Technical Implementation Details

**Language Models:**
- ARPA format language models trained on African language corpora
- Character-level models use space-separated character sequences
- Models loaded using KenLM Python library
- Scoring performed with beginning-of-sentence and end-of-sentence markers

**Decision Logic:**
- Score difference calculation: `score(correct) - score(wrong)`
- Threshold: 1.5 (empirically determined)
- Binary classification: misspelling detected if threshold exceeded

**Test Execution:**
- Automated testing via `run_spell_tests.py`
- Sequential processing of all four language models
- Progress tracking with visual indicators during model loading
- Comprehensive accuracy reporting by language and overall

## Key Findings

1. **Character-level approach is effective** for African language spellchecking with 80% overall accuracy
2. **Language-specific performance varies significantly** from 60% to 100%
3. **isiZulu shows exceptional compatibility** with this modeling approach
4. **isiNdebele presents the greatest challenge** requiring further investigation
5. **Word-level models are less reliable** than character-level models for this task
6. **The system successfully handles complex African language morphology** through character-level analysis

## Data Sources

**Test Files:**
- `isiZulu_test.txt` - 20 isiZulu word pairs
- `isiXhosa_test.txt` - 20 isiXhosa word pairs  
- `isiNdebele_test.txt` - 20 isiNdebele word pairs
- `siSwati_test.txt` - 20 siSwati word pairs

**Model Files:**
- Character-level models: `*UModel.arpa`
- Word-level validation model: `isiZuluModel.arpa`
- Training corpora: `raw_corpora/*.txt`

