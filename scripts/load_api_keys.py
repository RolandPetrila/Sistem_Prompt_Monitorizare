"""
Loads API keys from Excel/DOCX into secure config.
Supports: Claude, ChatGPT, Gemini, Perplexity, GitHub Copilot, Cursor
"""
import json
from pathlib import Path


def load_api_keys():
    """
    Load API keys from api_keys.xlsx or api_keys.docx.
    IMPORTANT: Acest script citește keys MANUAL din fișiere.
    
    Returns:
        dict: API keys configuration
    """
    # TEMPORAR: Hardcoded structure - replace după citire fișiere
    config = {
        "ai_providers": {
            "claude": {
                "api_key": "PLACEHOLDER_CLAUDE_KEY",
                "model": "claude-sonnet-4-20250514",
                "priority": 1,
                "enabled": True
            },
            "openai": {
                "api_key": "PLACEHOLDER_OPENAI_KEY", 
                "model": "gpt-4-turbo-preview",
                "priority": 2,
                "enabled": True
            },
            "gemini": {
                "api_key": "PLACEHOLDER_GEMINI_KEY",
                "model": "gemini-1.5-pro",
                "priority": 3,
                "enabled": True
            },
            "perplexity": {
                "api_key": "PLACEHOLDER_PERPLEXITY_KEY",
                "base_url": "https://api.perplexity.ai",
                "priority": 4,
                "enabled": True
            }
        },
        "fallback_strategy": {
            "enabled": True,
            "retry_count": 3,
            "timeout": 30,
            "auto_switch": True
        },
        "fine_tuning": {
            "enabled": True,
            "learning_rate": 0.001,
            "history_size": 100,
            "optimization_threshold": 0.7
        }
    }
    
    # TODO: Implementare citire din api_keys.xlsx
    # import pandas as pd
    # df = pd.read_excel("api_keys.xlsx")
    # for _, row in df.iterrows():
    #     provider = row["Provider"].lower()
    #     config["ai_providers"][provider]["api_key"] = row["API_Key"]
    
    # Salvează config
    config_path = Path("config_local.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ API keys configuration created")
    print("⚠️  IMPORTANT: Edit config_local.json cu API keys reale!")
    
    return config


if __name__ == "__main__":
    load_api_keys()

