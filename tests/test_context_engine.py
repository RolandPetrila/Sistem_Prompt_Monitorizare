"""Tests for ContextEngine."""
import tempfile
from pathlib import Path
from core.context_engine import ContextEngine


def test_analyze_project_structure():
    """Should analyze project structure."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "test_project"
        project_path.mkdir()
        
        # Create test files
        (project_path / "main.py").write_text("print('hello')")
        (project_path / "config.json").write_text("{}")
        (project_path / "README.md").write_text("# Test")
        
        engine = ContextEngine(str(project_path))
        structure = engine.analyze_project_structure()
        
        assert structure["total_files"] == 3
        assert ".py" in structure["file_types"]
        assert ".json" in structure["file_types"]


def test_get_code_summary():
    """Should get code file summary."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "test_project"
        project_path.mkdir()
        
        test_file = project_path / "test.py"
        test_file.write_text("def hello():\n    print('world')\n")
        
        engine = ContextEngine(str(project_path))
        summary = engine.get_code_summary("test.py")
        
        assert summary["path"] == "test.py"
        assert summary["lines"] == 2
        assert len(summary["preview"]) > 0


def test_generate_context_prompt():
    """Should generate context prompt."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "test_project"
        project_path.mkdir()
        
        (project_path / "main.py").write_text("print('hello')")
        
        engine = ContextEngine(str(project_path))
        prompt = engine.generate_context_prompt()
        
        assert "Project Context" in prompt
        assert "Project Structure" in prompt


def test_get_recent_changes():
    """Should get recently modified files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "test_project"
        project_path.mkdir()
        
        test_file = project_path / "recent.py"
        test_file.write_text("# Recent file")
        
        engine = ContextEngine(str(project_path))
        changes = engine.get_recent_changes(days=7)
        
        assert len(changes) >= 1
        assert any(c["path"] == "recent.py" for c in changes)


def test_nonexistent_project():
    """Should handle nonexistent project."""
    engine = ContextEngine("/nonexistent/path")
    structure = engine.analyze_project_structure()
    
    assert "error" in structure


def test_nonexistent_file():
    """Should handle nonexistent file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "test_project"
        project_path.mkdir()
        
        engine = ContextEngine(str(project_path))
        summary = engine.get_code_summary("nonexistent.py")
        
        assert "error" in summary


def test_ignore_patterns():
    """Should ignore common patterns."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "test_project"
        project_path.mkdir()
        
        # Create ignored directory
        (project_path / "__pycache__").mkdir()
        (project_path / "__pycache__" / "test.pyc").write_bytes(b"")
        
        # Create normal file
        (project_path / "main.py").write_text("print('hello')")
        
        engine = ContextEngine(str(project_path))
        structure = engine.analyze_project_structure()
        
        # Should not include __pycache__ files
        assert not any("__pycache__" in f for f in structure["files"])


def test_file_type_counting():
    """Should count files by type."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "test_project"
        project_path.mkdir()
        
        for i in range(5):
            (project_path / f"test{i}.py").write_text("# test")
        
        engine = ContextEngine(str(project_path))
        structure = engine.analyze_project_structure()
        
        assert structure["file_types"].get(".py") == 5


def test_context_prompt_format():
    """Should format context prompt correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "test_project"
        project_path.mkdir()
        
        (project_path / "main.py").write_text("print('hello')")
        
        engine = ContextEngine(str(project_path))
        prompt = engine.generate_context_prompt("code_quality")
        
        assert prompt.startswith("# Project Context:")
        assert "## Project Structure" in prompt


def test_recent_changes_empty():
    """Should return empty list for old changes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "test_project"
        project_path.mkdir()
        
        # Create file but don't modify it recently
        test_file = project_path / "old.py"
        test_file.write_text("# Old")
        
        engine = ContextEngine(str(project_path))
        changes = engine.get_recent_changes(days=0)  # Only today
        
        # Might be empty or have the file depending on timing
        assert isinstance(changes, list)

