"""Backup tab for snapshots."""
from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QLineEdit, QFileDialog, QMessageBox, QTextEdit
)
from pathlib import Path
from typing import Optional

from core.backup_manager import BackupManager


class BackupTab(QWidget):
    """Tab for managing backups."""
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._init_ui()
        self.backup_manager: Optional[BackupManager] = None
    
    def _init_ui(self) -> None:
        """Initialize UI."""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Backup Manager")
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
        
        # Backup controls
        controls_layout = QHBoxLayout()
        
        create_btn = QPushButton("Create Snapshot")
        create_btn.setStyleSheet("padding: 10px; background: #4CAF50; color: white;")
        create_btn.clicked.connect(self.create_snapshot)
        controls_layout.addWidget(create_btn)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_snapshots)
        controls_layout.addWidget(refresh_btn)
        
        delete_btn = QPushButton("Delete Selected")
        delete_btn.setStyleSheet("padding: 10px; background: #f44336; color: white;")
        delete_btn.clicked.connect(self.delete_snapshot)
        controls_layout.addWidget(delete_btn)
        
        cleanup_btn = QPushButton("Cleanup Old")
        cleanup_btn.clicked.connect(self.cleanup_snapshots)
        controls_layout.addWidget(cleanup_btn)
        
        layout.addLayout(controls_layout)
        
        # Snapshots list
        list_label = QLabel("Snapshots:")
        list_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        layout.addWidget(list_label)
        
        self.snapshots_list = QListWidget()
        self.snapshots_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        layout.addWidget(self.snapshots_list)
        
        # Snapshot details
        details_label = QLabel("Snapshot Details:")
        details_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        layout.addWidget(details_label)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setMaximumHeight(150)
        layout.addWidget(self.details_text)
        
        self.snapshots_list.itemSelectionChanged.connect(self.show_details)
        
        # Load initial snapshots
        self.setup_backup_manager()
        self.refresh_snapshots()
    
    def browse_project(self) -> None:
        """Browse for project directory."""
        path = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if path:
            self.project_path_input.setText(path)
    
    def setup_backup_manager(self) -> None:
        """Setup backup manager."""
        backup_dir = Path("backups")
        self.backup_manager = BackupManager(str(backup_dir))
    
    def create_snapshot(self) -> None:
        """Create snapshot."""
        project_path = self.project_path_input.text()
        
        if not project_path:
            QMessageBox.warning(self, "Warning", "Please select a project first.")
            return
        
        if not self.backup_manager:
            self.setup_backup_manager()
        
        try:
            snapshot_id = self.backup_manager.create_snapshot(project_path)
            QMessageBox.information(self, "Success", f"Snapshot created: {snapshot_id}")
            self.refresh_snapshots()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to create snapshot: {e}")
    
    def refresh_snapshots(self) -> None:
        """Refresh snapshots list."""
        if not self.backup_manager:
            self.setup_backup_manager()
        
        self.snapshots_list.clear()
        
        try:
            snapshots = self.backup_manager.list_snapshots()
            
            for snapshot in snapshots:
                snapshot_id = snapshot.get("snapshot_id", "Unknown")
                created_at = snapshot.get("created_at", "Unknown")
                item_text = f"{snapshot_id} - {created_at}"
                
                item = QListWidgetItem(item_text)
                item.setData(QListWidgetItem.ItemDataRole.UserRole, snapshot_id)
                self.snapshots_list.addItem(item)
        
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to list snapshots: {e}")
    
    def show_details(self) -> None:
        """Show snapshot details."""
        selected = self.snapshots_list.currentItem()
        if not selected:
            return
        
        snapshot_id = selected.data(QListWidgetItem.ItemDataRole.UserRole)
        
        if not self.backup_manager or not snapshot_id:
            return
        
        try:
            snapshot = self.backup_manager.get_snapshot(snapshot_id)
            if snapshot:
                details = f"""Snapshot ID: {snapshot.get('snapshot_id', 'N/A')}
Project: {Path(snapshot.get('project_path', 'N/A')).name}
Created: {snapshot.get('created_at', 'N/A')}
Files: {len(snapshot.get('files', []))} files
"""
                self.details_text.setText(details)
        except Exception as e:
            self.details_text.setText(f"Error loading details: {e}")
    
    def delete_snapshot(self) -> None:
        """Delete selected snapshot."""
        selected = self.snapshots_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Warning", "Please select a snapshot to delete.")
            return
        
        snapshot_id = selected.data(QListWidgetItem.ItemDataRole.UserRole)
        
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Delete snapshot {snapshot_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if self.backup_manager:
                    self.backup_manager.delete_snapshot(snapshot_id)
                    QMessageBox.information(self, "Success", "Snapshot deleted.")
                    self.refresh_snapshots()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete snapshot: {e}")
    
    def cleanup_snapshots(self) -> None:
        """Cleanup old snapshots."""
        if not self.backup_manager:
            return
        
        reply = QMessageBox.question(
            self,
            "Confirm Cleanup",
            "Delete old snapshots (keep only 10 most recent)?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                deleted = self.backup_manager.cleanup_old_snapshots(keep_count=10)
                QMessageBox.information(self, "Success", f"Deleted {deleted} old snapshots.")
                self.refresh_snapshots()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to cleanup snapshots: {e}")


__all__ = ["BackupTab"]

