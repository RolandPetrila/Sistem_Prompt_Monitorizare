"""Settings tab."""
from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QCheckBox, QSpinBox, QMessageBox, QTabWidget, QFormLayout
)
from typing import Optional

from core.config_manager import ConfigManager


class SettingsTab(QWidget):
    """Tab for application settings."""
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._init_ui()
        self.config_manager = ConfigManager()
    
    def _init_ui(self) -> None:
        """Initialize UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Settings")
        title.setStyleSheet("font-size: 24px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Tab widget for different settings
        settings_tabs = QTabWidget()
        
        # AI Providers tab
        ai_tab = QWidget()
        ai_layout = QFormLayout(ai_tab)
        
        # Claude settings
        self.claude_key_input = QLineEdit()
        self.claude_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.claude_key_input.setText(self.config_manager.get("ai_providers.claude.api_key", ""))
        ai_layout.addRow("Claude API Key:", self.claude_key_input)
        
        self.claude_enabled = QCheckBox()
        self.claude_enabled.setChecked(self.config_manager.get("ai_providers.claude.enabled", True))
        ai_layout.addRow("Claude Enabled:", self.claude_enabled)
        
        # OpenAI settings
        self.openai_key_input = QLineEdit()
        self.openai_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.openai_key_input.setText(self.config_manager.get("ai_providers.openai.api_key", ""))
        ai_layout.addRow("OpenAI API Key:", self.openai_key_input)
        
        self.openai_enabled = QCheckBox()
        self.openai_enabled.setChecked(self.config_manager.get("ai_providers.openai.enabled", True))
        ai_layout.addRow("OpenAI Enabled:", self.openai_enabled)
        
        # Gemini settings
        self.gemini_key_input = QLineEdit()
        self.gemini_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.gemini_key_input.setText(self.config_manager.get("ai_providers.gemini.api_key", ""))
        ai_layout.addRow("Gemini API Key:", self.gemini_key_input)
        
        self.gemini_enabled = QCheckBox()
        self.gemini_enabled.setChecked(self.config_manager.get("ai_providers.gemini.enabled", True))
        ai_layout.addRow("Gemini Enabled:", self.gemini_enabled)
        
        settings_tabs.addTab(ai_tab, "AI Providers")
        
        # Fallback settings
        fallback_tab = QWidget()
        fallback_layout = QFormLayout(fallback_tab)
        
        self.fallback_enabled = QCheckBox()
        self.fallback_enabled.setChecked(self.config_manager.get("fallback_strategy.enabled", True))
        fallback_layout.addRow("Fallback Enabled:", self.fallback_enabled)
        
        self.retry_count = QSpinBox()
        self.retry_count.setMinimum(1)
        self.retry_count.setMaximum(10)
        self.retry_count.setValue(self.config_manager.get("fallback_strategy.retry_count", 3))
        fallback_layout.addRow("Retry Count:", self.retry_count)
        
        self.timeout = QSpinBox()
        self.timeout.setMinimum(5)
        self.timeout.setMaximum(300)
        self.timeout.setValue(self.config_manager.get("fallback_strategy.timeout", 30))
        fallback_layout.addRow("Timeout (seconds):", self.timeout)
        
        settings_tabs.addTab(fallback_tab, "Fallback Strategy")
        
        layout.addWidget(settings_tabs)
        
        # Save button
        save_btn = QPushButton("Save Settings")
        save_btn.setStyleSheet("padding: 10px; font-size: 14px; background: #4CAF50; color: white;")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
    
    def save_settings(self) -> None:
        """Save settings."""
        try:
            # Save AI provider settings
            self.config_manager.set("ai_providers.claude.api_key", self.claude_key_input.text())
            self.config_manager.set("ai_providers.claude.enabled", self.claude_enabled.isChecked())
            
            self.config_manager.set("ai_providers.openai.api_key", self.openai_key_input.text())
            self.config_manager.set("ai_providers.openai.enabled", self.openai_enabled.isChecked())
            
            self.config_manager.set("ai_providers.gemini.api_key", self.gemini_key_input.text())
            self.config_manager.set("ai_providers.gemini.enabled", self.gemini_enabled.isChecked())
            
            # Save fallback settings
            self.config_manager.set("fallback_strategy.enabled", self.fallback_enabled.isChecked())
            self.config_manager.set("fallback_strategy.retry_count", self.retry_count.value())
            self.config_manager.set("fallback_strategy.timeout", self.timeout.value())
            
            QMessageBox.information(self, "Success", "Settings saved successfully!")
        
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save settings: {e}")


__all__ = ["SettingsTab"]

