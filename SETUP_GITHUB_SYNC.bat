@echo off
chcp 65001 >nul
title Setup GitHub Sync - Automatizat
color 0A

echo.
echo ================================================================================
echo    SETUP AUTOMAT SINCRONIZARE GITHUB
echo    Proiect: ai_prompt_generator_ultimate
echo ================================================================================
echo.

cd /d "%~dp0"

echo [INFO] Creare scripturi de sincronizare...
echo.

REM ===== 1. Creează VERIFY_SYSTEM.bat =====
echo @echo off > VERIFY_SYSTEM.bat
echo chcp 65001 ^>nul >> VERIFY_SYSTEM.bat
echo title Verificare Sistem >> VERIFY_SYSTEM.bat
echo echo. >> VERIFY_SYSTEM.bat
echo echo ============================================ >> VERIFY_SYSTEM.bat
echo echo    VERIFICARE SISTEM ^& PROIECT >> VERIFY_SYSTEM.bat
echo echo ============================================ >> VERIFY_SYSTEM.bat
echo echo. >> VERIFY_SYSTEM.bat
echo cd /d "%%~dp0" >> VERIFY_SYSTEM.bat
echo. >> VERIFY_SYSTEM.bat
echo echo [CHECK] Verificare Git... >> VERIFY_SYSTEM.bat
echo git --version ^>nul 2^>^&1 >> VERIFY_SYSTEM.bat
echo if %%errorlevel%% equ 0 ( >> VERIFY_SYSTEM.bat
echo     echo [OK] Git instalat >> VERIFY_SYSTEM.bat
echo ) else ( >> VERIFY_SYSTEM.bat
echo     echo [EROARE] Git NU este instalat! >> VERIFY_SYSTEM.bat
echo     echo Descarca: https://git-scm.com/download/win >> VERIFY_SYSTEM.bat
echo ) >> VERIFY_SYSTEM.bat
echo. >> VERIFY_SYSTEM.bat
echo echo [CHECK] Verificare Python... >> VERIFY_SYSTEM.bat
echo python --version ^>nul 2^>^&1 >> VERIFY_SYSTEM.bat
echo if %%errorlevel%% equ 0 ( >> VERIFY_SYSTEM.bat
echo     echo [OK] Python instalat >> VERIFY_SYSTEM.bat
echo ) else ( >> VERIFY_SYSTEM.bat
echo     echo [WARN] Python nu este detectat >> VERIFY_SYSTEM.bat
echo ) >> VERIFY_SYSTEM.bat
echo. >> VERIFY_SYSTEM.bat
echo echo. >> VERIFY_SYSTEM.bat
echo echo [INFO] Verificare completa! >> VERIFY_SYSTEM.bat
echo echo. >> VERIFY_SYSTEM.bat
echo pause >> VERIFY_SYSTEM.bat

echo [OK] Creat: VERIFY_SYSTEM.bat

REM ===== 2. Creează SETUP_GIT.bat =====
echo @echo off > SETUP_GIT.bat
echo chcp 65001 ^>nul >> SETUP_GIT.bat
echo title Setup Git Repository >> SETUP_GIT.bat
echo echo. >> SETUP_GIT.bat
echo echo ============================================ >> SETUP_GIT.bat
echo echo    SETUP GIT REPOSITORY >> SETUP_GIT.bat
echo echo ============================================ >> SETUP_GIT.bat
echo echo. >> SETUP_GIT.bat
echo cd /d "%%~dp0" >> SETUP_GIT.bat
echo. >> SETUP_GIT.bat
echo if not exist .git ( >> SETUP_GIT.bat
echo     git init >> SETUP_GIT.bat
echo     echo [OK] Repository Git creat >> SETUP_GIT.bat
echo ) else ( >> SETUP_GIT.bat
echo     echo [OK] Repository Git exista >> SETUP_GIT.bat
echo ) >> SETUP_GIT.bat
echo. >> SETUP_GIT.bat
echo git config user.name "RolandPetrila" >> SETUP_GIT.bat
echo set /p email="Introdu email GitHub: " >> SETUP_GIT.bat
echo git config user.email "%%email%%" >> SETUP_GIT.bat
echo echo [OK] User Git configurat >> SETUP_GIT.bat
echo. >> SETUP_GIT.bat
echo git remote get-url origin ^>nul 2^>^&1 >> SETUP_GIT.bat
echo if %%errorlevel%% neq 0 ( >> SETUP_GIT.bat
echo     git remote add origin https://github.com/RolandPetrila/Sistem_Prompt_Monitorizare.git >> SETUP_GIT.bat
echo     echo [OK] Remote GitHub adaugat >> SETUP_GIT.bat
echo ) else ( >> SETUP_GIT.bat
echo     echo [OK] Remote deja configurat >> SETUP_GIT.bat
echo ) >> SETUP_GIT.bat
echo. >> SETUP_GIT.bat
echo if not exist .gitignore ( >> SETUP_GIT.bat
echo     echo __pycache__/ ^> .gitignore >> SETUP_GIT.bat
echo     echo *.pyc ^>^> .gitignore >> SETUP_GIT.bat
echo     echo venv/ ^>^> .gitignore >> SETUP_GIT.bat
echo     echo venv311/ ^>^> .gitignore >> SETUP_GIT.bat
echo     echo .vscode/ ^>^> .gitignore >> SETUP_GIT.bat
echo     echo dist/ ^>^> .gitignore >> SETUP_GIT.bat
echo     echo build/ ^>^> .gitignore >> SETUP_GIT.bat
echo     echo *.exe ^>^> .gitignore >> SETUP_GIT.bat
echo     echo *.log ^>^> .gitignore >> SETUP_GIT.bat
echo     echo config.json ^>^> .gitignore >> SETUP_GIT.bat
echo     echo .backup_*/ ^>^> .gitignore >> SETUP_GIT.bat
echo     echo [OK] .gitignore creat >> SETUP_GIT.bat
echo ) >> SETUP_GIT.bat
echo. >> SETUP_GIT.bat
echo echo. >> SETUP_GIT.bat
echo echo [INFO] Setup complet! >> SETUP_GIT.bat
echo echo. >> SETUP_GIT.bat
echo pause >> SETUP_GIT.bat

