# Building ARPA Models on Windows

## Current Folder Structure
```
Spellchecker/
├── character_corpora/          # Your character-level training data
│   ├── isiZuluUCorpus.txt
│   ├── isiXhosaUCorpus.txt
│   ├── isiNdebeleUCorpus.txt
│   └── siSwatiUCorpus.txt
├── vcpkg_installed/
│   └── x64-windows/
│       └── tools/
│           └── kenlm/
│               ├── lmplz.exe   # The tool you need
│               └── ...
└── models/                     # Will be created for output
```

## Steps to Build Models on Windows

### Step 1: Open PowerShell or Command Prompt
Navigate to your Spellchecker directory:
```powershell
cd C:\path\to\Spellchecker
```

### Step 2: Create output directory
```powershell
mkdir models
```

### Step 3: Build each model

Run these commands one by one:

#### isiZulu Model
```powershell
Get-Content character_corpora\isiZuluUCorpus.txt | vcpkg_installed\x64-windows\tools\kenlm\lmplz.exe -o 3 > models\isiZuluUModel.arpa
```

#### isiXhosa Model
```powershell
Get-Content character_corpora\isiXhosaUCorpus.txt | vcpkg_installed\x64-windows\tools\kenlm\lmplz.exe -o 3 > models\isiXhosaUModel.arpa
```

#### isiNdebele Model
```powershell
Get-Content character_corpora\isiNdebeleUCorpus.txt | vcpkg_installed\x64-windows\tools\kenlm\lmplz.exe -o 3 > models\isiNdebeleUModel.arpa
```

#### siSwati Model
```powershell
Get-Content character_corpora\siSwatiUCorpus.txt | vcpkg_installed\x64-windows\tools\kenlm\lmplz.exe -o 3 > models\siSwatiUModel.arpa
```

### Alternative: Use Command Prompt (cmd.exe)

If you're using cmd.exe instead of PowerShell:

```cmd
type character_corpora\isiZuluUCorpus.txt | vcpkg_installed\x64-windows\tools\kenlm\lmplz.exe -o 3 > models\isiZuluUModel.arpa
type character_corpora\isiXhosaUCorpus.txt | vcpkg_installed\x64-windows\tools\kenlm\lmplz.exe -o 3 > models\isiXhosaUModel.arpa
type character_corpora\isiNdebeleUCorpus.txt | vcpkg_installed\x64-windows\tools\kenlm\lmplz.exe -o 3 > models\isiNdebeleUModel.arpa
type character_corpora\siSwatiUCorpus.txt | vcpkg_installed\x64-windows\tools\kenlm\lmplz.exe -o 3 > models\siSwatiUModel.arpa
```

### Step 4: Verify the models were created
```powershell
dir models\*.arpa
```

You should see 4 ARPA files created.

### Step 5: Copy models to test location (optional)
If you want to run tests immediately, copy the models to the kenlm tools directory:
```powershell
copy models\*.arpa vcpkg_installed\x64-windows\tools\kenlm\
```

## What the command does

- **`-o 3`**: Build a 3-gram language model (looks at sequences of 3 characters)
- **Input**: Character corpus (space-separated characters, one word per line)
- **Output**: ARPA format language model file

## Expected Output

Each command will show progress like:
```
=== 1/5 Counting and sorting n-grams ===
Reading character_corpora\isiZuluUCorpus.txt
----5---10---15---20---25---30---35---40---45---50---55---60---65---70---75---80---85---90---95--100
****************************************************************************************************
...
```

The process takes a few minutes per model depending on corpus size.

## Troubleshooting

**Error: "lmplz.exe is not recognized"**
- Make sure you're in the Spellchecker directory
- Check that vcpkg_installed\x64-windows\tools\kenlm\lmplz.exe exists

**Error: "Cannot find path"**
- Use `dir character_corpora` to verify the files exist
- Make sure file names match exactly (case-sensitive)

**Models are empty or very small**
- Check that the character corpus files are not empty
- Verify the input files have the correct format (space-separated characters)
