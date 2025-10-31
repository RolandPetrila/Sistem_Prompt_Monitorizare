"""Tests for FindBugs."""
import tempfile
from pathlib import Path
from tasks.find_bugs import FindBugs


def test_find_bugs_init():
    """Should initialize FindBugs."""
    finder = FindBugs()
    assert finder is not None


def test_get_bug_report():
    """Should get bug report."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        finder = FindBugs()
        report = finder.get_bug_report(str(project_path))
        
        assert "success" in report
        assert "bugs" in report

