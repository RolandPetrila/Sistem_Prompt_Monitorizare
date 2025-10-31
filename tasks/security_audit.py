"""Security audit task."""
from __future__ import annotations

from typing import Dict, Any, Optional
from core.ai_orchestrator import AIOrchestrator, AIResponse
from core.context_engine import ContextEngine
from core.next_prompt_generator import NextPromptGenerator, TaskType


class SecurityAudit:
    """
    Performs security audit of code.
    
    Features:
    - Vulnerability detection
    - Authentication review
    - SQL injection checks
    - XSS prevention
    """
    
    def __init__(self, orchestrator: Optional[AIOrchestrator] = None) -> None:
        self.orchestrator = orchestrator or AIOrchestrator()
        self.prompt_generator = NextPromptGenerator()
    
    def audit(self, project_path: str, max_tokens: int = 4000) -> AIResponse:
        """
        Perform security audit.
        
        Args:
            project_path: Path to project
            max_tokens: Maximum tokens for response
        
        Returns:
            AIResponse with security findings
        """
        context_engine = ContextEngine(project_path)
        context = context_engine.generate_context_prompt("security")
        
        prompt = self.prompt_generator.generate_custom_prompt(
            TaskType.SECURITY,
            context
        )
        
        return self.orchestrator.generate_completion(prompt, max_tokens=max_tokens)
    
    def get_security_report(self, project_path: str) -> Dict[str, Any]:
        """
        Get security audit report.
        
        Args:
            project_path: Path to project
        
        Returns:
            Dictionary with security findings
        """
        response = self.audit(project_path)
        
        return {
            "success": response.success,
            "security_issues": response.content,
            "provider": response.provider.value,
            "tokens_used": response.tokens_used,
            "error": response.error
        }


__all__ = ["SecurityAudit"]

