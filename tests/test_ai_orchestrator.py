"""Tests for AIOrchestrator."""
import tempfile
from pathlib import Path
from core.ai_orchestrator import AIOrchestrator, AIProvider, AIResponse


def test_ai_orchestrator_init():
    """Should initialize AIOrchestrator."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create minimal config
        config_path = Path(tmpdir) / "config.json"
        config_path.write_text('{"ai_providers": {}, "fallback_strategy": {}, "fine_tuning": {}}')
        
        orchestrator = AIOrchestrator(str(config_path))
        assert orchestrator is not None


def test_ai_orchestrator_no_config():
    """Should handle missing config file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "nonexistent.json"
        orchestrator = AIOrchestrator(str(config_path))
        assert orchestrator.config is not None


def test_ai_orchestrator_all_failed():
    """Should return failed response when all providers fail."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.json"
        config_path.write_text('{"ai_providers": {}, "fallback_strategy": {"retry_count": 1}}')
        
        orchestrator = AIOrchestrator(str(config_path))
        response = orchestrator.generate_completion("test prompt")
        
        assert response.success is False
        assert "failed" in response.error.lower() or response.error == ""


def test_export_fine_tuning_data():
    """Should export fine-tuning data."""
    import json
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.json"
        config = {"ai_providers": {}, "fallback_strategy": {}, "fine_tuning": {"enabled": True}}
        with open(config_path, "w") as f:
            json.dump(config, f)
        
        orchestrator = AIOrchestrator(str(config_path))
        
        # Add some history
        orchestrator.fine_tuning_history = [
            {
                "prompt": "test prompt",
                "response": "test response",
                "provider": "claude",
                "tokens": 100,
                "timestamp": 1234567890
            }
        ]
        
        output_path = Path(tmpdir) / "output.jsonl"
        orchestrator.export_fine_tuning_data(str(output_path))
        
        assert output_path.exists()
        content = output_path.read_text()
        assert "test prompt" in content
        assert "test response" in content


def test_get_usage_stats():
    """Should return usage statistics."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.json"
        config_path.write_text('{}')
        
        orchestrator = AIOrchestrator(str(config_path))
        stats = orchestrator.get_usage_stats()
        
        assert isinstance(stats, dict)


def test_fine_tuning_history_limit():
    """Should limit fine-tuning history size."""
    import json
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.json"
        config = {"ai_providers": {}, "fallback_strategy": {}, "fine_tuning": {"enabled": True, "history_size": 5}}
        with open(config_path, "w") as f:
            json.dump(config, f)
        
        orchestrator = AIOrchestrator(str(config_path))
        
        # Add more than limit
        for i in range(10):
            orchestrator._fine_tune_optimization(
                f"prompt {i}",
                {"content": f"response {i}", "tokens": 100},
                AIProvider.CLAUDE
            )
        
        assert len(orchestrator.fine_tuning_history) == 5


def test_record_usage():
    """Should record usage statistics."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.json"
        config_path.write_text('{}')
        
        orchestrator = AIOrchestrator(str(config_path))
        orchestrator._record_usage(
            AIProvider.CLAUDE,
            {"tokens": 100},
            1.5
        )
        
        stats = orchestrator.get_usage_stats()
        assert "claude" in stats
        assert stats["claude"]["calls"] == 1
        assert stats["claude"]["tokens"] == 100


def test_provider_enum():
    """Should have correct provider enums."""
    assert AIProvider.CLAUDE.value == "claude"
    assert AIProvider.OPENAI.value == "openai"
    assert AIProvider.GEMINI.value == "gemini"


def test_ai_response():
    """Should create AIResponse correctly."""
    response = AIResponse(
        content="test",
        provider=AIProvider.CLAUDE,
        model="claude-sonnet",
        tokens_used=100,
        duration=1.0,
        success=True
    )
    
    assert response.content == "test"
    assert response.provider == AIProvider.CLAUDE
    assert response.success is True


def test_ai_response_error():
    """Should handle error in AIResponse."""
    response = AIResponse(
        content="",
        provider=AIProvider.CLAUDE,
        model="none",
        tokens_used=0,
        duration=0,
        success=False,
        error="Test error"
    )
    
    assert response.success is False
    assert response.error == "Test error"


def test_fine_tuning_disabled():
    """Should not record history when fine-tuning disabled."""
    import json
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.json"
        config = {"ai_providers": {}, "fallback_strategy": {}, "fine_tuning": {"enabled": False}}
        with open(config_path, "w") as f:
            json.dump(config, f)
        
        orchestrator = AIOrchestrator(str(config_path))
        
        initial_len = len(orchestrator.fine_tuning_history)
        orchestrator._fine_tune_optimization(
            "test prompt",
            {"content": "test", "tokens": 100},
            AIProvider.CLAUDE
        )
        
        assert len(orchestrator.fine_tuning_history) == initial_len

