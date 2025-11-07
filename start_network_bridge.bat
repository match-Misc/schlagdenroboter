@echo off
chcp 65001 > nul
echo.
echo ================================================
echo   NFC Network Bridge Starter
echo ================================================
echo.

REM Prüfe ob Python installiert ist
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python ist nicht installiert!
    echo.
    echo Bitte installiere Python von: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Prüfe/Installiere erforderliche Pakete
echo Prüfe Python-Pakete...
pip show pyserial > nul 2>&1
if errorlevel 1 (
    echo Installing pyserial...
    pip install pyserial
)

pip show requests > nul 2>&1
if errorlevel 1 (
    echo Installing requests...
    pip install requests
)

echo.
echo ✓ Alle Pakete installiert
echo.
echo Starte NFC Network Bridge...
echo.

REM Starte die Bridge
python nfc_network_bridge.py

pause
