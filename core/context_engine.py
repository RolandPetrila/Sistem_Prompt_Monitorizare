"""Context engine for analyzing project structure and code."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Optional, Any
import json


class ContextEngine:
    """
    Analyzes project structure and generates context for prompts.
    
    Features:
    - File structure analysis
    - Code parsing with tree-sitter
    - Context summarization
    - Change tracking
    """
    
    def __init__(self, project_path: str) -> None:
        self.project_path = Path(project_path)
        self._structure_cache: Dict[str, Any] = {}
    
    def analyze_project_structure(self) -> Dict[str, Any]:
        """
        Analyze project file structure.
        
        Returns:
            Dictionary with project structure information
        """
        if not self.project_path.exists():
            return {"error": "Project path does not exist"}
        
        structure = {
            "root": str(self.project_path),
            "files": [],
            "directories": [],
            "file_types": {},
            "total_files": 0
        }
        
        # Common ignore patterns
        ignore_patterns = {
            "__pycache__", ".git", "venv", ".venv", "node_modules",
            "build", "dist", ".pytest_cache", "htmlcov", ".coverage"
        }
        
        for root, dirs, files in os.walk(self.project_path):
            # Filter ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_patterns]
            
            rel_root = Path(root).relative_to(self.project_path)
            
            # Add directories
            if rel_root != Path("."):
                structure["directories"].append(str(rel_root))
            
            # Add files with extensions
            for file in files:
                file_path = Path(root) / file
                rel_path = file_path.relative_to(self.project_path)
                
                structure["files"].append(str(rel_path))
                structure["total_files"] += 1
                
                # Count by extension
                ext = file_path.suffix.lower()
                if ext:
                    structure["file_types"][ext] = structure["file_types"].get(ext, 0) + 1
        
        self._structure_cache = structure
        return structure
    
    def get_code_summary(self, file_path: str, max_lines: int = 50) -> Dict[str, Any]:
        """
        Get summary of code file.
        
        Args:
            file_path: Relative path to file
            max_lines: Maximum lines to read
        
        Returns:
            Summary dictionary
        """
        full_path = self.project_path / file_path
        
        if not full_path.exists():
            return {"error": f"File not found: {file_path}"}
        
        summary = {
            "path": file_path,
            "size": full_path.stat().st_size,
            "lines": 0,
            "preview": []
        }
        
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                summary["lines"] = len(lines)
                
                # Preview first lines
                preview_lines = lines[:max_lines]
                summary["preview"] = [line.rstrip() for line in preview_lines]
                
        except Exception as e:
            summary["error"] = str(e)
        
        return summary
    
    def generate_context_prompt(self, task_type: str = "general") -> str:
        """
        Generate context prompt for AI.
        
        Args:
            task_type: Type of task (code_quality, refactoring, etc.)
        
        Returns:
            Context prompt string
        """
        structure = self.analyze_project_structure()
        
        prompt_parts = [
            f"# Project Context: {self.project_path.name}",
            f"\n## Project Structure",
            f"- Root: {structure.get('root', 'N/A')}",
            f"- Total Files: {structure.get('total_files', 0)}",
            f"- Directories: {len(structure.get('directories', []))}",
        ]
        
        # Add file type statistics
        if structure.get("file_types"):
            prompt_parts.append("\n## File Types:")
            for ext, count in sorted(structure["file_types"].items(), key=lambda x: -x[1])[:10]:
                prompt_parts.append(f"- {ext}: {count} files")
        
        # Add key files
        key_files = [f for f in structure.get("files", []) 
                    if any(f.endswith(ext) for ext in [".py", ".js", ".ts", ".java", ".go"])][:10]
        
        if key_files:
            prompt_parts.append("\n## Key Files:")
            for file in key_files:
                prompt_parts.append(f"- {file}")
        
        return "\n".join(prompt_parts)
    
    def get_recent_changes(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get list of recently modified files.
        
        Args:
            days: Number of days to look back
        
        Returns:
            List of file change information
        """
        import time
        
        changes = []
        cutoff_time = time.time() - (days * 24 * 60 * 60)
        
        for root, dirs, files in os.walk(self.project_path):
            # Filter ignored
            dirs[:] = [d for d in dirs if d not in {"__pycache__", ".git", "venv"}]
            
            for file in files:
                file_path = Path(root) / file
                
                try:
                    mtime = file_path.stat().st_mtime
                    if mtime > cutoff_time:
                        rel_path = file_path.relative_to(self.project_path)
                        changes.append({
                            "path": str(rel_path),
                            "modified": time.ctime(mtime),
                            "size": file_path.stat().st_size
                        })
                except Exception:
                    pass
        
        return sorted(changes, key=lambda x: x["modified"], reverse=True)


__all__ = ["ContextEngine"]

