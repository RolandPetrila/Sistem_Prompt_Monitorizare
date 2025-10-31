# Build & Deployment

## Development Setup

### Prerequisites
- **Python**: 3.10+ (tested on 3.13.7)
- **pip**: Latest version
- **Git**: For version control (optional)

### Installation Steps

#### 1. Clone Repository
```bash
git clone <repository-url>
cd ai_prompt_generator_ultimate
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure API Keys
Edit `config_local.json`:
```json
{
  "ai_providers": {
    "claude": {
      "api_key": "your-claude-key",
      "model": "claude-sonnet-4-20250514",
      "priority": 1,
      "enabled": true
    },
    "openai": {
      "api_key": "your-openai-key",
      "model": "gpt-4-turbo-preview",
      "priority": 2,
      "enabled": true
    },
    "gemini": {
      "api_key": "your-gemini-key",
      "model": "gemini-1.5-pro",
      "priority": 3,
      "enabled": true
    }
  }
}
```

Or use script:
```bash
python scripts/load_api_keys.py
```

#### 5. Run Application
```bash
python main.py
```

## Build Process

### PyInstaller Configuration

#### Entry Point
- **Main Script**: `main.py`
- **Application Name**: `AIPromptGenerator`
- **Executable Type**: Windowed (no console)

#### Hidden Imports
- `PySide6` (Qt framework)
- `anthropic` (Claude API)
- `openai` (OpenAI API)
- `google.generativeai` (Gemini API)
- `tree_sitter` (code parsing)

#### Data Files Included
- `config/` directory (configuration templates)

#### Excluded Modules
- Development dependencies (pytest, coverage, etc.)
- Unused packages

#### Output Settings
- **Output Directory**: `dist/`
- **Executable Name**: `AIPromptGenerator.exe`
- **Icon**: None (can be added)
- **Console**: False (windowed mode)
- **Onefile**: True (single executable)

### PyInstaller Spec File

**File**: `AIPromptGenerator.spec`

```python
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('config', 'config')],
    hiddenimports=[
        'PySide6',
        'anthropic',
        'openai',
        'google.generativeai',
        'tree_sitter'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AIPromptGenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='NONE',
)
```

### Build Script

**File**: `build_exe.py`

```python
"""Build executable using PyInstaller."""
import subprocess
import sys
from pathlib import Path

def build_exe() -> int:
    """Build executable using PyInstaller."""
    cmd = [
        "pyinstaller",
        "--name=AIPromptGenerator",
        "--windowed",
        "--onefile",
        "--icon=NONE",
        "--add-data=config;config",
        "--hidden-import=PySide6",
        "--hidden-import=anthropic",
        "--hidden-import=openai",
        "--hidden-import=google.generativeai",
        "--hidden-import=tree_sitter",
        "main.py"
    ]
    
    result = subprocess.run(cmd, check=True)
    return 0

if __name__ == "__main__":
    sys.exit(build_exe())
```

### Build Commands

#### Using Spec File
```bash
pyinstaller AIPromptGenerator.spec
```

#### Using Build Script
```bash
python build_exe.py
```

#### Using Batch Script (Windows)
```bash
build.bat
```

### Build Output

**Location**: `dist/AIPromptGenerator.exe`

**Size**: ~50-100 MB (estimated, depends on dependencies)

**Requirements**:
- Windows 10/11
- 4GB RAM minimum
- 500MB disk space for installation

## NSIS Installer

### Installer Configuration

**File**: `installer.nsi`

#### Installer Information
- **Application Name**: AI Prompt Generator Ultimate
- **Version**: 1.0.0
- **Publisher**: AI Tools
- **Install Directory**: `$PROGRAMFILES64\AIPromptGenerator`
- **Executable**: `AIPromptGenerator.exe`

#### Features
- Welcome page
- License agreement (LICENSE file)
- Components selection
- Directory selection
- Installation progress
- Finish page with options

#### Registry Entries
```
HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\AIPromptGenerator
- DisplayName: AI Prompt Generator Ultimate
- DisplayVersion: 1.0.0
- Publisher: AI Tools
- UninstallString: $INSTDIR\Uninstall.exe
```

#### Shortcuts Created
- Start Menu: `$SMPROGRAMS\AIPromptGenerator\AI Prompt Generator Ultimate.lnk`
- Desktop: `$DESKTOP\AI Prompt Generator Ultimate.lnk`
- Uninstaller: `$SMPROGRAMS\AIPromptGenerator\Uninstall.lnk`

#### Files Installed
- `AIPromptGenerator.exe`
- `README.md`
- `LICENSE`
- `config/` directory
- `Uninstall.exe`

### Build Installer

```bash
makensis installer.nsi
```

**Output**: `AIPromptGenerator_Setup_1.0.0.exe`

**Size**: ~50-100 MB (estimated)

## Release Workflow

### Automated Release Script

**File**: `release_v1.0.0.ps1` (PowerShell) or `release_v1.0.0.sh` (Bash)

### Release Steps (7 total)

#### Step 1: Dependencies Verification (5 min)
```bash
# Generate actual dependencies
pip freeze > requirements_actual.txt

# Compare with expected
# Verify critical packages
python -c "import PySide6, anthropic, openai, google.generativeai; print('OK')"
```

**Validation**:
- ✅ All dependencies installed
- ✅ Critical packages available
- ✅ Requirements file updated

#### Step 2: Full Test Suite (10 min)
```bash
# Run all tests with coverage
pytest tests/ -v --cov=. --cov-report=html --cov-report=term --cov-report=json

