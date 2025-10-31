# ====================================================================================
# SCRIPT MASTER - Rulează acest fișier pentru a crea toate scripturile de sync
# Autor: GitHub Copilot
# Versiune: 2.0 (Corectat și Funcțional)
# ====================================================================================

param(
    [string]$GitEmail = ""
)

Write-Host "`n🚀 INSTALARE AUTOMATĂ COMPLETĂ - SISTEM SINCRONIZARE GITHUB" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# Cale dinamică: proiectul este directorul unde se află acest script
$projectPath = $PSScriptRoot
Set-Location $projectPath

Write-Host "✅ Locație confirmată: $projectPath" -ForegroundColor Green
Write-Host "`n📝 Creare scripturi de sincronizare..." -ForegroundColor Yellow

# ------------------------------------------------------------------------------------
# 1. VERIFY_SYSTEM.ps1
# ------------------------------------------------------------------------------------
try {
@'
# SCRIPT VERIFICARE COMPLETĂ - NU ȘTERGE NIMIC!
param([switch]$AutoInstall = $false)

Write-Host "`n===============================================" -ForegroundColor Cyan
Write-Host "   🔍 VERIFICARE COMPLETĂ SISTEM ȘI PROIECT" -ForegroundColor Cyan
Write-Host "===============================================`n" -ForegroundColor Cyan

$projectPath = $PSScriptRoot
Set-Location $projectPath
$reportPath = Join-Path -Path $projectPath -ChildPath "VERIFICATION_REPORT_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
$issues = @()
$warnings = @()
$success = @()

# Verificare Git
Write-Host "📦 Verificare Git..." -ForegroundColor Yellow
$gitInstalled = Get-Command git -ErrorAction SilentlyContinue
if ($gitInstalled) {
    $gitVersion = git --version
    Write-Host "✅ Git instalat: $gitVersion" -ForegroundColor Green
    $success += "Git instalat"
} else {
    Write-Host "❌ Git NU este instalat!" -ForegroundColor Red
    $issues += "Git lipsește"
    
    if ($AutoInstall) {
        Write-Host "🔧 Instalare automată Git..." -ForegroundColor Yellow
        $gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.2/Git-2.42.0.2-64-bit.exe"
        $gitInstaller = Join-Path -Path $env:TEMP -ChildPath "GitInstaller.exe"
        
        Write-Host "   Descărcare Git..." -ForegroundColor Cyan
        Invoke-WebRequest -Uri $gitUrl -OutFile $gitInstaller -UseBasicParsing
        
        Write-Host "   Instalare Git..." -ForegroundColor Cyan
        Start-Process -FilePath $gitInstaller -ArgumentList "/VERYSILENT", "/NORESTART" -Wait
        
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        Write-Host "✅ Git instalat cu succes! Repornește PowerShell și rulează din nou." -ForegroundColor Green
        exit 0
    }
}

# Verificare Python
Write-Host "`n🐍 Verificare Python..." -ForegroundColor Yellow
$pythonInstalled = Get-Command python -ErrorAction SilentlyContinue
if ($pythonInstalled) {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python instalat: $pythonVersion" -ForegroundColor Green
    $success += "Python instalat"
} else {
    Write-Host "⚠️ Python nu este detectat" -ForegroundColor Yellow
    $warnings += "Python lipsește"
}

# Test conexiune GitHub
Write-Host "`n🌐 Test conexiune GitHub..." -ForegroundColor Yellow
try {
    Invoke-WebRequest -Uri "https://api.github.com/repos/RolandPetrila/Sistem_Prompt_Monitorizare" -UseBasicParsing -TimeoutSec 10 | Out-Null
    Write-Host "✅ Conexiune GitHub OK" -ForegroundColor Green
    $success += "GitHub accesibil"
} catch {
    Write-Host "⚠️ Nu se poate accesa repo GitHub. Verifică conexiunea internet." -ForegroundColor Yellow
    $warnings += "Verifică conexiunea internet"
}

# Sumar
Write-Host "`n" + "=" * 50 -ForegroundColor Cyan
Write-Host "📊 REZULTAT VERIFICARE" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host "✅ Verificări reușite: $($success.Count)" -ForegroundColor Green
$success | ForEach-Object { Write-Host "   - $_" -ForegroundColor Green }

if ($warnings.Count -gt 0) {
    Write-Host "⚠️ Avertismente: $($warnings.Count)" -ForegroundColor Yellow
    $warnings | ForEach-Object { Write-Host "   - $_" -ForegroundColor Yellow }
}

if ($issues.Count -gt 0) {
    Write-Host "❌ Probleme: $($issues.Count)" -ForegroundColor Red
    $issues | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
} else {
    Write-Host "`n✅ SISTEM PREGĂTIT PENTRU SINCRONIZARE!" -ForegroundColor Green
}

"VERIFICATION REPORT - $(Get-Date)" | Out-File $reportPath
"=" * 50 | Add-Content $reportPath
"Success: $($success -join ', ')" | Add-Content $reportPath
"Warnings: $($warnings -join ', ')" | Add-Content $reportPath
"Issues: $($issues -join ', ')" | Add-Content $reportPath

Write-Host "`n📄 Raport salvat: $reportPath" -ForegroundColor Gray
'@ | Set-Content -Path (Join-Path $projectPath "VERIFY_SYSTEM.ps1") -Encoding UTF8
    Write-Host "   ✅ Creat: VERIFY_SYSTEM.ps1" -ForegroundColor Green
} catch {
    Write-Host "❌ Eroare la crearea VERIFY_SYSTEM.ps1: $_" -ForegroundColor Red
}

