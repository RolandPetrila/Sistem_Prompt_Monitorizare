"""Tests for IncrementalWorkflow."""
import tempfile
from pathlib import Path
from core.incremental_workflow import IncrementalWorkflow, Iteration


def test_create_iteration():
    """Should create new iteration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        workflow_file = Path(tmpdir) / "workflow.json"
        workflow = IncrementalWorkflow(str(project_path), str(workflow_file))
        
        iteration_id = workflow.create_iteration("Test task")
        
        assert iteration_id is not None
        assert iteration_id in workflow.iterations
        assert workflow.iterations[iteration_id].task == "Test task"


def test_complete_iteration():
    """Should complete iteration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        workflow_file = Path(tmpdir) / "workflow.json"
        workflow = IncrementalWorkflow(str(project_path), str(workflow_file))
        
        iteration_id = workflow.create_iteration("Test task")
        success = workflow.complete_iteration(
            iteration_id,
            {"files_modified": ["test.py"]},
            "Task completed successfully"
        )
        
        assert success is True
        iteration = workflow.get_iteration(iteration_id)
        assert iteration.status == "completed"
        assert iteration.result == "Task completed successfully"


def test_fail_iteration():
    """Should mark iteration as failed."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        workflow_file = Path(tmpdir) / "workflow.json"
        workflow = IncrementalWorkflow(str(project_path), str(workflow_file))
        
        iteration_id = workflow.create_iteration("Test task")
        success = workflow.fail_iteration(iteration_id, "Test error")
        
        assert success is True
        iteration = workflow.get_iteration(iteration_id)
        assert iteration.status == "failed"
        assert "error" in iteration.result.lower()


def test_get_iteration():
    """Should get iteration by ID."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        workflow_file = Path(tmpdir) / "workflow.json"
        workflow = IncrementalWorkflow(str(project_path), str(workflow_file))
        
        iteration_id = workflow.create_iteration("Test task")
        iteration = workflow.get_iteration(iteration_id)
        
        assert iteration is not None
        assert iteration.iteration_id == iteration_id


def test_get_nonexistent_iteration():
    """Should return None for nonexistent iteration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        workflow_file = Path(tmpdir) / "workflow.json"
        workflow = IncrementalWorkflow(str(project_path), str(workflow_file))
        
        iteration = workflow.get_iteration("nonexistent")
        assert iteration is None


def test_list_iterations():
    """Should list all iterations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        workflow_file = Path(tmpdir) / "workflow.json"
        workflow = IncrementalWorkflow(str(project_path), str(workflow_file))
        
        workflow.create_iteration("Task 1")
        workflow.create_iteration("Task 2")
        
        iterations = workflow.list_iterations()
        assert len(iterations) == 2


def test_list_iterations_by_status():
    """Should filter iterations by status."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        workflow_file = Path(tmpdir) / "workflow.json"
        workflow = IncrementalWorkflow(str(project_path), str(workflow_file))
        
        iter1 = workflow.create_iteration("Task 1")
        iter2 = workflow.create_iteration("Task 2")
        
        workflow.complete_iteration(iter1, {})
        
        completed = workflow.list_iterations(status="completed")
        assert len(completed) == 1
        assert completed[0].iteration_id == iter1


def test_get_current_iteration():
    """Should get current active iteration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        workflow_file = Path(tmpdir) / "workflow.json"
        workflow = IncrementalWorkflow(str(project_path), str(workflow_file))
        
        iter1 = workflow.create_iteration("Task 1")
        workflow.create_iteration("Task 2")
        
        current = workflow.get_current_iteration()
        assert current is not None
        assert current.status == "in_progress"


def test_get_progress():
    """Should get workflow progress."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        workflow_file = Path(tmpdir) / "workflow.json"
        workflow = IncrementalWorkflow(str(project_path), str(workflow_file))
        
        iter1 = workflow.create_iteration("Task 1")
        iter2 = workflow.create_iteration("Task 2")
        
        workflow.complete_iteration(iter1, {})
        
        progress = workflow.get_progress()
        
        assert progress["total"] == 2
        assert progress["completed"] == 1
        assert progress["in_progress"] == 1
        assert progress["completion_rate"] == 0.5


def test_load_saved_workflow():
    """Should load workflow from file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        workflow_file = Path(tmpdir) / "workflow.json"
        
        # Create workflow and save
        workflow1 = IncrementalWorkflow(str(project_path), str(workflow_file))
        iter_id = workflow1.create_iteration("Test")
        
        # Load in new instance
        workflow2 = IncrementalWorkflow(str(project_path), str(workflow_file))
        
        assert iter_id in workflow2.iterations
        assert workflow2.get_iteration(iter_id).task == "Test"


def test_custom_snapshot_id():
    """Should use custom snapshot ID."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        workflow_file = Path(tmpdir) / "workflow.json"
        workflow = IncrementalWorkflow(str(project_path), str(workflow_file))
        
        custom_snapshot = "custom_snap_123"
        iteration_id = workflow.create_iteration("Test", snapshot_id=custom_snapshot)
        
        iteration = workflow.get_iteration(iteration_id)
        assert iteration.snapshot_id == custom_snapshot

