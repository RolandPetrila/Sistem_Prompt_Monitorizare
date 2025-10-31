"""Code style fixing task."""
from __future__ import annotations

from typing import Dict, Any, Optional
from core.ai_orchestrator import AIOrchestrator, AIResponse
from core.context_engine import ContextEngine


class CodeStyleFix:
    """
    Fixes code style issues.
    
    Features:
    - PEP8/PEP484 compliance
    - Naming conventions
    - Formatting fixes
    - Style consistency
    """
    
    def __init__(self, orchestrator: Optional[AIOrchestrator] = None) -> None:
        self.orchestrator = orchestrator or AIOrchestrator()
    
    def fix(self, project_path: str, max_tokens: int = 4000) -> AIResponse:
        """
        Fix code style issues.
        
        Args:
            project_path: Path to project
            max_tokens: Maximum tokens for response
        
        Returns:
            AIResponse with style fixes
        """
        context_engine = ContextEngine(project_path)
        context = context_engine.generate_context_prompt("code_quality")
        
        prompt = f"""{context}

Please analyze and fix code style issues:
1. PEP8/PEP484 compliance for Python
2. Naming conventions
3. Code formatting
4. Import organization
5. Docstring formatting
6. Type hints consistency

Provide specific fixes with code examples.
"""
        
        return self.orchestrator.generate_completion(prompt, max_tokens=max_tokens)
    
    def get_style_fixes(self, project_path: str) -> Dict[str, Any]:
        """
        Get code style fixes.
        
        Args:
            project_path: Path to project
        
        Returns:
            Dictionary with style fixes
        """
        response = self.fix(project_path)
        
        return {
            "success": response.success,
            "fixes": response.content,
            "provider": response.provider.value,
            "tokens_used": response.tokens_used,
            "error": response.error
        }


__all__ = ["CodeStyleFix"]

