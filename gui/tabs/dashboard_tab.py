"""Dashboard tab showing overview."""
from __future__ import annotations

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QHBoxLayout
from PySide6.QtCore import Qt
from typing import Optional

from core.database import Database
from core.ai_orchestrator import AIOrchestrator


class DashboardTab(QWidget):
    """Dashboard tab with project overview."""
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._init_ui()
        self.db = Database()
        self.orchestrator = AIOrchestrator()
    
    def _init_ui(self) -> None:
        """Initialize UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Stats section
        stats_layout = QHBoxLayout()
        
        self.projects_label = QLabel("Projects: 0")
        self.projects_label.setStyleSheet("padding: 10px; background: #f0f0f0; border-radius: 5px;")
        stats_layout.addWidget(self.projects_label)
        
        self.prompts_label = QLabel("Prompts Generated: 0")
        self.prompts_label.setStyleSheet("padding: 10px; background: #f0f0f0; border-radius: 5px;")
        stats_layout.addWidget(self.prompts_label)
        
        self.ai_calls_label = QLabel("AI Calls: 0")
        self.ai_calls_label.setStyleSheet("padding: 10px; background: #f0f0f0; border-radius: 5px;")
        stats_layout.addWidget(self.ai_calls_label)
        
        layout.addLayout(stats_layout)
        
        # Recent activity
        activity_label = QLabel("Recent Activity")
        activity_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(activity_label)
        
        self.activity_text = QTextEdit()
        self.activity_text.setReadOnly(True)
        self.activity_text.setPlaceholderText("No recent activity")
        layout.addWidget(self.activity_text)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_stats)
        layout.addWidget(refresh_btn)
        
        # Load initial stats
        self.refresh_stats()
    
    def refresh_stats(self) -> None:
        """Refresh dashboard statistics."""
        # Get stats from database
        # This is a placeholder - would need actual project tracking
        
        stats_text = "AI Prompt Generator Dashboard\n\n"
        stats_text += "Ready to generate prompts!\n\n"
        
        usage_stats = self.orchestrator.get_usage_stats()
        if usage_stats:
            stats_text += "AI Usage Statistics:\n"
            for provider, stats in usage_stats.items():
                stats_text += f"- {provider}: {stats.get('calls', 0)} calls\n"
        else:
            stats_text += "No AI calls yet."
        
        self.activity_text.setText(stats_text)
        
        # Update labels (placeholder values)
        self.projects_label.setText("Projects: -")
        self.prompts_label.setText("Prompts Generated: -")
        total_calls = sum(s.get('calls', 0) for s in usage_stats.values()) if usage_stats else 0
        self.ai_calls_label.setText(f"AI Calls: {total_calls}")


__all__ = ["DashboardTab"]

