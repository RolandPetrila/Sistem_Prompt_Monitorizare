"""Tests for CodeStyleFix."""
import tempfile
from pathlib import Path
from tasks.code_style_fix import CodeStyleFix


def test_code_style_fix_init():
    """Should initialize CodeStyleFix."""
    fixer = CodeStyleFix()
    assert fixer is not None


def test_get_style_fixes():
    """Should get style fixes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        fixer = CodeStyleFix()
        fixes = fixer.get_style_fixes(str(project_path))
        
        assert "success" in fixes
        assert "fixes" in fixes

