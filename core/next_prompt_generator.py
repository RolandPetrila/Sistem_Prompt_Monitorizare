"""Next prompt generator for AI suggestions."""
from __future__ import annotations

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class TaskType(Enum):
    """Available task types."""
    CODE_QUALITY = "code_quality"
    REFACTORING = "refactoring"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    BUG_FIX = "bug_fix"
    OPTIMIZATION = "optimization"
    SECURITY = "security"
    GENERAL = "general"


@dataclass
class PromptSuggestion:
    """Prompt suggestion with metadata."""
    prompt: str
    task_type: TaskType
    priority: int
    description: str
    context: Optional[Dict[str, Any]] = None


class NextPromptGenerator:
    """
    Generates next prompt suggestions based on context.
    
    Features:
    - Context-aware suggestions
    - Task type prioritization
    - Prompt templates
    - History awareness
    """
    
    def __init__(self) -> None:
        self._prompt_templates = self._load_templates()
    
    def _load_templates(self) -> Dict[TaskType, str]:
        """Load prompt templates for different task types."""
        return {
            TaskType.CODE_QUALITY: """Analyze the code quality of this project:
- Check for code smells and anti-patterns
- Evaluate code organization and structure
- Suggest improvements for maintainability
- Review naming conventions and documentation

Project Context:
{context}""",
            
            TaskType.REFACTORING: """Suggest refactoring opportunities for this codebase:
- Identify duplicate code
- Suggest design pattern improvements
- Recommend code simplification
- Highlight areas for better abstraction

Project Context:
{context}""",
            
            TaskType.TESTING: """Generate comprehensive tests for this project:
- Identify test coverage gaps
- Suggest unit tests for critical components
- Recommend integration test scenarios
- Create test data and fixtures

Project Context:
{context}""",
            
            TaskType.DOCUMENTATION: """Improve documentation for this project:
- Generate docstrings for functions and classes
- Create comprehensive README
- Document API endpoints and usage
- Add code comments where needed

Project Context:
{context}""",
            
            TaskType.BUG_FIX: """Identify and fix bugs in this project:
- Analyze error patterns and logs
- Review edge cases and boundary conditions
- Suggest fixes for identified issues
- Prevent similar bugs in the future

Project Context:
{context}""",
            
            TaskType.OPTIMIZATION: """Optimize performance of this codebase:
- Identify performance bottlenecks
- Suggest algorithmic improvements
- Recommend caching strategies
- Optimize database queries and I/O operations

Project Context:
{context}""",
            
            TaskType.SECURITY: """Perform security audit of this project:
- Identify security vulnerabilities
- Review authentication and authorization
- Check for SQL injection and XSS risks
- Suggest security best practices

Project Context:
{context}""",
            
            TaskType.GENERAL: """Analyze and improve this project:
{context}

Please provide comprehensive analysis and suggestions for improvement."""
        }
    
    def generate_suggestions(
        self,
        context: str,
        task_types: Optional[List[TaskType]] = None,
        max_suggestions: int = 5
    ) -> List[PromptSuggestion]:
        """
        Generate prompt suggestions.
        
        Args:
            context: Project context string
            task_types: List of task types to generate (None = all)
            max_suggestions: Maximum number of suggestions
        
        Returns:
            List of prompt suggestions
        """
        if task_types is None:
            task_types = list(TaskType)
        
        suggestions = []
        
        # Priority mapping (lower = higher priority)
        priority_map = {
            TaskType.BUG_FIX: 1,
            TaskType.SECURITY: 2,
            TaskType.CODE_QUALITY: 3,
            TaskType.TESTING: 4,
            TaskType.OPTIMIZATION: 5,
            TaskType.REFACTORING: 6,
            TaskType.DOCUMENTATION: 7,
            TaskType.GENERAL: 8
        }
        
        for task_type in task_types[:max_suggestions]:
            template = self._prompt_templates.get(task_type, "")
            
            prompt = template.format(context=context) if "{context}" in template else template + "\n\n" + context
            
            suggestion = PromptSuggestion(
                prompt=prompt,
                task_type=task_type,
                priority=priority_map.get(task_type, 9),
                description=self._get_description(task_type),
                context={"context_length": len(context)}
            )
            
            suggestions.append(suggestion)
        
        # Sort by priority
        suggestions.sort(key=lambda x: x.priority)
        
        return suggestions[:max_suggestions]
    
    def _get_description(self, task_type: TaskType) -> str:
        """Get description for task type."""
        descriptions = {
            TaskType.CODE_QUALITY: "Analyze and improve code quality",
            TaskType.REFACTORING: "Refactor code for better structure",
            TaskType.TESTING: "Generate comprehensive tests",
            TaskType.DOCUMENTATION: "Improve project documentation",
            TaskType.BUG_FIX: "Identify and fix bugs",
            TaskType.OPTIMIZATION: "Optimize performance",
            TaskType.SECURITY: "Perform security audit",
            TaskType.GENERAL: "General project analysis"
        }
        return descriptions.get(task_type, "Analyze project")
    
    def generate_custom_prompt(
        self,
        task_type: TaskType,
        context: str,
        custom_instructions: Optional[str] = None
    ) -> str:
        """
        Generate custom prompt with specific instructions.
        
        Args:
            task_type: Task type
            context: Project context
            custom_instructions: Additional custom instructions
        
        Returns:
            Generated prompt string
        """
        base_template = self._prompt_templates.get(task_type, "")
        
        prompt = base_template.format(context=context) if "{context}" in base_template else base_template + "\n\n" + context
        
        if custom_instructions:
            prompt += f"\n\nAdditional Instructions:\n{custom_instructions}"
        
        return prompt


__all__ = ["NextPromptGenerator", "PromptSuggestion", "TaskType"]

