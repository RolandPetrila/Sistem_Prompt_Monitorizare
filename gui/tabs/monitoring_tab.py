"""Monitoring tab for file watching."""
from __future__ import annotations

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QHBoxLayout, QCheckBox, QLineEdit
from PySide6.QtCore import QTimer
from typing import Optional

from core.change_detector import ChangeDetector
from pathlib import Path


class MonitoringTab(QWidget):
    """Tab for monitoring file changes."""
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._init_ui()
        self.change_detector: Optional[ChangeDetector] = None
        self.monitoring_active = False
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.check_changes)
        self.monitor_timer.setInterval(2000)  # Check every 2 seconds
    
    def _init_ui(self) -> None:
        """Initialize UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("File Monitoring")
        title.setStyleSheet("font-size: 24px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Project selection
        project_layout = QHBoxLayout()
        project_layout.addWidget(QLabel("Project Path:"))
        
        self.project_path_input = QLineEdit()
        self.project_path_input.setPlaceholderText("Select project directory to monitor...")
        project_layout.addWidget(self.project_path_input)
        
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_project)
        project_layout.addWidget(browse_btn)
        
        layout.addLayout(project_layout)
        
        # Monitoring controls
        controls_layout = QHBoxLayout()
        
        self.monitor_checkbox = QCheckBox("Enable Monitoring")
        self.monitor_checkbox.toggled.connect(self.toggle_monitoring)
        controls_layout.addWidget(self.monitor_checkbox)
        
        refresh_btn = QPushButton("Refresh Now")
        refresh_btn.clicked.connect(self.check_changes)
        controls_layout.addWidget(refresh_btn)
        
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_log)
        controls_layout.addWidget(clear_btn)
        
        layout.addLayout(controls_layout)
        
        # Status
        self.status_label = QLabel("Status: Not monitoring")
        self.status_label.setStyleSheet("padding: 5px; background: #f0f0f0; border-radius: 3px;")
        layout.addWidget(self.status_label)
        
        # Changes log
        log_label = QLabel("File Changes:")
        log_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        layout.addWidget(log_label)
        
        self.changes_text = QTextEdit()
        self.changes_text.setReadOnly(True)
        self.changes_text.setPlaceholderText("File changes will appear here...")
        layout.addWidget(self.changes_text)
    
    def browse_project(self) -> None:
        """Browse for project directory."""
        from PySide6.QtWidgets import QFileDialog
        
        path = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if path:
            self.project_path_input.setText(path)
            self.setup_monitoring(path)
    
    def setup_monitoring(self, project_path: str) -> None:
        """Setup file monitoring."""
        try:
            state_file = Path(project_path) / ".change_state.json"
            self.change_detector = ChangeDetector(project_path, str(state_file))
            self.status_label.setText(f"Status: Monitoring {Path(project_path).name}")
            self.status_label.setStyleSheet("padding: 5px; background: #e8f5e9; border-radius: 3px;")
        except Exception as e:
            self.status_label.setText(f"Status: Error - {e}")
            self.status_label.setStyleSheet("padding: 5px; background: #ffebee; border-radius: 3px;")
    
    def toggle_monitoring(self, enabled: bool) -> None:
        """Toggle monitoring on/off."""
        if not self.project_path_input.text():
            self.monitor_checkbox.setChecked(False)
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Warning", "Please select a project first.")
            return
        
        if enabled:
            if not self.change_detector:
                self.setup_monitoring(self.project_path_input.text())
            self.monitoring_active = True
            self.monitor_timer.start()
            self.status_label.setText("Status: Monitoring (Active)")
            self.status_label.setStyleSheet("padding: 5px; background: #c8e6c9; border-radius: 3px;")
        else:
            self.monitoring_active = False
            self.monitor_timer.stop()
            self.status_label.setText("Status: Monitoring (Paused)")
            self.status_label.setStyleSheet("padding: 5px; background: #fff9c4; border-radius: 3px;")
    
    def check_changes(self) -> None:
        """Check for file changes."""
        if not self.change_detector:
            return
        
        try:
            changes = self.change_detector.detect_changes()
            
            if changes["modified"] or changes["added"] or changes["deleted"]:
                log_entry = f"[{self.monitor_timer.interval() / 1000}s] Changes detected:\n"
                
                if changes["modified"]:
                    log_entry += f"Modified: {', '.join(changes['modified'][:10])}\n"
                if changes["added"]:
                    log_entry += f"Added: {', '.join(changes['added'][:10])}\n"
                if changes["deleted"]:
                    log_entry += f"Deleted: {', '.join(changes['deleted'][:10])}\n"
                
                self.changes_text.append(log_entry)
        
        except Exception as e:
            self.changes_text.append(f"Error checking changes: {e}")
    
    def clear_log(self) -> None:
        """Clear changes log."""
        self.changes_text.clear()


__all__ = ["MonitoringTab"]

