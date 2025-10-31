"""Configuration manager for application settings."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigManager:
    """
    Manages application configuration with validation.
    
    Example:
        >>> config = ConfigManager()
        >>> api_key = config.get("ai_providers.claude.api_key")
    """
    
    def __init__(self, config_path: str = "config_local.json") -> None:
        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from file."""
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                self._config = json.load(f)
        else:
            self._config = self._default_config()
            self._save_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            "ai_providers": {
                "claude": {
                    "api_key": "",
                    "model": "claude-sonnet-4-20250514",
                    "priority": 1,
                    "enabled": True
                },
                "openai": {
                    "api_key": "",
                    "model": "gpt-4-turbo-preview",
                    "priority": 2,
                    "enabled": True
                },
                "gemini": {
                    "api_key": "",
                    "model": "gemini-1.5-pro",
                    "priority": 3,
                    "enabled": True
                }
            },
            "fallback_strategy": {
                "enabled": True,
                "retry_count": 3,
                "timeout": 30
            },
            "database": {
                "path": "data.db"
            },
            "ui": {
                "theme": "dark",
                "font_size": 12
            }
        }
    
    def _save_config(self) -> None:
        """Save configuration to file."""
        with open(self.config_path, "w") as f:
            json.dump(self._config, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-separated path.
        
        Args:
            key: Dot-separated path (e.g., "ai_providers.claude.api_key")
            default: Default value if key not found
        
        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value by dot-separated path.
        
        Args:
            key: Dot-separated path
            value: Value to set
        """
        keys = key.split(".")
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self._save_config()
    
    def get_all(self) -> Dict[str, Any]:
        """Get full configuration."""
        return self._config.copy()
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Update configuration with dictionary."""
        self._config.update(updates)
        self._save_config()


__all__ = ["ConfigManager"]

