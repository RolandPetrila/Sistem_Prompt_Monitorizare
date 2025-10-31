"""Bug detection task."""
from __future__ import annotations

from typing import Dict, Any, Optional
from core.ai_orchestrator import AIOrchestrator, AIResponse
from core.context_engine import ContextEngine
from core.next_prompt_generator import NextPromptGenerator, TaskType


class FindBugs:
    """
    Finds bugs and issues in code.
    
    Features:
    - Error pattern analysis
    - Edge case detection
    - Potential runtime errors
    - Bug prevention suggestions
    """
    
    def __init__(self, orchestrator: Optional[AIOrchestrator] = None) -> None:
        self.orchestrator = orchestrator or AIOrchestrator()
        self.prompt_generator = NextPromptGenerator()
    
    def find(self, project_path: str, max_tokens: int = 4000) -> AIResponse:
        """
        Find bugs in project.
        
        Args:
            project_path: Path to project
            max_tokens: Maximum tokens for response
        
        Returns:
            AIResponse with bug findings
        """
        context_engine = ContextEngine(project_path)
        context = context_engine.generate_context_prompt("bug_fix")
        
        prompt = self.prompt_generator.generate_custom_prompt(
            TaskType.BUG_FIX,
            context
        )
        
        return self.orchestrator.generate_completion(prompt, max_tokens=max_tokens)
    
    def get_bug_report(self, project_path: str) -> Dict[str, Any]:
        """
        Get bug report.
        
        Args:
            project_path: Path to project
        
        Returns:
            Dictionary with bug report
        """
        response = self.find(project_path)
        
        return {
            "success": response.success,
            "bugs": response.content,
            "provider": response.provider.value,
            "tokens_used": response.tokens_used,
            "error": response.error
        }


__all__ = ["FindBugs"]

