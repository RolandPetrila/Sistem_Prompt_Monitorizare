"""Tests for ChangeDetector."""
import tempfile
from pathlib import Path
from core.change_detector import ChangeDetector


def test_detect_changes():
    """Should detect file changes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        test_file = project_path / "test.py"
        test_file.write_text("print('v1')")
        
        state_file = Path(tmpdir) / "state.json"
        detector = ChangeDetector(str(project_path), str(state_file))
        
        # First scan - should detect as new
        changes = detector.detect_changes()
        assert len(changes["added"]) > 0
        
        # Second scan - no changes
        changes = detector.detect_changes()
        assert len(changes["modified"]) == 0
        assert len(changes["added"]) == 0
        
        # Modify file
        test_file.write_text("print('v2')")
        changes = detector.detect_changes()
        assert "test.py" in changes["modified"]


def test_detect_added_files():
    """Should detect added files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        state_file = Path(tmpdir) / "state.json"
        detector = ChangeDetector(str(project_path), str(state_file))
        
        # Initial scan
        detector.detect_changes()
        
        # Add new file
        new_file = project_path / "new.py"
        new_file.write_text("# new")
        
        changes = detector.detect_changes()
        assert "new.py" in changes["added"]


def test_detect_deleted_files():
    """Should detect deleted files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        test_file = project_path / "test.py"
        test_file.write_text("# test")
        
        state_file = Path(tmpdir) / "state.json"
        detector = ChangeDetector(str(project_path), str(state_file))
        
        # Initial scan
        detector.detect_changes()
        
        # Delete file
        test_file.unlink()
        
        changes = detector.detect_changes()
        assert "test.py" in changes["deleted"]


def test_has_changes():
    """Should correctly detect if changes exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        state_file = Path(tmpdir) / "state.json"
        detector = ChangeDetector(str(project_path), str(state_file))
        
        # First check - should have changes (new files)  
        # Create file first
        test_file = project_path / "test.py"
        test_file.write_text("# test")
        
        # First detection should find new file
        assert detector.has_changes() is True
        
        # After detection, no more changes
        detector.detect_changes()  # This saves state
        assert detector.has_changes() is False
        
        # Now modify it
        test_file.write_text("# modified")
        assert detector.has_changes() is True


def test_get_modified_files():
    """Should get list of modified files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        test_file = project_path / "test.py"
        test_file.write_text("v1")
        
        state_file = Path(tmpdir) / "state.json"
        detector = ChangeDetector(str(project_path), str(state_file))
        detector.detect_changes()  # Initial scan
        
        test_file.write_text("v2")
        modified = detector.get_modified_files()
        
        assert "test.py" in modified


def test_reset_state():
    """Should reset state."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        test_file = project_path / "test.py"
        test_file.write_text("# test")
        
        state_file = Path(tmpdir) / "state.json"
        detector = ChangeDetector(str(project_path), str(state_file))
        detector.detect_changes()
        
        detector.reset_state()
        
        # After reset, all files should be detected as new
        changes = detector.detect_changes()
        assert "test.py" in changes["added"]


def test_ignore_patterns():
    """Should ignore common patterns."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        # Create ignored file
        (project_path / "__pycache__").mkdir()
        (project_path / "__pycache__" / "test.pyc").write_bytes(b"")
        
        # Create normal file
        (project_path / "main.py").write_text("# main")
        
        state_file = Path(tmpdir) / "state.json"
        detector = ChangeDetector(str(project_path), str(state_file))
        changes = detector.detect_changes()
        
        # Should not include __pycache__ files
        assert not any("__pycache__" in f for f in changes["added"])
        assert "main.py" in changes["added"]


def test_load_saved_state():
    """Should load saved state from file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        test_file = project_path / "test.py"
        test_file.write_text("# test")
        
        state_file = Path(tmpdir) / "state.json"
        
        # Create detector and scan
        detector1 = ChangeDetector(str(project_path), str(state_file))
        detector1.detect_changes()
        
        # Create new detector - should load state
        detector2 = ChangeDetector(str(project_path), str(state_file))
        changes = detector2.detect_changes()
        
        # Should not detect test.py as new
        assert "test.py" not in changes["added"]


def test_nonexistent_project():
    """Should handle nonexistent project."""
    state_file = Path("/tmp/state.json")
    detector = ChangeDetector("/nonexistent/path", str(state_file))
    
    changes = detector.detect_changes()
    assert changes == {"modified": [], "added": [], "deleted": []}

