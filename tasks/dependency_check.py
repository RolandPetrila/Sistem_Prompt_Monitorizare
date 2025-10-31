"""Dependency checking task."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from core.ai_orchestrator import AIOrchestrator, AIResponse


class DependencyCheck:
    """
    Checks project dependencies.
    
    Features:
    - Dependency analysis
    - Version checking
    - Security vulnerabilities
    - Outdated packages
    """
    
    def __init__(self, orchestrator: Optional[AIOrchestrator] = None) -> None:
        self.orchestrator = orchestrator or AIOrchestrator()
    
    def check(self, project_path: str, max_tokens: int = 4000) -> AIResponse:
        """
        Check project dependencies.
        
        Args:
            project_path: Path to project
            max_tokens: Maximum tokens for response
        
        Returns:
            AIResponse with dependency analysis
        """
        project_path = Path(project_path)
        dependencies = []
        
        # Check for requirements.txt
        req_file = project_path / "requirements.txt"
        if req_file.exists():
            with open(req_file, "r") as f:
                dependencies = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        
        # Check for package.json
        package_json = project_path / "package.json"
        if package_json.exists():
            with open(package_json, "r") as f:
                data = json.load(f)
                deps = data.get("dependencies", {})
                dev_deps = data.get("devDependencies", {})
                dependencies.extend([f"{k}@{v}" for k, v in {**deps, **dev_deps}.items()])
        
        prompt = f"""Analyze dependencies for this project:

## Dependencies Found:
{chr(10).join(f"- {dep}" for dep in dependencies[:50])}

Please provide:
1. Security vulnerabilities
2. Outdated packages
3. Dependency conflicts
4. Recommendations for updates
5. Best practices
"""
        
        return self.orchestrator.generate_completion(prompt, max_tokens=max_tokens)
    
    def get_dependency_report(self, project_path: str) -> Dict[str, Any]:
        """
        Get dependency check report.
        
        Args:
            project_path: Path to project
        
        Returns:
            Dictionary with dependency analysis
        """
        response = self.check(project_path)
        
        return {
            "success": response.success,
            "report": response.content,
            "provider": response.provider.value,
            "tokens_used": response.tokens_used,
            "error": response.error
        }


__all__ = ["DependencyCheck"]

