@echo off 
chcp 65001 >nul 
title Verificare Sistem 
echo. 
echo ============================================ 
echo    VERIFICARE SISTEM & PROIECT 
echo ============================================ 
echo. 
cd /d "%~dp0" 
 
echo [CHECK] Verificare Git... 
git --version >nul 2>&1 
if %errorlevel% equ 0 ( 
    echo [OK] Git instalat 
) else ( 
    echo [EROARE] Git NU este instalat! 
    echo Descarca: https://git-scm.com/download/win 
) 
 
echo [CHECK] Verificare Python... 
python --version >nul 2>&1 
if %errorlevel% equ 0 ( 
    echo [OK] Python instalat 
) else ( 
    echo [WARN] Python nu este detectat 
) 
 
echo. 
echo [INFO] Verificare completa! 
echo. 
pause 
