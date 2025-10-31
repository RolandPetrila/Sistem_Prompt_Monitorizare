"""Main application window."""
from __future__ import annotations

from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from typing import Optional

from gui.tabs.dashboard_tab import DashboardTab
from gui.tabs.prompt_generator_tab import PromptGeneratorTab
from gui.tabs.monitoring_tab import MonitoringTab
from gui.tabs.settings_tab import SettingsTab
from gui.tabs.backup_tab import BackupTab
from gui.tabs.incremental_tab import IncrementalTab
from gui.tabs.context_tab import ContextTab


class MainWindow(QMainWindow):
    """Main application window with tabbed interface."""
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("AI Prompt Generator Ultimate")
        self.setMinimumSize(1200, 800)
        
        # Create central widget with tabs
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Create layout
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        
        # Add tabs
        self.dashboard_tab = DashboardTab()
        self.tab_widget.addTab(self.dashboard_tab, "Dashboard")
        
        self.prompt_generator_tab = PromptGeneratorTab()
        self.tab_widget.addTab(self.prompt_generator_tab, "Prompt Generator")
        
        self.monitoring_tab = MonitoringTab()
        self.tab_widget.addTab(self.monitoring_tab, "Monitoring")
        
        self.context_tab = ContextTab()
        self.tab_widget.addTab(self.context_tab, "Context")
        
        self.backup_tab = BackupTab()
        self.tab_widget.addTab(self.backup_tab, "Backup")
        
        self.incremental_tab = IncrementalTab()
        self.tab_widget.addTab(self.incremental_tab, "Incremental")
        
        self.settings_tab = SettingsTab()
        self.tab_widget.addTab(self.settings_tab, "Settings")
        
        layout.addWidget(self.tab_widget)


__all__ = ["MainWindow"]

