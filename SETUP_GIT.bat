@echo off 
chcp 65001 >nul 
title Setup Git Repository 
echo. 
echo ============================================ 
echo    SETUP GIT REPOSITORY 
echo ============================================ 
echo. 
cd /d "%~dp0" 
 
if not exist .git ( 
    git init 
    echo [OK] Repository Git creat 
) else ( 
    echo [OK] Repository Git exista 
) 
 
git config user.name "RolandPetrila" 
set /p email="Introdu email GitHub: " 
git config user.email "%email%" 
echo [OK] User Git configurat 
 
git remote get-url origin >nul 2>&1 
if %errorlevel% neq 0 ( 
    git remote add origin https://github.com/RolandPetrila/Sistem_Prompt_Monitorizare.git 
    echo [OK] Remote GitHub adaugat 
) else ( 
    echo [OK] Remote deja configurat 
) 
 
if not exist .gitignore ( 
    echo __pycache__/ > .gitignore 
    echo *.pyc >> .gitignore 
    echo venv/ >> .gitignore 
    echo venv311/ >> .gitignore 
    echo .vscode/ >> .gitignore 
    echo dist/ >> .gitignore 
    echo build/ >> .gitignore 
    echo *.exe >> .gitignore 
    echo *.log >> .gitignore 
    echo config.json >> .gitignore 
    echo .backup_*/ >> .gitignore 
    echo [OK] .gitignore creat 
) 
 
echo. 
echo [INFO] Setup complet! 
echo. 
pause 