echo [OK] Creat: SETUP_GIT.bat

REM ===== 3. Creează SYNC_NOW.bat =====
echo @echo off > SYNC_NOW.bat
echo chcp 65001 ^>nul >> SYNC_NOW.bat
echo title Sincronizare GitHub >> SYNC_NOW.bat
echo echo. >> SYNC_NOW.bat
echo echo ============================================ >> SYNC_NOW.bat
echo echo    SINCRONIZARE CU GITHUB >> SYNC_NOW.bat
echo echo ============================================ >> SYNC_NOW.bat
echo echo. >> SYNC_NOW.bat
echo cd /d "%%~dp0" >> SYNC_NOW.bat
echo. >> SYNC_NOW.bat
echo git status --porcelain ^| find /v "" ^>nul >> SYNC_NOW.bat
echo if %%errorlevel%% neq 0 ( >> SYNC_NOW.bat
echo     echo [INFO] Nu exista modificari >> SYNC_NOW.bat
echo     pause >> SYNC_NOW.bat
echo     exit /b 0 >> SYNC_NOW.bat
echo ) >> SYNC_NOW.bat
echo. >> SYNC_NOW.bat
echo echo [INFO] Fisiere modificate: >> SYNC_NOW.bat
echo git status --short >> SYNC_NOW.bat
echo echo. >> SYNC_NOW.bat
echo. >> SYNC_NOW.bat
echo set /p msg="Mesaj commit (Enter pentru auto): " >> SYNC_NOW.bat
echo if "%%msg%%"=="" set msg=Update: %%date%% %%time%% >> SYNC_NOW.bat
echo. >> SYNC_NOW.bat
echo echo. >> SYNC_NOW.bat
echo echo [SYNC] Sincronizare in curs... >> SYNC_NOW.bat
echo git add . >> SYNC_NOW.bat
echo git commit -m "%%msg%%" >> SYNC_NOW.bat
echo git push -u origin main >> SYNC_NOW.bat
echo. >> SYNC_NOW.bat
echo if %%errorlevel%% equ 0 ( >> SYNC_NOW.bat
echo     echo. >> SYNC_NOW.bat
echo     echo [OK] Sincronizare completa! >> SYNC_NOW.bat
echo     echo Verifica: https://github.com/RolandPetrila/Sistem_Prompt_Monitorizare >> SYNC_NOW.bat
echo ) else ( >> SYNC_NOW.bat
echo     echo. >> SYNC_NOW.bat
echo     echo [EROARE] Sincronizare esuata! >> SYNC_NOW.bat
echo     echo Verifica Personal Access Token >> SYNC_NOW.bat
echo ) >> SYNC_NOW.bat
echo. >> SYNC_NOW.bat
echo echo. >> SYNC_NOW.bat
echo pause >> SYNC_NOW.bat

echo [OK] Creat: SYNC_NOW.bat

REM ===== 4. Creează README =====
echo # GHID SINCRONIZARE GITHUB > README_SYNC.txt
echo. >> README_SYNC.txt
echo UTILIZARE: >> README_SYNC.txt
echo 1. Ruleaza: VERIFY_SYSTEM.bat (verifica sistemul) >> README_SYNC.txt
echo 2. Ruleaza: SETUP_GIT.bat (setup initial, o singura data) >> README_SYNC.txt
echo 3. Ruleaza: SYNC_NOW.bat (sincronizare) >> README_SYNC.txt
echo. >> README_SYNC.txt
echo AUTENTIFICARE GITHUB: >> README_SYNC.txt
echo - Username: RolandPetrila >> README_SYNC.txt
echo - Password: Foloseste Personal Access Token >> README_SYNC.txt
echo - Creaza token: https://github.com/settings/tokens >> README_SYNC.txt

echo [OK] Creat: README_SYNC.txt

echo.
echo ================================================================================
echo [SUCCESS] Toate scripturile au fost create!
echo ================================================================================
echo.
echo URMATORII PASI:
echo 1. Dublu-click pe: VERIFY_SYSTEM.bat
echo 2. Dublu-click pe: SETUP_GIT.bat
echo 3. Dublu-click pe: SYNC_NOW.bat
echo.
echo ================================================================================
pause