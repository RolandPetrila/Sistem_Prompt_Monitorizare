"""Change detector for monitoring file modifications."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime


class ChangeDetector:
    """
    Detects changes in project files.
    
    Features:
    - File hash tracking
    - Change detection
    - Modified files list
    - Change history
    """
    
    def __init__(self, project_path: str, state_file: str = ".change_state.json") -> None:
        self.project_path = Path(project_path)
        self.state_file = Path(state_file)
        self._file_hashes: Dict[str, str] = {}
        self._load_state()
    
    def _load_state(self) -> None:
        """Load previous state from file."""
        if self.state_file.exists():
            try:
                with open(self.state_file, "r") as f:
                    data = json.load(f)
                    self._file_hashes = data.get("file_hashes", {})
            except Exception:
                self._file_hashes = {}
        else:
            self._file_hashes = {}
    
    def _save_state(self) -> None:
        """Save current state to file."""
        data = {
            "file_hashes": self._file_hashes,
            "last_updated": datetime.now().isoformat()
        }
        
        with open(self.state_file, "w") as f:
            json.dump(data, f, indent=2)
    
    def _calculate_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file."""
        try:
            with open(file_path, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""
    
    def detect_changes(self) -> Dict[str, List[str]]:
        """
        Detect changes in project files.
        
        Returns:
            Dictionary with 'modified', 'added', 'deleted' file lists
        """
        if not self.project_path.exists():
            return {"modified": [], "added": [], "deleted": []}
        
        changes = {
            "modified": [],
            "added": [],
            "deleted": []
        }
        
        ignore_patterns = {
            "__pycache__", ".git", "venv", ".venv", "node_modules",
            "build", "dist", ".pytest_cache", "htmlcov", ".coverage",
            ".change_state.json", "backups"
        }
        
        current_files: Set[str] = set()
        
        # Scan current files
        for item in self.project_path.rglob("*"):
            if item.is_file():
                # Check if should ignore
                if any(part in ignore_patterns for part in item.parts):
                    continue
                
                rel_path = str(item.relative_to(self.project_path))
                current_files.add(rel_path)
                
                current_hash = self._calculate_hash(item)
                
                if rel_path in self._file_hashes:
                    # File exists, check if modified
                    if self._file_hashes[rel_path] != current_hash:
                        changes["modified"].append(rel_path)
                        self._file_hashes[rel_path] = current_hash
                else:
                    # New file
                    changes["added"].append(rel_path)
                    self._file_hashes[rel_path] = current_hash
        
        # Check for deleted files
        previous_files = set(self._file_hashes.keys())
        deleted_files = previous_files - current_files
        
        for file in deleted_files:
            changes["deleted"].append(file)
            del self._file_hashes[file]
        
        # Save updated state
        self._save_state()
        
        return changes
    
    def get_modified_files(self) -> List[str]:
        """
        Get list of modified files since last check.
        
        Returns:
            List of modified file paths
        """
        changes = self.detect_changes()
        return changes["modified"]
    
    def has_changes(self) -> bool:
        """
        Check if there are any changes.
        
        Returns:
            True if changes detected
        """
        changes = self.detect_changes()
        return len(changes["modified"]) > 0 or len(changes["added"]) > 0 or len(changes["deleted"]) > 0
    
    def reset_state(self) -> None:
        """Reset change detection state (treat all files as new)."""
        self._file_hashes = {}
        self._save_state()


__all__ = ["ChangeDetector"]