# ------------------------------------------------------------------------------------
# 2. SETUP_SAFE_SYNC.ps1
# ------------------------------------------------------------------------------------
try {
$setupScriptContent = @"
# SETUP SIGUR - NU ȘTERGE NIMIC
param(
    [string]`$GitEmail = "$($using:GitEmail)"
)
Write-Host "`n🛡️ SETUP SIGUR PENTRU SINCRONIZARE GITHUB" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

`$projectPath = `$PSScriptRoot
Set-Location `$projectPath

Write-Host "`n💾 Dorești backup de siguranță? (Y/N)" -ForegroundColor Yellow
`$backup = Read-Host
if (`$backup -eq "Y") {
    `$backupDir = ".backup_`$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    New-Item -ItemType Directory -Path `$backupDir -Force | Out-Null
    Get-ChildItem -File -Filter "*.py" | Copy-Item -Destination `$backupDir
    Get-ChildItem -File -Filter "*.txt" | Copy-Item -Destination `$backupDir
    Get-ChildItem -File -Filter "*.md" | Copy-Item -Destination `$backupDir
    Write-Host "✅ Backup creat în: `$backupDir" -ForegroundColor Green
}

if (!(Test-Path ".git")) {
    git init
    Write-Host "✅ Repository Git creat" -ForegroundColor Green
} else {
    Write-Host "✅ Repository Git există" -ForegroundColor Green
}

`$currentUser = git config user.name 2>`$null
if (!`$currentUser) {
    git config user.name "RolandPetrila"
    if (`$GitEmail) {
        git config user.email "`$GitEmail"
    } else {
        `$emailInput = Read-Host "Introdu adresa de email asociată contului tău GitHub"
        git config user.email "`$emailInput"
    }
    Write-Host "✅ User Git configurat" -ForegroundColor Green
}

`$remoteUrl = "https://github.com/RolandPetrila/Sistem_Prompt_Monitorizare.git"
`$currentRemote = git remote get-url origin 2>`$null
if (!`$currentRemote) {
    git remote add origin `$remoteUrl
    Write-Host "✅ Remote GitHub adăugat" -ForegroundColor Green
} else {
    Write-Host "✅ Remote deja configurat" -ForegroundColor Green
}

if (!(Test-Path ".gitignore")) {
    @"
__pycache__/
*.py[cod]
venv/
venv311/
.vscode/
.idea/
build/
dist/
*.exe
*.spec
.pytest_cache/
htmlcov/
.coverage
*.log
*.db
config.json
.env
.backup_*/
*.tmp
"@ | Set-Content ".gitignore" -Encoding UTF8
    Write-Host "✅ .gitignore creat" -ForegroundColor Green
}

Write-Host "`n✅ SETUP COMPLET!" -ForegroundColor Green
Write-Host "Rulează: .\SAFE_SYNC_TO_GITHUB.ps1" -ForegroundColor Yellow
"@
    $setupScriptContent | Set-Content -Path (Join-Path $projectPath "SETUP_SAFE_SYNC.ps1") -Encoding UTF8
    Write-Host "   ✅ Creat: SETUP_SAFE_SYNC.ps1" -ForegroundColor Green
} catch {
    Write-Host "❌ Eroare la crearea SETUP_SAFE_SYNC.ps1: $_" -ForegroundColor Red
}

