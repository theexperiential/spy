@echo off
REM Build script for Spy - Machine Identity Wallpaper Generator
REM Creates a standalone executable using PyInstaller

echo ============================================================
echo Spy - Build Script
echo ============================================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller is not installed. Installing now...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

echo Building standalone executable...
echo.

REM Build the executable using Python module syntax (use forward slashes for cross-platform compatibility)
python -m PyInstaller --onefile --console --name spy --icon=assets/spy_icon.ico spy.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Build Complete!
echo ============================================================
echo.
echo Executable location: dist\spy.exe
echo File size: Approximately 20-30 MB
echo.
echo You can now distribute this .exe file to any Windows machine.
echo No Python installation required on target machines.
echo.
pause
