# Spellchecker Experiment Report

Date: 2025-10-20 23:29:46Z

## Commands

```
python vcpkg_installed\x64-windows\tools\kenlm/run_spell_tests.py
python vcpkg_installed\x64-windows\tools\kenlm/test_perplexity.py
```

## Character-level Results

```
python.exe : Loading the LM will be faster if you build a binary file.
At C:\Users\riski\Desktop\Spellchecker\run_experiment.ps1:18 char:5
+     & $Cmd @ArgList 1> $OutFile 2>&1
+     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Loading the LM ... a binary file.:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
Reading C:\Users\riski\Desktop\Spellchecker\vcpkg_installed\x64-windows\tools\kenlm\isiZuluUModel.arpa
----5---10---15---20---25---30---35---40---45---50---55---60---65---70---75---80---85---90---95--100
****************************************************************************************************
Loading the LM will be faster if you build a binary file.
Reading C:\Users\riski\Desktop\Spellchecker\vcpkg_installed\x64-windows\tools\kenlm\isiXhosaUModel.arpa
----5---10---15---20---25---30---35---40---45---50---55---60---65---70---75---80---85---90---95--100
****************************************************************************************************
Loading the LM will be faster if you build a binary file.
Reading C:\Users\riski\Desktop\Spellchecker\vcpkg_installed\x64-windows\tools\kenlm\isiNdebeleUModel.arpa
----5---10---15---20---25---30---35---40---45---50---55---60---65---70---75---80---85---90---95--100
****************************************************************************************************
Loading the LM will be faster if you build a binary file.
Reading C:\Users\riski\Desktop\Spellchecker\vcpkg_installed\x64-windows\tools\kenlm\siSwatiUModel.arpa
----5---10---15---20---25---30---35---40---45---50---55---60---65---70---75---80---85---90---95--100
****************************************************************************************************
=== Spell Detection Accuracy (Character-level LMs) ===
isiZulu: 20/20 = 100.00%
isiXhosa: 14/20 = 70.00%
isiNdebele: 12/20 = 60.00%
siSwati: 18/20 = 90.00%
Overall: 64/80 = 80.00%

```

## Sentence Perplexity (isiZulu)

```
=== Zulu Sentence Perplexity Check ===
Correct sentence perplexity (lower is better): 9738.58427157086
Wrecked sentence perplexity (lower is better): 7609.360034365502
Result: WARN ù Model did not prefer the correct sentence.

```
