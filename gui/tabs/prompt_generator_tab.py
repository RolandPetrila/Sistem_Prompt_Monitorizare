"""Prompt generator tab."""
from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QComboBox, QLineEdit, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from pathlib import Path
from typing import Optional

from core.ai_orchestrator import AIOrchestrator
from core.context_engine import ContextEngine
from core.next_prompt_generator import NextPromptGenerator, TaskType
from core.database import Database


class PromptGeneratorTab(QWidget):
    """Tab for generating AI prompts."""
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._init_ui()
        self.orchestrator = AIOrchestrator()
        self.prompt_generator = NextPromptGenerator()
        self.db = Database()
        self.current_project_path: Optional[str] = None
        self.current_project_id: Optional[int] = None
    
    def _init_ui(self) -> None:
        """Initialize UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Prompt Generator")
        title.setStyleSheet("font-size: 24px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Project selection
        project_layout = QHBoxLayout()
        project_layout.addWidget(QLabel("Project Path:"))
        
        self.project_path_input = QLineEdit()
        self.project_path_input.setPlaceholderText("Select project directory...")
        project_layout.addWidget(self.project_path_input)
        
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_project)
        project_layout.addWidget(browse_btn)
        
        layout.addLayout(project_layout)
        
        # Task type selection
        task_layout = QHBoxLayout()
        task_layout.addWidget(QLabel("Task Type:"))
        
        self.task_type_combo = QComboBox()
        self.task_type_combo.addItems([
            "Code Quality",
            "Bug Fix",
            "Performance Optimization",
            "Security Audit",
            "Test Generation",
            "Refactoring",
            "Documentation",
            "Architecture Review"
        ])
        task_layout.addWidget(self.task_type_combo)
        
        layout.addLayout(task_layout)
        
        # Context display
        context_label = QLabel("Project Context:")
        context_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        layout.addWidget(context_label)
        
        self.context_text = QTextEdit()
        self.context_text.setReadOnly(True)
        self.context_text.setMaximumHeight(150)
        self.context_text.setPlaceholderText("Select a project to view context")
        layout.addWidget(self.context_text)
        
        # Generate button
        generate_btn = QPushButton("Generate Prompt")
        generate_btn.setStyleSheet("padding: 10px; font-size: 14px;")
        generate_btn.clicked.connect(self.generate_prompt)
        layout.addWidget(generate_btn)
        
        # Generated prompt
        prompt_label = QLabel("Generated Prompt:")
        prompt_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        layout.addWidget(prompt_label)
        
        self.prompt_text = QTextEdit()
        self.prompt_text.setPlaceholderText("Generated prompt will appear here...")
        layout.addWidget(self.prompt_text)
        
        # Send to AI button
        send_layout = QHBoxLayout()
        send_ai_btn = QPushButton("Send to AI")
        send_ai_btn.setStyleSheet("padding: 10px; font-size: 14px; background: #4CAF50; color: white;")
        send_ai_btn.clicked.connect(self.send_to_ai)
        send_layout.addWidget(send_ai_btn)
        
        copy_btn = QPushButton("Copy Prompt")
        copy_btn.clicked.connect(self.copy_prompt)
        send_layout.addWidget(copy_btn)
        
        layout.addLayout(send_layout)
        
        # AI Response
        response_label = QLabel("AI Response:")
        response_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        layout.addWidget(response_label)
        
        self.response_text = QTextEdit()
        self.response_text.setReadOnly(True)
        self.response_text.setPlaceholderText("AI response will appear here...")
        layout.addWidget(self.response_text)
    
    def browse_project(self) -> None:
        """Browse for project directory."""
        path = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if path:
            self.project_path_input.setText(path)
            self.current_project_path = path
            self.load_project_context()
    
    def load_project_context(self) -> None:
        """Load project context."""
        if not self.current_project_path:
            return
        
        try:
            context_engine = ContextEngine(self.current_project_path)
            context = context_engine.generate_context_prompt()
            self.context_text.setText(context)
            
            # Add project to database
            project = self.db.get_project(self.current_project_path)
            if project:
                self.current_project_id = project["id"]
            else:
                self.current_project_id = self.db.add_project(
                    self.current_project_path,
                    Path(self.current_project_path).name
                )
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load project context: {e}")
    
    def generate_prompt(self) -> None:
        """Generate prompt."""
        if not self.current_project_path:
            QMessageBox.warning(self, "Warning", "Please select a project first.")
            return
        
        try:
            # Get task type
            task_type_map = {
                "Code Quality": TaskType.CODE_QUALITY,
                "Bug Fix": TaskType.BUG_FIX,
                "Performance Optimization": TaskType.OPTIMIZATION,
                "Security Audit": TaskType.SECURITY,
                "Test Generation": TaskType.TESTING,
                "Refactoring": TaskType.REFACTORING,
                "Documentation": TaskType.DOCUMENTATION,
                "Architecture Review": TaskType.GENERAL
            }
            
            selected_task = self.task_type_combo.currentText()
            task_type = task_type_map.get(selected_task, TaskType.GENERAL)
            
            # Generate context
            context_engine = ContextEngine(self.current_project_path)
            context = context_engine.generate_context_prompt()
            
            # Generate prompt
            prompt = self.prompt_generator.generate_custom_prompt(task_type, context)
            self.prompt_text.setText(prompt)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to generate prompt: {e}")
    
    def send_to_ai(self) -> None:
        """Send prompt to AI."""
        prompt = self.prompt_text.toPlainText()
        if not prompt:
            QMessageBox.warning(self, "Warning", "No prompt to send.")
            return
        
        try:
            self.response_text.setText("Sending to AI...")
            
            response = self.orchestrator.generate_completion(prompt)
            
            if response.success:
                self.response_text.setText(response.content)
                
                # Save to database
                if self.current_project_id:
                    task_type = self.task_type_combo.currentText().lower().replace(" ", "_")
                    self.db.add_prompt(self.current_project_id, task_type, prompt)
            else:
                self.response_text.setText(f"Error: {response.error}")
                QMessageBox.warning(self, "Error", f"AI request failed: {response.error}")
        
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to send to AI: {e}")
            self.response_text.setText(f"Error: {e}")
    
    def copy_prompt(self) -> None:
        """Copy prompt to clipboard."""
        prompt = self.prompt_text.toPlainText()
        if prompt:
            from PySide6.QtGui import QClipboard
            clipboard = QClipboard()
            clipboard.setText(prompt)
            QMessageBox.information(self, "Copied", "Prompt copied to clipboard!")


__all__ = ["PromptGeneratorTab"]

