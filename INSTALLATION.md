# Installation Guide

## AI Prompt Generator Ultimate - Installation Instructions

### Requirements
- Python 3.10 or higher
- Windows 10/11 (for executable)
- API keys for AI providers (Claude, OpenAI, or Gemini)

### Installation Methods

#### Method 1: Standalone Executable (Recommended)
1. Download `AIPromptGenerator_Setup_1.0.0.exe`
2. Run the installer
3. Follow the installation wizard
4. Launch from Start Menu or Desktop shortcut

#### Method 2: From Source
1. Clone or download the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure API keys in `config_local.json`
4. Run the application:
   ```bash
   python main.py
   ```

#### Method 3: Build from Source
1. Follow Method 2 steps
2. Build executable:
   ```bash
   python build_exe.py
   ```
3. Or use build script:
   ```bash
   build.bat
   ```

### Configuration

#### API Keys Setup
1. Edit `config_local.json`
2. Add your API keys:
   ```json
   {
     "ai_providers": {
       "claude": {
         "api_key": "your-claude-key",
         "enabled": true
       },
       "openai": {
         "api_key": "your-openai-key",
         "enabled": true
       }
     }
   }
   ```
3. Or use the Settings tab in the GUI

### First Run
1. Launch the application
2. Go to Settings tab
3. Enter your API keys
4. Select a project in Prompt Generator tab
5. Start generating prompts!

### Troubleshooting

**Issue: Application won't start**
- Check Python version: `python --version`
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

**Issue: AI requests fail**
- Verify API keys in Settings tab
- Check internet connection
- Ensure API keys are valid and have credits

**Issue: Build fails**
- Install PyInstaller: `pip install pyinstaller`
- Check PySide6 installation: `pip install PySide6`

### Support
For issues or questions, check the README.md or open an issue on GitHub.

