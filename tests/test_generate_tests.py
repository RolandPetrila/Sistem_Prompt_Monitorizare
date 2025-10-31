"""Tests for GenerateTests."""
import tempfile
from pathlib import Path
from tasks.generate_tests import GenerateTests


def test_generate_tests_init():
    """Should initialize GenerateTests."""
    generator = GenerateTests()
    assert generator is not None


def test_get_test_suite():
    """Should get test suite."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        generator = GenerateTests()
        suite = generator.get_test_suite(str(project_path))
        
        assert "success" in suite
        assert "tests" in suite