# ------------------------------------------------------------------------------------
# 3. SAFE_SYNC_TO_GITHUB.ps1
# ------------------------------------------------------------------------------------
try {
@'
# SINCRONIZARE SIGURĂ
param(
    [string]$CommitMessage = "",
    [switch]$DryRun = $false
)

Write-Host "`n🔄 SINCRONIZARE CU GITHUB" -ForegroundColor Cyan
Set-Location $PSScriptRoot

$status = git status --porcelain
if (!$status) {
    Write-Host "✅ Nu există modificări" -ForegroundColor Green
    exit 0
}

Write-Host "`n📊 Fișiere modificate:" -ForegroundColor Yellow
$status | ForEach-Object { Write-Host "   $_" -ForegroundColor Gray }

if ($DryRun) {
    Write-Host "`n🔍 DRY RUN - Doar simulare" -ForegroundColor Magenta
    exit 0
}

if (!$CommitMessage) {
    $CommitMessage = Read-Host "`n📝 Introdu un mesaj pentru commit (sau lasă gol pentru auto-mesaj)"
    if (!$CommitMessage) {
        $CommitMessage = "Auto-update: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    }
}

Write-Host "`n⚠️ Confirmi sincronizarea cu mesajul: '$CommitMessage'? (Y/N)" -ForegroundColor Yellow
$confirm = Read-Host
if ($confirm -ne "Y") {
    Write-Host "❌ Anulat" -ForegroundColor Red
    exit 0
}

git add .
git commit -m "$CommitMessage"
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ SINCRONIZARE COMPLETĂ!" -ForegroundColor Green
    Write-Host "🔗 Vezi pe: https://github.com/RolandPetrila/Sistem_Prompt_Monitorizare" -ForegroundColor Cyan
} else {
    Write-Host "`n❌ Eroare la push!" -ForegroundColor Red
    Write-Host "Soluții:" -ForegroundColor Yellow
    Write-Host "1. Verifică Personal Access Token" -ForegroundColor White
    Write-Host "2. Creează token: https://github.com/settings/tokens" -ForegroundColor Cyan
}
'@ | Set-Content -Path (Join-Path $projectPath "SAFE_SYNC_TO_GITHUB.ps1") -Encoding UTF8
    Write-Host "   ✅ Creat: SAFE_SYNC_TO_GITHUB.ps1" -ForegroundColor Green
} catch {
    Write-Host "❌ Eroare la crearea SAFE_SYNC_TO_GITHUB.ps1: $_" -ForegroundColor Red
}

# ------------------------------------------------------------------------------------
# 4. AUTO_MONITOR.ps1
# ------------------------------------------------------------------------------------
try {
@'
# MONITORIZARE AUTOMATĂ
Write-Host "👁️ MONITORIZARE AUTOMATĂ ACTIVĂ" -ForegroundColor Cyan
Write-Host "Apasă Ctrl+C pentru oprire" -ForegroundColor Yellow

$projectPath = $PSScriptRoot
Set-Location $projectPath

$lastSync = Get-Date
$syncInterval = 300  # 5 minute

while ($true) {
    $changes = git status --porcelain
    if ($changes) {
        $timeSinceSync = ((Get-Date) - $lastSync).TotalSeconds
        if ($timeSinceSync -ge $syncInterval) {
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Sincronizare automată..." -ForegroundColor Cyan
            git add .
            git commit -m "Auto-sync: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
            git push origin main
            $lastSync = Get-Date
            Write-Host "✅ Sincronizat" -ForegroundColor Green
        } else {
            $remaining = [int]($syncInterval - $timeSinceSync)
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Modificări detectate. Sync în $remaining secunde" -ForegroundColor Gray
        }
    }
    Start-Sleep -Seconds 30
}
'@ | Set-Content -Path (Join-Path $projectPath "AUTO_MONITOR.ps1") -Encoding UTF8
    Write-Host "   ✅ Creat: AUTO_MONITOR.ps1" -ForegroundColor Green
} catch {
    Write-Host "❌ Eroare la crearea AUTO_MONITOR.ps1: $_" -ForegroundColor Red
}

# ------------------------------------------------------------------------------------
# 5. SYNC_NOW.bat
# ------------------------------------------------------------------------------------
try {
@'
@echo off
title Quick Sync to GitHub
echo ========================================
echo    SINCRONIZARE RAPIDA GITHUB
echo ========================================
echo.

cd /d "%~dp0"

powershell -ExecutionPolicy Bypass -File SAFE_SYNC_TO_GITHUB.ps1 -CommitMessage "Manual quick-sync"

echo.
echo Apasa orice tasta...
pause >nul
'@ | Set-Content -Path (Join-Path $projectPath "SYNC_NOW.bat") -Encoding ASCII
    Write-Host "   ✅ Creat: SYNC_NOW.bat" -ForegroundColor Green
} catch {
    Write-Host "❌ Eroare la crearea SYNC_NOW.bat: $_" -ForegroundColor Red
}

# ------------------------------------------------------------------------------------
# 6. README_SYNC.md
# ------------------------------------------------------------------------------------
try {
@'
# 📚 GHID SINCRONIZARE GITHUB

## 🚀 Quick Start

### 1️⃣ Prima utilizare
```powershell
# Verificare sistem (recomandat)
.\VERIFY_SYSTEM.ps1

# Setup inițial (obligatoriu o singură dată)
.\SETUP_SAFE_SYNC.ps1

# Prima sincronizare
.\SAFE_SYNC_TO_GITHUB.ps1