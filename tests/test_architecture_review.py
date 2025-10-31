"""Tests for ArchitectureReview."""
import tempfile
from pathlib import Path
from tasks.architecture_review import ArchitectureReview


def test_architecture_review_init():
    """Should initialize ArchitectureReview."""
    reviewer = ArchitectureReview()
    assert reviewer is not None


def test_get_review():
    """Should get architecture review."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        reviewer = ArchitectureReview()
        review = reviewer.get_review(str(project_path))
        
        assert "success" in review
        assert "review" in review

