"""Tests for DependencyCheck."""
import tempfile
from pathlib import Path
from tasks.dependency_check import DependencyCheck


def test_dependency_check_init():
    """Should initialize DependencyCheck."""
    checker = DependencyCheck()
    assert checker is not None


def test_get_dependency_report():
    """Should get dependency report."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        # Create requirements.txt
        (project_path / "requirements.txt").write_text("pytest>=8.0.0\nrequests>=2.0.0")
        
        checker = DependencyCheck()
        report = checker.get_dependency_report(str(project_path))
        
        assert "success" in report
        assert "report" in report


def test_check_with_package_json():
    """Should check dependencies from package.json."""
    import json
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        # Create package.json
        package_json = {
            "dependencies": {
                "express": "^4.18.0",
                "lodash": "^4.17.21"
            },
            "devDependencies": {
                "jest": "^28.0.0"
            }
        }
        (project_path / "package.json").write_text(json.dumps(package_json))
        
        checker = DependencyCheck()
        report = checker.get_dependency_report(str(project_path))
        
        assert "success" in report

