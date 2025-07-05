@echo off
title QuakeSafe Game - Automatic Package Installation

echo.
echo 🎮 QuakeSafe Game - Automatic Package Installation
echo ==================================================
echo.

echo 🔍 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found in system
    echo 💡 Please install Python from https://www.python.org/downloads/
    echo ⚠️  Don't forget to check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo ✅ Python found
python --version

echo.
echo 🔍 Checking pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip not found
    echo 💡 Try using: python -m pip instead
    echo.
    pause
    exit /b 1
)

echo ✅ pip found
pip --version

echo.
echo 📦 Installing required packages...
echo.

echo 🎯 Installing pygame...
pip install pygame
if %errorlevel% neq 0 (
    echo ❌ pygame installation failed
    echo 💡 Try: python -m pip install pygame
    pause
    exit /b 1
)

echo.
echo 🎯 Installing pyinstaller (for creating .exe files)...
pip install pyinstaller
if %errorlevel% neq 0 (
    echo ⚠️  pyinstaller installation failed (not required for playing the game)
)

echo.
echo ✅ Installation completed!
echo.
echo 🎮 You can now play the game by:
echo    1. Double-clicking QuakeSafe.exe (easy way)
echo    2. Or running: python quakesafe_game.py
echo.
echo 📋 Installed packages:
pip list | findstr pygame
pip list | findstr pyinstaller

echo.
echo 🎉 Ready to play QuakeSafe!
echo.
pause