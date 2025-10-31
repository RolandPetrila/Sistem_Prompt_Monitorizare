"""Tests for Database."""
import tempfile
from pathlib import Path
from core.database import Database


def test_database_init():
    """Database should initialize schema."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(str(db_path))
        assert db_path.exists()


def test_add_get_project():
    """Should add and retrieve project."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db = Database(str(Path(tmpdir) / "test.db"))
        
        project_id = db.add_project("/path/to/project", "TestProject")
        assert project_id > 0
        
        project = db.get_project("/path/to/project")
        assert project is not None
        assert project["name"] == "TestProject"


def test_add_get_prompts():
    """Should add and retrieve prompts."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db = Database(str(Path(tmpdir) / "test.db"))
        
        project_id = db.add_project("/path", "Test")
        prompt_id = db.add_prompt(project_id, "code_quality", "Analyze this code...")
        
        prompts = db.get_prompts(project_id)
        assert len(prompts) == 1
        assert prompts[0]["task_type"] == "code_quality"


def test_add_iteration():
    """Should add iteration record."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db = Database(str(Path(tmpdir) / "test.db"))
        
        project_id = db.add_project("/path", "Test")
        iteration_id = db.add_iteration(
            project_id, "iter-123", "refactor", "snap-456", "2025-01-01T00:00:00"
        )
        assert iteration_id > 0


def test_update_iteration():
    """Should update iteration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db = Database(str(Path(tmpdir) / "test.db"))
        
        project_id = db.add_project("/path", "Test")
        db.add_iteration(project_id, "iter-123", "task", "snap", "2025-01-01")
        
        db.update_iteration("iter-123", "2025-01-02", '{"changes": []}')
        # Should not raise


def test_get_nonexistent_project():
    """Should return None for nonexistent project."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db = Database(str(Path(tmpdir) / "test.db"))
        project = db.get_project("/nonexistent")
        assert project is None


def test_prompts_limit():
    """Should respect limit parameter."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db = Database(str(Path(tmpdir) / "test.db"))
        project_id = db.add_project("/path", "Test")
        
        for i in range(20):
            db.add_prompt(project_id, "task", f"Prompt {i}")
        
        prompts = db.get_prompts(project_id, limit=5)
        assert len(prompts) == 5


def test_prompts_order():
    """Should return newest prompts first."""
    import time
    with tempfile.TemporaryDirectory() as tmpdir:
        db = Database(str(Path(tmpdir) / "test.db"))
        project_id = db.add_project("/path", "Test")
        
        db.add_prompt(project_id, "task", "First")
        time.sleep(0.01)  # Small delay to ensure different timestamps
        db.add_prompt(project_id, "task", "Second")
        
        prompts = db.get_prompts(project_id)
        assert prompts[0]["prompt_text"] == "Second"
        assert prompts[1]["prompt_text"] == "First"