# Extract coverage percentage
python -c "import json; print(json.load(open('coverage.json'))['totals']['percent_covered'])"
```

**Validation**:
- ✅ All tests passing (107/107)
- ✅ Coverage ≥ 70% (achieved 91%)
- ✅ No critical test failures

#### Step 3: API Keys Validation (5 min)
```bash
# Check config exists
# Validate config structure
python -c "import json; print(json.load(open('config_local.json')))"
```

**Validation**:
- ✅ Config file exists
- ✅ Config structure valid
- ✅ API keys configured (user responsibility)

#### Step 4: Build Executable (10 min)
```bash
# Build with PyInstaller
python build_exe.py

# Verify executable created
# Test executable
```

**Validation**:
- ✅ Executable built successfully
- ✅ Executable size reasonable
- ✅ Executable runs without errors

#### Step 5: Create Installer (5 min)
```bash
# Build NSIS installer
makensis installer.nsi

# Verify installer created
# Test installer (manual)
```

**Validation**:
- ✅ Installer built successfully
- ✅ Installer size reasonable
- ✅ Installer works (manual test)

#### Step 6: Generate Checksums (2 min)
```bash
# SHA256 checksum for executable
Get-FileHash dist\AIPromptGenerator.exe -Algorithm SHA256

# SHA256 checksum for installer
Get-FileHash AIPromptGenerator_Setup_1.0.0.exe -Algorithm SHA256
```

**Output**: `CHECKSUMS.txt`

**Format**:
```
AIPromptGenerator.exe: SHA256 <hash>
AIPromptGenerator_Setup_1.0.0.exe: SHA256 <hash>
```

#### Step 7: Git Finalization (3 min)
```bash
# Create git tag
git tag v1.0.0

# Push tag
git push origin v1.0.0

# Update CHANGELOG.md
# Commit final changes
git commit -m "Release v1.0.0"
git push
```

**Validation**:
- ✅ Git tag created
- ✅ CHANGELOG updated
- ✅ All changes committed

### Release Script Execution

#### PowerShell (Windows)
```powershell
.\release_v1.0.0.ps1
```

#### Bash (Linux/Mac)
```bash
./release_v1.0.0.sh
```

### Release Output

#### Distribution Files
1. **Executable**: `dist/AIPromptGenerator.exe` (~50-100 MB)
2. **Installer**: `AIPromptGenerator_Setup_1.0.0.exe` (~50-100 MB)
3. **Checksums**: `CHECKSUMS.txt`
4. **Source Code**: GitHub repository

#### Documentation
1. **README.md**: Project overview
2. **INSTALLATION.md**: Installation guide
3. **CHANGELOG.md**: Version history
4. **LICENSE**: License information

## Distribution

### Executable Details
- **Name**: `AIPromptGenerator.exe`
- **Size**: ~50-100 MB (estimated)
- **SHA256 Checksum**: Generated în `CHECKSUMS.txt`
- **Requirements**: Windows 10/11, 4GB RAM, 500MB disk

### Installer Details
- **Name**: `AIPromptGenerator_Setup_1.0.0.exe`
- **Size**: ~50-100 MB (estimated)
- **SHA256 Checksum**: Generated în `CHECKSUMS.txt`
- **Install Location**: `C:\Program Files\AIPromptGenerator`
- **Features**: Desktop shortcut, Start Menu entry, Uninstaller

### System Requirements

#### Minimum Requirements
- **OS**: Windows 10/11 (64-bit)
- **RAM**: 4GB
- **Disk Space**: 500MB
- **Internet**: Required for AI API calls

#### Recommended Requirements
- **OS**: Windows 11 (64-bit)
- **RAM**: 8GB+
- **Disk Space**: 1GB+
- **Internet**: Stable connection pentru AI APIs

### Installation Methods

#### Method 1: Standalone Executable (Recommended)
1. Download `AIPromptGenerator.exe`
2. Run executable directly (no installation needed)
3. Configure API keys în `config_local.json`

#### Method 2: NSIS Installer
1. Download `AIPromptGenerator_Setup_1.0.0.exe`
2. Run installer
3. Follow installation wizard
4. Launch from Start Menu or Desktop shortcut

#### Method 3: From Source
1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python main.py`

### Post-Installation

#### First Run
1. Launch application
2. Go to Settings tab
3. Enter API keys pentru AI providers
4. Enable desired providers
5. Configure fallback strategy (optional)

#### Configuration
- **Config File**: `config_local.json` (auto-created)
- **Database**: `data.db` (auto-created)
- **Backups**: `backups/` directory (auto-created)
- **Logs**: Console output (can be redirected)

### Deployment Checklist

#### Pre-Release
- [x] All tests passing (107/107)
- [x] Coverage ≥ 70% (91% achieved)
- [x] Build script working
- [x] Installer script working
- [x] Documentation complete

#### Release
- [x] Executable built
- [x] Installer created
- [x] Checksums generated
- [x] Git tag created
- [x] CHANGELOG updated

#### Post-Release
- [ ] Clean system test pe VM Windows 11 ⚠️ PENDING
- [ ] GitHub release created ⚠️ PENDING
- [ ] Distribution links verified ⚠️ PENDING

---

**Generated**: 2025-10-31  
**Source**: build_exe.py, installer.nsi, release_v1.0.0.ps1, INSTALLATION.md

