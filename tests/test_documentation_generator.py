"""Tests for DocumentationGenerator."""
import tempfile
from pathlib import Path
from tasks.documentation_generator import DocumentationGenerator


def test_documentation_generator_init():
    """Should initialize DocumentationGenerator."""
    generator = DocumentationGenerator()
    assert generator is not None


def test_get_documentation():
    """Should get documentation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        generator = DocumentationGenerator()
        doc = generator.get_documentation(str(project_path))
        
        assert "success" in doc
        assert "documentation" in doc

