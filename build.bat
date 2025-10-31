@echo off
REM Build script for AI Prompt Generator Ultimate

echo ====================================
echo AI Prompt Generator - Build Script
echo ====================================
echo.

REM Check Python
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    exit /b 1
)

REM Run tests
echo.
echo Running tests...
python -m pytest tests/ -v --tb=short
if errorlevel 1 (
    echo WARNING: Some tests failed!
)

REM Build executable
echo.
echo Building executable...
python build_exe.py
if errorlevel 1 (
    echo ERROR: Build failed!
    exit /b 1
)

echo.
echo ====================================
echo Build complete!
echo Executable: dist\AIPromptGenerator.exe
echo ====================================

pause

