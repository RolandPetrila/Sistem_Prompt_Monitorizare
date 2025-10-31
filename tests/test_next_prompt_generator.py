"""Tests for NextPromptGenerator."""
from core.next_prompt_generator import NextPromptGenerator, PromptSuggestion, TaskType


def test_generate_suggestions():
    """Should generate prompt suggestions."""
    generator = NextPromptGenerator()
    
    context = "Project with Python code"
    suggestions = generator.generate_suggestions(context, max_suggestions=3)
    
    assert len(suggestions) == 3
    assert all(isinstance(s, PromptSuggestion) for s in suggestions)


def test_generate_specific_task_type():
    """Should generate suggestions for specific task types."""
    generator = NextPromptGenerator()
    
    context = "Python project"
    suggestions = generator.generate_suggestions(
        context,
        task_types=[TaskType.CODE_QUALITY, TaskType.TESTING],
        max_suggestions=5
    )
    
    assert len(suggestions) == 2
    assert suggestions[0].task_type in [TaskType.CODE_QUALITY, TaskType.TESTING]
    assert suggestions[1].task_type in [TaskType.CODE_QUALITY, TaskType.TESTING]


def test_suggestions_priority():
    """Should sort suggestions by priority."""
    generator = NextPromptGenerator()
    
    context = "Test project"
    suggestions = generator.generate_suggestions(context, max_suggestions=10)
    
    # Check that priorities are in ascending order
    priorities = [s.priority for s in suggestions]
    assert priorities == sorted(priorities)


def test_generate_custom_prompt():
    """Should generate custom prompt."""
    generator = NextPromptGenerator()
    
    context = "Python project with API"
    custom_instructions = "Focus on REST API endpoints"
    
    prompt = generator.generate_custom_prompt(
        TaskType.CODE_QUALITY,
        context,
        custom_instructions
    )
    
    assert context in prompt
    assert custom_instructions in prompt


def test_prompt_template_formatting():
    """Should format prompt templates correctly."""
    generator = NextPromptGenerator()
    
    context = "Test context"
    suggestions = generator.generate_suggestions(context, max_suggestions=1)
    
    if suggestions:
        prompt = suggestions[0].prompt
        assert context in prompt


def test_task_type_enum():
    """Should have correct task type enums."""
    assert TaskType.CODE_QUALITY.value == "code_quality"
    assert TaskType.REFACTORING.value == "refactoring"
    assert TaskType.TESTING.value == "testing"


def test_prompt_suggestion():
    """Should create PromptSuggestion correctly."""
    suggestion = PromptSuggestion(
        prompt="Test prompt",
        task_type=TaskType.GENERAL,
        priority=1,
        description="Test description"
    )
    
    assert suggestion.prompt == "Test prompt"
    assert suggestion.task_type == TaskType.GENERAL
    assert suggestion.priority == 1


def test_all_task_types():
    """Should support all task types."""
    generator = NextPromptGenerator()
    
    context = "Test project"
    suggestions = generator.generate_suggestions(context, max_suggestions=10)
    
    task_types = [s.task_type for s in suggestions]
    assert len(set(task_types)) > 1  # Should have multiple types


def test_max_suggestions():
    """Should respect max_suggestions limit."""
    generator = NextPromptGenerator()
    
    context = "Test"
    suggestions = generator.generate_suggestions(context, max_suggestions=3)
    
    assert len(suggestions) <= 3


def test_custom_prompt_no_instructions():
    """Should generate prompt without custom instructions."""
    generator = NextPromptGenerator()
    
    context = "Test context"
    prompt = generator.generate_custom_prompt(TaskType.GENERAL, context)
    
    assert context in prompt

