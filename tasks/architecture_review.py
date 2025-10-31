"""Architecture review task."""
from __future__ import annotations

from typing import Dict, Any, Optional
from core.ai_orchestrator import AIOrchestrator, AIResponse
from core.context_engine import ContextEngine


class ArchitectureReview:
    """
    Reviews project architecture.
    
    Features:
    - Architecture pattern analysis
    - Design review
    - Scalability assessment
    - Best practices check
    """
    
    def __init__(self, orchestrator: Optional[AIOrchestrator] = None) -> None:
        self.orchestrator = orchestrator or AIOrchestrator()
    
    def review(self, project_path: str, max_tokens: int = 4000) -> AIResponse:
        """
        Review project architecture.
        
        Args:
            project_path: Path to project
            max_tokens: Maximum tokens for response
        
        Returns:
            AIResponse with architecture review
        """
        context_engine = ContextEngine(project_path)
        structure = context_engine.analyze_project_structure()
        
        prompt = f"""Review the architecture of this project:

## Project Structure
- Root: {structure.get('root', 'N/A')}
- Total Files: {structure.get('total_files', 0)}
- Directories: {len(structure.get('directories', []))}

## File Types:
{chr(10).join(f"- {ext}: {count} files" for ext, count in sorted(structure.get('file_types', {}).items(), key=lambda x: -x[1])[:10])}

## Key Files:
{chr(10).join(f"- {file}" for file in [f for f in structure.get('files', []) if any(f.endswith(ext) for ext in ['.py', '.js', '.ts', '.java', '.go'])][:20])}

Please provide:
1. Architecture pattern analysis
2. Design strengths and weaknesses
3. Scalability assessment
4. Recommendations for improvement
"""
        
        return self.orchestrator.generate_completion(prompt, max_tokens=max_tokens)
    
    def get_review(self, project_path: str) -> Dict[str, Any]:
        """
        Get architecture review.
        
        Args:
            project_path: Path to project
        
        Returns:
            Dictionary with architecture review
        """
        response = self.review(project_path)
        
        return {
            "success": response.success,
            "review": response.content,
            "provider": response.provider.value,
            "tokens_used": response.tokens_used,
            "error": response.error
        }


__all__ = ["ArchitectureReview"]

