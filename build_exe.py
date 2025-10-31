"""Build executable using PyInstaller."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def build_exe() -> int:
    """Build executable using PyInstaller."""
    print("[BUILD] Building executable with PyInstaller...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name=AIPromptGenerator",
        "--windowed",
        "--onefile",
        "--icon=NONE",  # Add icon if available
        "--add-data=config;config",
        "--hidden-import=PySide6",
        "--hidden-import=anthropic",
        "--hidden-import=openai",
        "--hidden-import=google.generativeai",
        "--hidden-import=tree_sitter",
        "main.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("[OK] Build successful!")
        print(f"[INFO] Executable location: dist/AIPromptGenerator.exe")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return 1
    except FileNotFoundError:
        print("[ERROR] PyInstaller not found. Install it with: pip install pyinstaller")
        return 1


if __name__ == "__main__":
    sys.exit(build_exe())

