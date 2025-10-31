@echo off 
chcp 65001 >nul 
title Sincronizare GitHub 
echo. 
echo ============================================ 
echo    SINCRONIZARE CU GITHUB 
echo ============================================ 
echo. 
cd /d "%~dp0" 
 
git status --porcelain | find /v "" >nul 
if %errorlevel% neq 0 ( 
    echo [INFO] Nu exista modificari 
    pause 
    exit /b 0 
) 
 
echo [INFO] Fisiere modificate: 
git status --short 
echo. 
 
set /p msg="Mesaj commit (Enter pentru auto): " 
if "%msg%"=="" set msg=Update: %date% %time% 
 
echo. 
echo [SYNC] Sincronizare in curs... 
git add . 
git commit -m "%msg%" 
git push -u origin main 
 
if %errorlevel% equ 0 ( 
    echo. 
    echo [OK] Sincronizare completa! 
    echo Verifica: https://github.com/RolandPetrila/Sistem_Prompt_Monitorizare 
) else ( 
    echo. 
    echo [EROARE] Sincronizare esuata! 
    echo Verifica Personal Access Token 
) 
 
echo. 
pause 
