"""Code quality analysis task."""
from __future__ import annotations

from typing import Dict, Any, Optional
from core.ai_orchestrator import AIOrchestrator, AIResponse
from core.context_engine import ContextEngine
from core.next_prompt_generator import NextPromptGenerator, TaskType


class AnalyzeCodeQuality:
    """
    Analyzes code quality of a project.
    
    Features:
    - Code smell detection
    - Best practices review
    - Maintainability analysis
    - Suggestions for improvement
    """
    
    def __init__(self, orchestrator: Optional[AIOrchestrator] = None) -> None:
        self.orchestrator = orchestrator or AIOrchestrator()
        self.prompt_generator = NextPromptGenerator()
    
    def analyze(self, project_path: str, max_tokens: int = 4000) -> AIResponse:
        """
        Analyze code quality of a project.
        
        Args:
            project_path: Path to project
            max_tokens: Maximum tokens for response
        
        Returns:
            AIResponse with analysis results
        """
        context_engine = ContextEngine(project_path)
        context = context_engine.generate_context_prompt("code_quality")
        
        prompt = self.prompt_generator.generate_custom_prompt(
            TaskType.CODE_QUALITY,
            context
        )
        
        return self.orchestrator.generate_completion(prompt, max_tokens=max_tokens)
    
    def get_suggestions(self, project_path: str) -> Dict[str, Any]:
        """
        Get code quality suggestions.
        
        Args:
            project_path: Path to project
        
        Returns:
            Dictionary with suggestions
        """
        response = self.analyze(project_path)
        
        return {
            "success": response.success,
            "analysis": response.content,
            "provider": response.provider.value,
            "tokens_used": response.tokens_used,
            "error": response.error
        }


__all__ = ["AnalyzeCodeQuality"]

