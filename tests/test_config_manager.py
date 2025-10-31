"""Tests for ConfigManager."""
import tempfile
from pathlib import Path
from core.config_manager import ConfigManager


def test_config_manager_default():
    """Should create default config if file doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "test_config.json"
        config = ConfigManager(str(config_path))
        
        assert config.get("ai_providers.claude.enabled") is True
        assert config_path.exists()


def test_get_nested_key():
    """Should get nested configuration values."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = ConfigManager(str(Path(tmpdir) / "test_config.json"))
        
        value = config.get("ai_providers.claude.model")
        assert value == "claude-sonnet-4-20250514"


def test_get_default():
    """Should return default for missing key."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = ConfigManager(str(Path(tmpdir) / "test_config.json"))
        
        value = config.get("nonexistent.key", "default")
        assert value == "default"


def test_set_nested_key():
    """Should set nested configuration values."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = ConfigManager(str(Path(tmpdir) / "test_config.json"))
        
        config.set("ai_providers.claude.api_key", "test-key-123")
        assert config.get("ai_providers.claude.api_key") == "test-key-123"


def test_get_all():
    """Should return full configuration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = ConfigManager(str(Path(tmpdir) / "test_config.json"))
        
        all_config = config.get_all()
        assert "ai_providers" in all_config
        assert "database" in all_config


def test_update():
    """Should update configuration with dictionary."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = ConfigManager(str(Path(tmpdir) / "test_config.json"))
        
        config.update({"ui": {"theme": "light", "font_size": 14}})
        assert config.get("ui.theme") == "light"
        assert config.get("ui.font_size") == 14

