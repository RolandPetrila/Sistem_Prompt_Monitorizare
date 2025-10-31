"""Documentation generation task."""
from __future__ import annotations

from typing import Dict, Any, Optional
from core.ai_orchestrator import AIOrchestrator, AIResponse
from core.context_engine import ContextEngine
from core.next_prompt_generator import NextPromptGenerator, TaskType


class DocumentationGenerator:
    """
    Generates documentation for code.
    
    Features:
    - Docstring generation
    - README creation
    - API documentation
    - Code comments
    """
    
    def __init__(self, orchestrator: Optional[AIOrchestrator] = None) -> None:
        self.orchestrator = orchestrator or AIOrchestrator()
        self.prompt_generator = NextPromptGenerator()
    
    def generate(self, project_path: str, max_tokens: int = 4000) -> AIResponse:
        """
        Generate documentation for project.
        
        Args:
            project_path: Path to project
            max_tokens: Maximum tokens for response
        
        Returns:
            AIResponse with documentation
        """
        context_engine = ContextEngine(project_path)
        context = context_engine.generate_context_prompt("documentation")
        
        prompt = self.prompt_generator.generate_custom_prompt(
            TaskType.DOCUMENTATION,
            context
        )
        
        return self.orchestrator.generate_completion(prompt, max_tokens=max_tokens)
    
    def get_documentation(self, project_path: str) -> Dict[str, Any]:
        """
        Get generated documentation.
        
        Args:
            project_path: Path to project
        
        Returns:
            Dictionary with documentation
        """
        response = self.generate(project_path)
        
        return {
            "success": response.success,
            "documentation": response.content,
            "provider": response.provider.value,
            "tokens_used": response.tokens_used,
            "error": response.error
        }


__all__ = ["DocumentationGenerator"]

