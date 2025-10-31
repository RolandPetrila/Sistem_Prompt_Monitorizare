"""Tests for AnalyzeCodeQuality."""
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
from tasks.analyze_code_quality import AnalyzeCodeQuality


def test_analyze_code_quality_init():
    """Should initialize AnalyzeCodeQuality."""
    analyzer = AnalyzeCodeQuality()
    assert analyzer is not None


@patch('tasks.analyze_code_quality.AIOrchestrator')
def test_analyze_code_quality(mock_orchestrator_class):
    """Should analyze code quality."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        (project_path / "main.py").write_text("print('hello')")
        
        mock_response = Mock()
        mock_response.success = True
        mock_response.content = "Code quality analysis"
        mock_response.provider.value = "claude"
        mock_response.tokens_used = 100
        mock_response.error = None
        
        mock_orchestrator = Mock()
        mock_orchestrator.generate_completion.return_value = mock_response
        mock_orchestrator_class.return_value = mock_orchestrator
        
        analyzer = AnalyzeCodeQuality()
        response = analyzer.analyze(str(project_path))
        
        assert response.success is True
        assert "Code quality" in response.content


def test_get_suggestions():
    """Should get suggestions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "project"
        project_path.mkdir()
        
        analyzer = AnalyzeCodeQuality()
        # Will fail without API, but structure should work
        suggestions = analyzer.get_suggestions(str(project_path))
        
        assert "success" in suggestions

