"""Performance profiling task."""
from __future__ import annotations

from typing import Dict, Any, Optional
from core.ai_orchestrator import AIOrchestrator, AIResponse
from core.context_engine import ContextEngine


class PerformanceProfiling:
    """
    Profiles code performance.
    
    Features:
    - Performance bottlenecks
    - Memory usage analysis
    - CPU profiling suggestions
    - Optimization opportunities
    """
    
    def __init__(self, orchestrator: Optional[AIOrchestrator] = None) -> None:
        self.orchestrator = orchestrator or AIOrchestrator()
    
    def profile(self, project_path: str, max_tokens: int = 4000) -> AIResponse:
        """
        Profile code performance.
        
        Args:
            project_path: Path to project
            max_tokens: Maximum tokens for response
        
        Returns:
            AIResponse with profiling results
        """
        context_engine = ContextEngine(project_path)
        structure = context_engine.analyze_project_structure()
        recent_changes = context_engine.get_recent_changes(days=7)
        
        prompt = f"""Profile performance for this project:

## Project Structure
- Total Files: {structure.get('total_files', 0)}
- File Types: {', '.join(sorted(structure.get('file_types', {}).keys(), key=lambda x: -structure.get('file_types', {}).get(x, 0))[:10])}

## Recently Modified Files:
{chr(10).join(f"- {change['path']} (modified: {change['modified']})" for change in recent_changes[:10])}

Please provide:
1. Potential performance bottlenecks
2. Memory usage analysis
3. CPU profiling recommendations
4. Optimization opportunities
5. Profiling tools suggestions
"""
        
        return self.orchestrator.generate_completion(prompt, max_tokens=max_tokens)
    
    def get_profile_report(self, project_path: str) -> Dict[str, Any]:
        """
        Get performance profile report.
        
        Args:
            project_path: Path to project
        
        Returns:
            Dictionary with profiling results
        """
        response = self.profile(project_path)
        
        return {
            "success": response.success,
            "profile": response.content,
            "provider": response.provider.value,
            "tokens_used": response.tokens_used,
            "error": response.error
        }


__all__ = ["PerformanceProfiling"]

