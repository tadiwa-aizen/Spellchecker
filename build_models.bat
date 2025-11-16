@echo off
REM Build ARPA language models from character corpora using KenLM
REM Run this on Windows from the Spellchecker directory

echo ==========================================
echo Building KenLM ARPA Language Models
echo ==========================================
echo.

REM Create output directory
if not exist models mkdir models

REM Set paths
set LMPLZ=vcpkg_installed\x64-windows\tools\kenlm\lmplz.exe
set ORDER=5

REM Check if lmplz exists
if not exist %LMPLZ% (
    echo [ERROR] lmplz.exe not found at: %LMPLZ%
    echo Please ensure you're in the Spellchecker directory
    pause
    exit /b 1
)

echo Building isiZulu model...
echo   Input:  character_corpora\isiZuluUCorpus.txt
echo   Output: models\isiZuluUModel.arpa
echo   Order:  %ORDER%-gram
%LMPLZ% -o %ORDER% < character_corpora\isiZuluUCorpus.txt > models\isiZuluUModel.arpa 2>&1
if exist models\isiZuluUModel.arpa (
    echo   [OK] Model built!
) else (
    echo   [ERROR] Failed to build model
)
echo.

echo Building isiXhosa model...
echo   Input:  character_corpora\isiXhosaUCorpus.txt
echo   Output: models\isiXhosaUModel.arpa
echo   Order:  %ORDER%-gram
%LMPLZ% -o %ORDER% < character_corpora\isiXhosaUCorpus.txt > models\isiXhosaUModel.arpa 2>&1
if exist models\isiXhosaUModel.arpa (
    echo   [OK] Model built!
) else (
    echo   [ERROR] Failed to build model
)
echo.

echo Building isiNdebele model...
echo   Input:  character_corpora\isiNdebeleUCorpus.txt
echo   Output: models\isiNdebeleUModel.arpa
echo   Order:  %ORDER%-gram
%LMPLZ% -o %ORDER% < character_corpora\isiNdebeleUCorpus.txt > models\isiNdebeleUModel.arpa 2>&1
if exist models\isiNdebeleUModel.arpa (
    echo   [OK] Model built!
) else (
    echo   [ERROR] Failed to build model
)
echo.

echo Building siSwati model...
echo   Input:  character_corpora\siSwatiUCorpus.txt
echo   Output: models\siSwatiUModel.arpa
echo   Order:  %ORDER%-gram
%LMPLZ% -o %ORDER% < character_corpora\siSwatiUCorpus.txt > models\siSwatiUModel.arpa 2>&1
if exist models\siSwatiUModel.arpa (
    echo   [OK] Model built!
) else (
    echo   [ERROR] Failed to build model
)
echo.

echo ==========================================
echo Complete! Check models\ folder
echo ==========================================
echo.
dir models\*.arpa
echo.
pause
