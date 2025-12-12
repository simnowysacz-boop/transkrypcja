@echo off
echo ========================================
echo Uruchamianie Transkrypcja YT/Facebook
echo ========================================
echo.
echo Aplikacja otworzy sie w przegladarce...
echo Aby zatrzymac, nacisnij Ctrl+C
echo.

REM Dodaj FFmpeg do PATH
set PATH=%PATH%;C:\Users\win11\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin

streamlit run app.py
pause
