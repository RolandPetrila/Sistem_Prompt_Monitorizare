"""Code refactoring task."""
from __future__ import annotations

from typing import Dict, Any, Optional
from core.ai_orchestrator import AIOrchestrator, AIResponse
from core.context_engine import ContextEngine
from core.next_prompt_generator import NextPromptGenerator, TaskType


class RefactorCode:
    """
    Refactors code for better structure.
    
    Features:
    - Duplicate code elimination
    - Design pattern suggestions
    - Code simplification
    - Better abstraction
    """
    
    def __init__(self, orchestrator: Optional[AIOrchestrator] = None) -> None:
        self.orchestrator = orchestrator or AIOrchestrator()
        self.prompt_generator = NextPromptGenerator()
    
    def refactor(self, project_path: str, max_tokens: int = 4000) -> AIResponse:
        """
        Suggest refactoring opportunities.
        
        Args:
            project_path: Path to project
            max_tokens: Maximum tokens for response
        
        Returns:
            AIResponse with refactoring suggestions
        """
        context_engine = ContextEngine(project_path)
        context = context_engine.generate_context_prompt("refactoring")
        
        prompt = self.prompt_generator.generate_custom_prompt(
            TaskType.REFACTORING,
            context
        )
        
        return self.orchestrator.generate_completion(prompt, max_tokens=max_tokens)
    
    def get_refactoring_suggestions(self, project_path: str) -> Dict[str, Any]:
        """
        Get refactoring suggestions.
        
        Args:
            project_path: Path to project
        
        Returns:
            Dictionary with refactoring suggestions
        """
        response = self.refactor(project_path)
        
        return {
            "success": response.success,
            "suggestions": response.content,
            "provider": response.provider.value,
            "tokens_used": response.tokens_used,
            "error": response.error
        }


__all__ = ["RefactorCode"]

