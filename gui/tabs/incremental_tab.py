"""Incremental workflow tab."""
from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QLineEdit, QFileDialog, QMessageBox, QTextEdit, QComboBox
)
from pathlib import Path
from typing import Optional

from core.incremental_workflow import IncrementalWorkflow


class IncrementalTab(QWidget):
    """Tab for incremental workflow."""
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._init_ui()
        self.workflow: Optional[IncrementalWorkflow] = None
    
    def _init_ui(self) -> None:
        """Initialize UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Incremental Workflow")
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
        
        # New iteration
        iteration_layout = QHBoxLayout()
        iteration_layout.addWidget(QLabel("Task:"))
        
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter task description...")
        iteration_layout.addWidget(self.task_input)
        
        create_btn = QPushButton("Create Iteration")
        create_btn.setStyleSheet("padding: 10px; background: #4CAF50; color: white;")
        create_btn.clicked.connect(self.create_iteration)
        iteration_layout.addWidget(create_btn)
        
        layout.addLayout(iteration_layout)
        
        # Progress stats
        self.progress_label = QLabel("Progress: No workflow active")
        self.progress_label.setStyleSheet("padding: 5px; background: #f0f0f0; border-radius: 3px;")
        layout.addWidget(self.progress_label)
        
        # Iterations list
        list_label = QLabel("Iterations:")
        list_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        layout.addWidget(list_label)
        
        self.iterations_list = QListWidget()
        layout.addWidget(self.iterations_list)
        
        # Iteration controls
        controls_layout = QHBoxLayout()
        
        complete_btn = QPushButton("Mark Complete")
        complete_btn.setStyleSheet("padding: 10px; background: #2196F3; color: white;")
        complete_btn.clicked.connect(self.complete_iteration)
        controls_layout.addWidget(complete_btn)
        
        fail_btn = QPushButton("Mark Failed")
        fail_btn.setStyleSheet("padding: 10px; background: #f44336; color: white;")
        fail_btn.clicked.connect(self.fail_iteration)
        controls_layout.addWidget(fail_btn)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_iterations)
        controls_layout.addWidget(refresh_btn)
        
        layout.addLayout(controls_layout)
        
        # Details
        details_label = QLabel("Iteration Details:")
        details_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        layout.addWidget(details_label)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setMaximumHeight(150)
        layout.addWidget(self.details_text)
        
        self.iterations_list.itemSelectionChanged.connect(self.show_details)
    
    def browse_project(self) -> None:
        """Browse for project directory."""
        path = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if path:
            self.project_path_input.setText(path)
            self.load_workflow(path)
    
    def load_workflow(self, project_path: str) -> None:
        """Load workflow for project."""
        try:
            workflow_file = Path(project_path) / ".workflow.json"
            self.workflow = IncrementalWorkflow(project_path, str(workflow_file))
            self.refresh_iterations()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load workflow: {e}")
    
    def create_iteration(self) -> None:
        """Create new iteration."""
        project_path = self.project_path_input.text()
        task = self.task_input.text()
        
        if not project_path:
            QMessageBox.warning(self, "Warning", "Please select a project first.")
            return
        
        if not task:
            QMessageBox.warning(self, "Warning", "Please enter a task description.")
            return
        
        if not self.workflow:
            self.load_workflow(project_path)
        
        try:
            if self.workflow:
                iteration_id = self.workflow.create_iteration(task)
                QMessageBox.information(self, "Success", f"Iteration created: {iteration_id}")
                self.task_input.clear()
                self.refresh_iterations()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to create iteration: {e}")
    
    def refresh_iterations(self) -> None:
        """Refresh iterations list."""
        if not self.workflow:
            return
        
        self.iterations_list.clear()
        
        try:
            iterations = self.workflow.list_iterations()
            
            for iteration in iterations:
                status = iteration.status
                task = iteration.task[:50] + "..." if len(iteration.task) > 50 else iteration.task
                item_text = f"[{status.upper()}] {task}"
                
                item = QListWidgetItem(item_text)
                item.setData(QListWidgetItem.ItemDataRole.UserRole, iteration.iteration_id)
                self.iterations_list.addItem(item)
            
            # Update progress
            progress = self.workflow.get_progress()
            self.progress_label.setText(
                f"Progress: {progress['completed']}/{progress['total']} completed "
                f"({progress['completion_rate']*100:.1f}%)"
            )
        
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to list iterations: {e}")
    
    def show_details(self) -> None:
        """Show iteration details."""
        selected = self.iterations_list.currentItem()
        if not selected:
            return
        
        iteration_id = selected.data(QListWidgetItem.ItemDataRole.UserRole)
        
        if not self.workflow or not iteration_id:
            return
        
        try:
            iteration = self.workflow.get_iteration(iteration_id)
            if iteration:
                details = f"""Iteration ID: {iteration.iteration_id}
Task: {iteration.task}
Status: {iteration.status}
Started: {iteration.started_at}
Ended: {iteration.ended_at or 'N/A'}
Result: {iteration.result or 'N/A'}
"""
                self.details_text.setText(details)
        except Exception as e:
            self.details_text.setText(f"Error loading details: {e}")
    
    def complete_iteration(self) -> None:
        """Mark iteration as complete."""
        selected = self.iterations_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Warning", "Please select an iteration.")
            return
        
        iteration_id = selected.data(QListWidgetItem.ItemDataRole.UserRole)
        
        try:
            if self.workflow:
                self.workflow.complete_iteration(iteration_id, {"status": "completed"}, "Completed")
                QMessageBox.information(self, "Success", "Iteration marked as complete.")
                self.refresh_iterations()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to complete iteration: {e}")
    
    def fail_iteration(self) -> None:
        """Mark iteration as failed."""
        selected = self.iterations_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Warning", "Please select an iteration.")
            return
        
        iteration_id = selected.data(QListWidgetItem.ItemDataRole.UserRole)
        
        try:
            if self.workflow:
                self.workflow.fail_iteration(iteration_id, "User marked as failed")
                QMessageBox.information(self, "Success", "Iteration marked as failed.")
                self.refresh_iterations()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to fail iteration: {e}")


__all__ = ["IncrementalTab"]

