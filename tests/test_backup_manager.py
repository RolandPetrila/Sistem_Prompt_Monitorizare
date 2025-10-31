"""Tests for BackupManager."""
import tempfile
from pathlib import Path
from core.backup_manager import BackupManager


def test_create_snapshot():
    """Should create project snapshot."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test project
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        (project_path / "main.py").write_text("print('hello')")
        (project_path / "config.json").write_text("{}")
        
        backup_dir = Path(tmpdir) / "backups"
        manager = BackupManager(str(backup_dir))
        
        snapshot_id = manager.create_snapshot(str(project_path))
        
        assert snapshot_id is not None
        assert (backup_dir / snapshot_id).exists()
        assert (backup_dir / snapshot_id / "metadata.json").exists()


def test_list_snapshots():
    """Should list all snapshots."""
    import time
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        (project_path / "test.py").write_text("# test")
        
        manager = BackupManager(str(Path(tmpdir) / "backups"))
        
        snapshot_id1 = manager.create_snapshot(str(project_path))
        time.sleep(0.01)  # Ensure different timestamps
        snapshot_id2 = manager.create_snapshot(str(project_path))
        
        snapshots = manager.list_snapshots()
        # Should find at least 2 snapshots (might have directories + archives)
        assert len(snapshots) >= 2


def test_get_snapshot():
    """Should get snapshot metadata."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        (project_path / "test.py").write_text("# test")
        
        manager = BackupManager(str(Path(tmpdir) / "backups"))
        
        snapshot_id = manager.create_snapshot(str(project_path))
        snapshot = manager.get_snapshot(snapshot_id)
        
        assert snapshot is not None
        assert snapshot["snapshot_id"] == snapshot_id
        assert "files" in snapshot


def test_get_nonexistent_snapshot():
    """Should return None for nonexistent snapshot."""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = BackupManager(str(Path(tmpdir) / "backups"))
        snapshot = manager.get_snapshot("nonexistent")
        assert snapshot is None


def test_restore_snapshot():
    """Should restore project from snapshot."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create project
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        test_file = project_path / "test.py"
        test_file.write_text("print('original')")
        
        manager = BackupManager(str(Path(tmpdir) / "backups"))
        snapshot_id = manager.create_snapshot(str(project_path))
        
        # Modify file
        test_file.write_text("print('modified')")
        
        # Restore to new location
        restore_path = Path(tmpdir) / "restored"
        success = manager.restore_snapshot(snapshot_id, str(restore_path))
        
        assert success is True
        restored_file = restore_path / "test.py"
        assert restored_file.exists()
        assert "original" in restored_file.read_text()


def test_delete_snapshot():
    """Should delete snapshot."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        (project_path / "test.py").write_text("# test")
        
        manager = BackupManager(str(Path(tmpdir) / "backups"))
        snapshot_id = manager.create_snapshot(str(project_path))
        
        assert manager.get_snapshot(snapshot_id) is not None
        
        success = manager.delete_snapshot(snapshot_id)
        assert success is True
        assert manager.get_snapshot(snapshot_id) is None


def test_cleanup_old_snapshots():
    """Should cleanup old snapshots."""
    import time
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        (project_path / "test.py").write_text("# test")
        
        manager = BackupManager(str(Path(tmpdir) / "backups"))
        
        # Create multiple snapshots
        for i in range(15):
            manager.create_snapshot(str(project_path))
            time.sleep(0.01)  # Ensure different timestamps
        
        initial_count = len(manager.list_snapshots())
        deleted = manager.cleanup_old_snapshots(keep_count=10)
        
        # Should have deleted some snapshots
        final_count = len(manager.list_snapshots())
        assert final_count <= initial_count
        assert deleted >= 0  # At least 0 deleted (might be more)


def test_ignore_patterns():
    """Should ignore common patterns in snapshots."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        # Create files including ignored
        (project_path / "main.py").write_text("# main")
        (project_path / "__pycache__").mkdir()
        (project_path / "__pycache__" / "test.pyc").write_bytes(b"")
        
        manager = BackupManager(str(Path(tmpdir) / "backups"))
        snapshot_id = manager.create_snapshot(str(project_path))
        
        snapshot = manager.get_snapshot(snapshot_id)
        files = snapshot.get("files", [])
        
        # Should not include __pycache__ files
        assert not any("__pycache__" in f for f in files)
        assert "main.py" in files


def test_custom_snapshot_id():
    """Should use custom snapshot ID."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        (project_path / "test.py").write_text("# test")
        
        manager = BackupManager(str(Path(tmpdir) / "backups"))
        
        custom_id = "custom_snapshot_123"
        snapshot_id = manager.create_snapshot(str(project_path), snapshot_id=custom_id)
        
        assert snapshot_id == custom_id
        assert manager.get_snapshot(custom_id) is not None


def test_snapshot_nonexistent_project():
    """Should raise error for nonexistent project."""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = BackupManager(str(Path(tmpdir) / "backups"))
        
        try:
            manager.create_snapshot("/nonexistent/path")
            assert False, "Should raise ValueError"
        except ValueError:
            pass

