"""Context tab for project analysis."""
from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QLineEdit, QFileDialog, QMessageBox, QTreeWidget, QTreeWidgetItem
)
from pathlib import Path
from typing import Optional

from core.context_engine import ContextEngine


class ContextTab(QWidget):
    """Tab for viewing project context."""
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._init_ui()
        self.context_engine: Optional[ContextEngine] = None
    
    def _init_ui(self) -> None:
        """Initialize UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Project Context")
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
        
        analyze_btn = QPushButton("Analyze")
        analyze_btn.clicked.connect(self.analyze_project)
        project_layout.addWidget(analyze_btn)
        
        layout.addLayout(project_layout)
        
        # Split view for structure and context
        split_layout = QHBoxLayout()
        
        # Structure tree
        structure_label = QLabel("Project Structure:")
        structure_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        layout.addWidget(structure_label)
        
        self.structure_tree = QTreeWidget()
        self.structure_tree.setHeaderLabel("Files")
        self.structure_tree.setMaximumWidth(300)
        split_layout.addWidget(self.structure_tree)
        
        # Context display
        context_label = QLabel("Project Context:")
        context_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        layout.addWidget(context_label)
        
        self.context_text = QTextEdit()
        self.context_text.setReadOnly(True)
        self.context_text.setPlaceholderText("Select a project and click Analyze...")
        split_layout.addWidget(self.context_text)
        
        layout.addLayout(split_layout)
        
        # Stats
        stats_label = QLabel("Statistics:")
        stats_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        layout.addWidget(stats_label)
        
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        self.stats_text.setMaximumHeight(100)
        layout.addWidget(self.stats_text)
    
    def browse_project(self) -> None:
        """Browse for project directory."""
        path = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if path:
            self.project_path_input.setText(path)
            self.load_project(path)
    
    def load_project(self, project_path: str) -> None:
        """Load project."""
        try:
            self.context_engine = ContextEngine(project_path)
            self.update_structure()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load project: {e}")
    
    def update_structure(self) -> None:
        """Update structure tree."""
        if not self.context_engine:
            return
        
        self.structure_tree.clear()
        
        try:
            structure = self.context_engine.analyze_project_structure()
            files = structure.get("files", [])
            
            # Add root item
            root = QTreeWidgetItem(self.structure_tree, [Path(self.project_path_input.text()).name])
            root.setExpanded(True)
            
            # Add files (limit to first 50 for performance)
            for file_path in files[:50]:
                parts = file_path.split("/")
                current = root
                
                for part in parts:
                    children = [current.child(i) for i in range(current.childCount())]
                    child = next((c for c in children if c.text(0) == part), None)
                    
                    if not child:
                        child = QTreeWidgetItem(current, [part])
                    
                    current = child
                    
                    if part == parts[-1]:  # File
                        current.setExpanded(False)
        
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to update structure: {e}")
    
    def analyze_project(self) -> None:
        """Analyze project."""
        project_path = self.project_path_input.text()
        
        if not project_path:
            QMessageBox.warning(self, "Warning", "Please select a project first.")
            return
        
        try:
            if not self.context_engine:
                self.load_project(project_path)
            
            if self.context_engine:
                # Generate context
                context = self.context_engine.generate_context_prompt()
                self.context_text.setText(context)
                
                # Get statistics
                structure = self.context_engine.analyze_project_structure()
                stats = f"""Project Statistics:
- Total Files: {structure.get('total_files', 0)}
- Directories: {len(structure.get('directories', []))}
- File Types: {len(structure.get('file_types', {}))}

Top File Types:
{chr(10).join(f"- {ext}: {count} files" for ext, count in sorted(structure.get('file_types', {}).items(), key=lambda x: -x[1])[:10])}
"""
                self.stats_text.setText(stats)
                
                self.update_structure()
        
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to analyze project: {e}")


__all__ = ["ContextTab"]

