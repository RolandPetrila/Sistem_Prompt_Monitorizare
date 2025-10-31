"""Tests for PerformanceProfiling."""
import tempfile
from pathlib import Path
from tasks.performance_profiling import PerformanceProfiling


def test_performance_profiling_init():
    """Should initialize PerformanceProfiling."""
    profiler = PerformanceProfiling()
    assert profiler is not None


def test_get_profile_report():
    """Should get profile report."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        profiler = PerformanceProfiling()
        report = profiler.get_profile_report(str(project_path))
        
        assert "success" in report
        assert "profile" in report

