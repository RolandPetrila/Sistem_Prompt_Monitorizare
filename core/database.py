"""SQLite database manager."""
from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from contextlib import contextmanager


class Database:
    """
    SQLite database manager with migrations.
    
    Tables:
    - projects: Tracked projects
    - prompts: Generated prompts history
    - iterations: Incremental workflow iterations
    """
    
    def __init__(self, db_path: str = "data.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connection."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def _init_schema(self) -> None:
        """Initialize database schema."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Projects table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_analyzed TIMESTAMP
                )
            """)
            
            # Prompts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prompts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    task_type TEXT NOT NULL,
                    prompt_text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects(id)
                )
            """)
            
            # Iterations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS iterations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    iteration_id TEXT UNIQUE NOT NULL,
                    task TEXT NOT NULL,
                    snapshot_id TEXT NOT NULL,
                    started_at TIMESTAMP,
                    ended_at TIMESTAMP,
                    changes TEXT,
                    FOREIGN KEY (project_id) REFERENCES projects(id)
                )
            """)
    
    def add_project(self, path: str, name: str) -> int:
        """Add or update project."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO projects (path, name, last_analyzed)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (path, name))
            return cursor.lastrowid
    
    def get_project(self, path: str) -> Optional[Dict[str, Any]]:
        """Get project by path."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects WHERE path = ?", (path,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def add_prompt(self, project_id: int, task_type: str, prompt_text: str) -> int:
        """Add prompt to history."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Use explicit timestamp to ensure ordering
            timestamp = datetime.now().isoformat()
            cursor.execute("""
                INSERT INTO prompts (project_id, task_type, prompt_text, created_at)
                VALUES (?, ?, ?, ?)
            """, (project_id, task_type, prompt_text, timestamp))
            return cursor.lastrowid
    
    def get_prompts(self, project_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent prompts for project."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM prompts 
                WHERE project_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (project_id, limit))
            return [dict(row) for row in cursor.fetchall()]
    
    def add_iteration(self, project_id: int, iteration_id: str, task: str, 
                     snapshot_id: str, started_at: str) -> int:
        """Add iteration record."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO iterations 
                (project_id, iteration_id, task, snapshot_id, started_at)
                VALUES (?, ?, ?, ?, ?)
            """, (project_id, iteration_id, task, snapshot_id, started_at))
            return cursor.lastrowid
    
    def update_iteration(self, iteration_id: str, ended_at: str, changes: str) -> None:
        """Update iteration when complete."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE iterations 
                SET ended_at = ?, changes = ?
                WHERE iteration_id = ?
            """, (ended_at, changes, iteration_id))


__all__ = ["Database"]

