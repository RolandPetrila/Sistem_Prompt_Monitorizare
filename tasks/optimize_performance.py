"""Performance optimization task."""
from __future__ import annotations

from typing import Dict, Any, Optional
from core.ai_orchestrator import AIOrchestrator, AIResponse
from core.context_engine import ContextEngine
from core.next_prompt_generator import NextPromptGenerator, TaskType


class OptimizePerformance:
    """
    Optimizes code performance.
    
    Features:
    - Bottleneck identification
    - Algorithm optimization
    - Caching strategies
    - I/O optimization
    """
    
    def __init__(self, orchestrator: Optional[AIOrchestrator] = None) -> None:
        self.orchestrator = orchestrator or AIOrchestrator()
        self.prompt_generator = NextPromptGenerator()
    
    def optimize(self, project_path: str, max_tokens: int = 4000) -> AIResponse:
        """
        Analyze and optimize performance.
        
        Args:
            project_path: Path to project
            max_tokens: Maximum tokens for response
        
        Returns:
            AIResponse with optimization suggestions
        """
        context_engine = ContextEngine(project_path)
        context = context_engine.generate_context_prompt("optimization")
        
        prompt = self.prompt_generator.generate_custom_prompt(
            TaskType.OPTIMIZATION,
            context
        )
        
        return self.orchestrator.generate_completion(prompt, max_tokens=max_tokens)
    
    def get_optimization_report(self, project_path: str) -> Dict[str, Any]:
        """
        Get performance optimization report.
        
        Args:
            project_path: Path to project
        
        Returns:
            Dictionary with optimization suggestions
        """
        response = self.optimize(project_path)
        
        return {
            "success": response.success,
            "optimizations": response.content,
            "provider": response.provider.value,
            "tokens_used": response.tokens_used,
            "error": response.error
        }


__all__ = ["OptimizePerformance"]

