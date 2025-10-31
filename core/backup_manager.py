"""Backup manager for project snapshots."""
from __future__ import annotations

import json
import shutil
import tarfile
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any


class BackupManager:
    """
    Manages project backups and snapshots.
    
    Features:
    - Create snapshots
    - Restore from snapshots
    - List snapshots
    - Cleanup old snapshots
    """
    
    def __init__(self, backup_dir: str = "backups") -> None:
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def create_snapshot(self, project_path: str, snapshot_id: Optional[str] = None) -> str:
        """
        Create project snapshot.
        
        Args:
            project_path: Path to project
            snapshot_id: Optional snapshot ID (auto-generated if None)
        
        Returns:
            Snapshot ID
        """
        project_path = Path(project_path)
        
        if not project_path.exists():
            raise ValueError(f"Project path does not exist: {project_path}")
        
        if snapshot_id is None:
            # Use microseconds for uniqueness
            snapshot_id = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        snapshot_dir = self.backup_dir / snapshot_id
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        
        # Create metadata
        metadata = {
            "snapshot_id": snapshot_id,
            "project_path": str(project_path),
            "created_at": datetime.now().isoformat(),
            "files": []
        }
        
        # Copy files (excluding common ignores)
        ignore_patterns = {
            "__pycache__", ".git", "venv", ".venv", "node_modules",
            "build", "dist", ".pytest_cache", "htmlcov", ".coverage",
            "backups", ".coverage"
        }
        
        for item in project_path.rglob("*"):
            if item.is_file():
                # Check if should ignore
                if any(part in ignore_patterns for part in item.parts):
                    continue
                
                rel_path = item.relative_to(project_path)
                dest_path = snapshot_dir / rel_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                shutil.copy2(item, dest_path)
                metadata["files"].append(str(rel_path))
        
        # Save metadata
        metadata_path = snapshot_dir / "metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        
        # Create archive (but keep directory too for list_snapshots to work)
        archive_path = self.backup_dir / f"{snapshot_id}.tar.gz"
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(snapshot_dir, arcname=snapshot_id)
        
        # Keep snapshot directory for listing (don't delete it)
        return snapshot_id
    
    def list_snapshots(self) -> List[Dict[str, Any]]:
        """
        List all snapshots.
        
        Returns:
            List of snapshot metadata
        """
        snapshots = []
        
        for item in self.backup_dir.iterdir():
            if item.is_dir() and (item / "metadata.json").exists():
                with open(item / "metadata.json", "r") as f:
                    metadata = json.load(f)
                    snapshots.append(metadata)
        
        return sorted(snapshots, key=lambda x: x.get("created_at", ""), reverse=True)
    
    def get_snapshot(self, snapshot_id: str) -> Optional[Dict[str, Any]]:
        """
        Get snapshot metadata.
        
        Args:
            snapshot_id: Snapshot ID
        
        Returns:
            Snapshot metadata or None
        """
        snapshot_dir = self.backup_dir / snapshot_id
        metadata_path = snapshot_dir / "metadata.json"
        
        if not metadata_path.exists():
            return None
        
        with open(metadata_path, "r") as f:
            return json.load(f)
    
    def restore_snapshot(self, snapshot_id: str, target_path: Optional[str] = None) -> bool:
        """
        Restore project from snapshot.
        
        Args:
            snapshot_id: Snapshot ID
            target_path: Target path (uses original if None)
        
        Returns:
            True if successful
        """
        snapshot = self.get_snapshot(snapshot_id)
        if not snapshot:
            return False
        
        if target_path is None:
            target_path = snapshot.get("project_path")
        
        target_path = Path(target_path)
        target_path.mkdir(parents=True, exist_ok=True)
        
        snapshot_dir = self.backup_dir / snapshot_id
        
        # Restore files
        for file_rel in snapshot.get("files", []):
            src_path = snapshot_dir / file_rel
            dst_path = target_path / file_rel
            
            if src_path.exists():
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, dst_path)
        
        return True
    
    def delete_snapshot(self, snapshot_id: str) -> bool:
        """
        Delete snapshot.
        
        Args:
            snapshot_id: Snapshot ID
        
        Returns:
            True if successful
        """
        snapshot_dir = self.backup_dir / snapshot_id
        archive_path = self.backup_dir / f"{snapshot_id}.tar.gz"
        
        if snapshot_dir.exists():
            shutil.rmtree(snapshot_dir)
        
        if archive_path.exists():
            archive_path.unlink()
        
        return True
    
    def cleanup_old_snapshots(self, keep_count: int = 10) -> int:
        """
        Cleanup old snapshots, keeping only most recent N.
        
        Args:
            keep_count: Number of snapshots to keep
        
        Returns:
            Number of snapshots deleted
        """
        snapshots = self.list_snapshots()
        
        if len(snapshots) <= keep_count:
            return 0
        
        deleted = 0
        for snapshot in snapshots[keep_count:]:
            if self.delete_snapshot(snapshot["snapshot_id"]):
                deleted += 1
        
        return deleted


__all__ = ["BackupManager"]

