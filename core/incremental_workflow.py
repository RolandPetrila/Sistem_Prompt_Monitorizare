"""Incremental workflow for step-by-step project improvements."""
from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class Iteration:
    """Single iteration in incremental workflow."""
    iteration_id: str
    task: str
    snapshot_id: str
    started_at: str
    ended_at: Optional[str] = None
    changes: Optional[Dict[str, Any]] = None
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[str] = None


class IncrementalWorkflow:
    """
    Manages incremental workflow for step-by-step improvements.
    
    Features:
    - Create iterations
    - Track progress
    - Manage snapshots
    - Export workflow history
    """
    
    def __init__(self, project_path: str, workflow_file: str = ".workflow.json") -> None:
        self.project_path = Path(project_path)
        self.workflow_file = Path(workflow_file)
        self.iterations: Dict[str, Iteration] = {}
        self._load_workflow()
    
    def _load_workflow(self) -> None:
        """Load workflow from file."""
        if self.workflow_file.exists():
            try:
                with open(self.workflow_file, "r") as f:
                    data = json.load(f)
                    iterations_data = data.get("iterations", {})
                    
                    for iter_id, iter_data in iterations_data.items():
                        self.iterations[iter_id] = Iteration(**iter_data)
            except Exception:
                self.iterations = {}
        else:
            self.iterations = {}
    
    def _save_workflow(self) -> None:
        """Save workflow to file."""
        data = {
            "project_path": str(self.project_path),
            "iterations": {iter_id: asdict(iteration) for iter_id, iteration in self.iterations.items()},
            "last_updated": datetime.now().isoformat()
        }
        
        with open(self.workflow_file, "w") as f:
            json.dump(data, f, indent=2)
    
    def create_iteration(
        self,
        task: str,
        snapshot_id: Optional[str] = None
    ) -> str:
        """
        Create new iteration.
        
        Args:
            task: Task description
            snapshot_id: Optional snapshot ID (auto-generated if None)
        
        Returns:
            Iteration ID
        """
        if snapshot_id is None:
            snapshot_id = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        iteration_id = f"iter_{uuid.uuid4().hex[:8]}"
        
        iteration = Iteration(
            iteration_id=iteration_id,
            task=task,
            snapshot_id=snapshot_id,
            started_at=datetime.now().isoformat(),
            status="in_progress"
        )
        
        self.iterations[iteration_id] = iteration
        self._save_workflow()
        
        return iteration_id
    
    def complete_iteration(
        self,
        iteration_id: str,
        changes: Dict[str, Any],
        result: Optional[str] = None
    ) -> bool:
        """
        Mark iteration as completed.
        
        Args:
            iteration_id: Iteration ID
            changes: Dictionary of changes made
            result: Optional result description
        
        Returns:
            True if successful
        """
        if iteration_id not in self.iterations:
            return False
        
        iteration = self.iterations[iteration_id]
        iteration.status = "completed"
        iteration.ended_at = datetime.now().isoformat()
        iteration.changes = changes
        iteration.result = result
        
        self._save_workflow()
        return True
    
    def fail_iteration(self, iteration_id: str, error: str) -> bool:
        """
        Mark iteration as failed.
        
        Args:
            iteration_id: Iteration ID
            error: Error description
        
        Returns:
            True if successful
        """
        if iteration_id not in self.iterations:
            return False
        
        iteration = self.iterations[iteration_id]
        iteration.status = "failed"
        iteration.ended_at = datetime.now().isoformat()
        iteration.result = f"Error: {error}"
        
        self._save_workflow()
        return True
    
    def get_iteration(self, iteration_id: str) -> Optional[Iteration]:
        """
        Get iteration by ID.
        
        Args:
            iteration_id: Iteration ID
        
        Returns:
            Iteration or None
        """
        return self.iterations.get(iteration_id)
    
    def list_iterations(self, status: Optional[str] = None) -> List[Iteration]:
        """
        List all iterations, optionally filtered by status.
        
        Args:
            status: Optional status filter (pending, in_progress, completed, failed)
        
        Returns:
            List of iterations
        """
        iterations = list(self.iterations.values())
        
        if status:
            iterations = [i for i in iterations if i.status == status]
        
        # Sort by started_at
        iterations.sort(key=lambda x: x.started_at, reverse=True)
        
        return iterations
    
    def get_current_iteration(self) -> Optional[Iteration]:
        """
        Get current active iteration (in_progress).
        
        Returns:
            Current iteration or None
        """
        active = [i for i in self.iterations.values() if i.status == "in_progress"]
        
        if active:
            return max(active, key=lambda x: x.started_at)
        
        return None
    
    def get_progress(self) -> Dict[str, Any]:
        """
        Get workflow progress statistics.
        
        Returns:
            Progress dictionary
        """
        total = len(self.iterations)
        
        if total == 0:
            return {
                "total": 0,
                "completed": 0,
                "failed": 0,
                "in_progress": 0,
                "pending": 0,
                "completion_rate": 0.0
            }
        
        completed = len([i for i in self.iterations.values() if i.status == "completed"])
        failed = len([i for i in self.iterations.values() if i.status == "failed"])
        in_progress = len([i for i in self.iterations.values() if i.status == "in_progress"])
        pending = len([i for i in self.iterations.values() if i.status == "pending"])
        
        return {
            "total": total,
            "completed": completed,
            "failed": failed,
            "in_progress": in_progress,
            "pending": pending,
            "completion_rate": completed / total if total > 0 else 0.0
        }


__all__ = ["IncrementalWorkflow", "Iteration"]

