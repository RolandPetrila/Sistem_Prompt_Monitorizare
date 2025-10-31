"""Tests for RefactorCode."""
import tempfile
from pathlib import Path
from tasks.refactor_code import RefactorCode


def test_refactor_code_init():
    """Should initialize RefactorCode."""
    refactor = RefactorCode()
    assert refactor is not None


def test_get_refactoring_suggestions():
    """Should get refactoring suggestions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        refactor = RefactorCode()
        suggestions = refactor.get_refactoring_suggestions(str(project_path))
        
        assert "success" in suggestions
        assert "suggestions" in suggestions

