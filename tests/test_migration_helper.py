"""Tests for MigrationHelper."""
import tempfile
from pathlib import Path
from tasks.migration_helper import MigrationHelper


def test_migration_helper_init():
    """Should initialize MigrationHelper."""
    helper = MigrationHelper()
    assert helper is not None


def test_get_migration_guide():
    """Should get migration guide."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        helper = MigrationHelper()
        guide = helper.get_migration_guide(str(project_path))
        
        assert "success" in guide
        assert "guide" in guide


def test_get_migration_guide_with_target():
    """Should get migration guide with target framework."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        helper = MigrationHelper()
        guide = helper.get_migration_guide(str(project_path), "Python 3.13")
        
        assert "success" in guide

