@echo off
echo ========================================
echo Instalacja Transkrypcja YT/Facebook
echo ========================================
echo.

echo [1/3] Sprawdzanie Pythona...
python --version
if errorlevel 1 (
    echo BLAD: Python nie jest zainstalowany!
    echo Pobierz z: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo [2/3] Sprawdzanie FFmpeg...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo UWAGA: FFmpeg nie jest zainstalowany!
    echo Musisz zainstalowac FFmpeg aby aplikacja dzialala.
    echo.
    echo Opcja 1: choco install ffmpeg
    echo Opcja 2: Pobierz z https://www.gyan.dev/ffmpeg/builds/
    echo.
    pause
)

echo.
echo [3/3] Instalowanie pakietow Python...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo BLAD: Nie udalo sie zainstalowac pakietow!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Instalacja zakonczona pomyslnie!
echo ========================================
echo.
echo Aby uruchomic aplikacje, uzyj: run.bat
echo lub: streamlit run app.py
echo.
pause
