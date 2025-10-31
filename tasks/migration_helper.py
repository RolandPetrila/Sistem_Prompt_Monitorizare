"""Migration helper task."""
from __future__ import annotations

from typing import Dict, Any, Optional
from core.ai_orchestrator import AIOrchestrator, AIResponse
from core.context_engine import ContextEngine


class MigrationHelper:
    """
    Helps with code migrations.
    
    Features:
    - Framework migration
    - Version upgrade guides
    - Breaking changes analysis
    - Migration steps
    """
    
    def __init__(self, orchestrator: Optional[AIOrchestrator] = None) -> None:
        self.orchestrator = orchestrator or AIOrchestrator()
    
    def help_migrate(self, project_path: str, target_framework: str = "", max_tokens: int = 4000) -> AIResponse:
        """
        Help with migration.
        
        Args:
            project_path: Path to project
            target_framework: Target framework/version
            max_tokens: Maximum tokens for response
        
        Returns:
            AIResponse with migration guide
        """
        context_engine = ContextEngine(project_path)
        structure = context_engine.analyze_project_structure()
        
        prompt = f"""Help migrate this project{f" to {target_framework}" if target_framework else ""}:

## Project Structure
- Root: {structure.get('root', 'N/A')}
- Total Files: {structure.get('total_files', 0)}
- File Types: {', '.join(structure.get('file_types', {}).keys())[:10]}

## Key Files:
{chr(10).join(f"- {file}" for file in [f for f in structure.get('files', []) if any(f.endswith(ext) for ext in ['.py', '.js', '.ts'])][:20])}

Please provide:
1. Migration strategy
2. Step-by-step guide
3. Breaking changes to watch for
4. Code examples for migration
5. Testing recommendations
"""
        
        return self.orchestrator.generate_completion(prompt, max_tokens=max_tokens)
    
    def get_migration_guide(self, project_path: str, target_framework: str = "") -> Dict[str, Any]:
        """
        Get migration guide.
        
        Args:
            project_path: Path to project
            target_framework: Target framework/version
        
        Returns:
            Dictionary with migration guide
        """
        response = self.help_migrate(project_path, target_framework)
        
        return {
            "success": response.success,
            "guide": response.content,
            "provider": response.provider.value,
            "tokens_used": response.tokens_used,
            "error": response.error
        }


__all__ = ["MigrationHelper"]

