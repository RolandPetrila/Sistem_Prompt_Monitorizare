"""Tests for OptimizePerformance."""
import tempfile
from pathlib import Path
from tasks.optimize_performance import OptimizePerformance


def test_optimize_performance_init():
    """Should initialize OptimizePerformance."""
    optimizer = OptimizePerformance()
    assert optimizer is not None


def test_get_optimization_report():
    """Should get optimization report."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        optimizer = OptimizePerformance()
        report = optimizer.get_optimization_report(str(project_path))
        
        assert "success" in report
        assert "optimizations" in report

