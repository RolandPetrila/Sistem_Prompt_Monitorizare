"""
Multi-AI orchestrator with automatic fallback.
Supports: Claude, OpenAI, Gemini, Perplexity
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import openai
except ImportError:
    openai = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None


class AIProvider(Enum):
    """Available AI providers."""
    CLAUDE = "claude"
    OPENAI = "openai"
    GEMINI = "gemini"
    PERPLEXITY = "perplexity"


@dataclass
class AIResponse:
    """AI response with metadata."""
    content: str
    provider: AIProvider
    model: str
    tokens_used: int
    duration: float
    success: bool
    error: Optional[str] = None


class AIOrchestrator:
    """
    Multi-AI orchestrator cu fallback automat.
    
    Features:
    - Auto-fallback între providers
    - Retry logic cu exponential backoff
    - Usage tracking
    - Fine-tuning optimization (NEW)
    
    Example:
        >>> orchestrator = AIOrchestrator()
        >>> response = orchestrator.generate_completion("Explain Python")
        >>> print(response.content)
    """
    
    def __init__(self, config_path: str = "config_local.json") -> None:
        self.config = self._load_config(config_path)
        self.claude_client = None
        self.claude_model = None
        self.openai_model = None
        self.gemini_model = None
        self._init_providers()
        self.usage_stats: Dict[str, Any] = {}
        self.fine_tuning_history: List[Dict] = []
    
    def _load_config(self, path: str) -> Dict[str, Any]:
        """Load configuration from file."""
        config_file = Path(path)
        if not config_file.exists():
            # Return default config
            return {
                "ai_providers": {
                    "claude": {"api_key": "", "model": "claude-sonnet-4-20250514", "priority": 1, "enabled": False},
                    "openai": {"api_key": "", "model": "gpt-4-turbo-preview", "priority": 2, "enabled": False},
                    "gemini": {"api_key": "", "model": "gemini-1.5-pro", "priority": 3, "enabled": False},
                },
                "fallback_strategy": {"enabled": True, "retry_count": 3, "timeout": 30, "auto_switch": True},
                "fine_tuning": {"enabled": True, "learning_rate": 0.001, "history_size": 100, "optimization_threshold": 0.7}
            }
        
        with open(config_file, "r") as f:
            return json.load(f)
    
    def _init_providers(self) -> None:
        """Initialize AI provider clients."""
        providers = self.config.get("ai_providers", {})
        
        # Claude
        if providers.get("claude", {}).get("enabled") and anthropic:
            claude_key = providers["claude"].get("api_key", "")
            if claude_key and not claude_key.startswith("PLACEHOLDER") and claude_key.strip():
                try:
                    self.claude_client = anthropic.Anthropic(api_key=claude_key)
                    self.claude_model = providers["claude"].get("model", "claude-sonnet-4-20250514")
                except Exception as e:
                    print(f"⚠️  Failed to initialize Claude: {e}")
        
        # OpenAI
        if providers.get("openai", {}).get("enabled") and openai:
            openai_key = providers["openai"].get("api_key", "")
            if openai_key and not openai_key.startswith("PLACEHOLDER") and openai_key.strip():
                try:
                    openai.api_key = openai_key
                    self.openai_model = providers["openai"].get("model", "gpt-4-turbo-preview")
                except Exception as e:
                    print(f"⚠️  Failed to initialize OpenAI: {e}")
        
        # Gemini
        if providers.get("gemini", {}).get("enabled") and genai:
            gemini_key = providers["gemini"].get("api_key", "")
            if gemini_key and not gemini_key.startswith("PLACEHOLDER") and gemini_key.strip():
                try:
                    genai.configure(api_key=gemini_key)
                    self.gemini_model = providers["gemini"].get("model", "gemini-1.5-pro")
                except Exception as e:
                    print(f"⚠️  Failed to initialize Gemini: {e}")
    
    def generate_completion(
        self,
        prompt: str,
        preferred_provider: Optional[AIProvider] = None,
        max_tokens: int = 4000
    ) -> AIResponse:
        """
        Generate completion cu fallback automat.
        
        Args:
            prompt: User prompt
            preferred_provider: Preferred AI (None = auto-select by priority)
            max_tokens: Max tokens în response
        
        Returns:
            AIResponse with content and metadata
        """
        # Determine providers order by priority
        providers_config = self.config.get("ai_providers", {})
        providers_sorted = sorted(
            providers_config.items(),
            key=lambda x: x[1].get("priority", 999)
        )
        
        # If preferred, try that first
        if preferred_provider:
            providers_sorted = [
                (preferred_provider.value, providers_config.get(preferred_provider.value, {}))
            ] + [p for p in providers_sorted if p[0] != preferred_provider.value]
        
        # Try each provider in order
        fallback_config = self.config.get("fallback_strategy", {})
        retry_count = fallback_config.get("retry_count", 3)
        timeout = fallback_config.get("timeout", 30)
        
        last_error = None
        
        for provider_name, provider_config in providers_sorted:
            if not provider_config.get("enabled"):
                continue
            
            provider_enum = AIProvider(provider_name) if provider_name in [p.value for p in AIProvider] else None
            if not provider_enum:
                continue
            
            for attempt in range(retry_count):
                try:
                    start_time = time.time()
                    
                    if provider_enum == AIProvider.CLAUDE:
                        response = self._call_claude(prompt, max_tokens, timeout)
                    elif provider_enum == AIProvider.OPENAI:
                        response = self._call_openai(prompt, max_tokens, timeout)
                    elif provider_enum == AIProvider.GEMINI:
                        response = self._call_gemini(prompt, max_tokens, timeout)
                    else:
                        continue  # Perplexity not implemented yet
                    
                    duration = time.time() - start_time
                    
                    # Success! Record and return
                    self._record_usage(provider_enum, response, duration)
                    self._fine_tune_optimization(prompt, response, provider_enum)
                    
                    return AIResponse(
                        content=response["content"],
                        provider=provider_enum,
                        model=response["model"],
                        tokens_used=response["tokens"],
                        duration=duration,
                        success=True
                    )
                
                except Exception as e:
                    last_error = str(e)
                    print(f"⚠️  {provider_enum.value} attempt {attempt+1} failed: {e}")
                    
                    if attempt < retry_count - 1:
                        time.sleep(2 ** attempt)  # Exponential backoff
        
        # All providers failed
        return AIResponse(
            content="",
            provider=AIProvider.CLAUDE,  # Default
            model="none",
            tokens_used=0,
            duration=0,
            success=False,
            error=f"All providers failed. Last error: {last_error}"
        )
    
    def _call_claude(self, prompt: str, max_tokens: int, timeout: int) -> Dict[str, Any]:
        """Call Claude API."""
        if not self.claude_client:
            raise ValueError("Claude not configured")
        
        response = self.claude_client.messages.create(
            model=self.claude_model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
            timeout=timeout
        )
        
        return {
            "content": response.content[0].text,
            "model": self.claude_model,
            "tokens": response.usage.input_tokens + response.usage.output_tokens
        }
    
    def _call_openai(self, prompt: str, max_tokens: int, timeout: int) -> Dict[str, Any]:
        """Call OpenAI API."""
        if not openai or not openai.api_key:
            raise ValueError("OpenAI not configured")
        
        # For OpenAI SDK v1.x
        response = openai.chat.completions.create(
            model=self.openai_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            timeout=timeout
        )
        
        return {
            "content": response.choices[0].message.content,
            "model": self.openai_model,
            "tokens": response.usage.total_tokens
        }
    
    def _call_gemini(self, prompt: str, max_tokens: int, timeout: int) -> Dict[str, Any]:
        """Call Gemini API."""
        if not genai or not self.gemini_model:
            raise ValueError("Gemini not configured")
        
        model = genai.GenerativeModel(self.gemini_model)
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_tokens
            )
        )
        
        return {
            "content": response.text,
            "model": self.gemini_model,
            "tokens": 0  # Gemini doesn't return token count easily
        }
    
    def _record_usage(self, provider: AIProvider, response: Dict, duration: float) -> None:
        """Record usage statistics."""
        provider_name = provider.value
        
        if provider_name not in self.usage_stats:
            self.usage_stats[provider_name] = {
                "calls": 0,
                "tokens": 0,
                "duration": 0,
                "errors": 0
            }
        
        self.usage_stats[provider_name]["calls"] += 1
        self.usage_stats[provider_name]["tokens"] += response["tokens"]
        self.usage_stats[provider_name]["duration"] += duration
    
    def _fine_tune_optimization(
        self,
        prompt: str,
        response: Dict,
        provider: AIProvider
    ) -> None:
        """
        Record prompt-response pairs pentru fine-tuning.
        FEATURE NOU: AI model fine-tuning pentru prompturi optimizate.
        """
        fine_tuning_config = self.config.get("fine_tuning", {})
        if not fine_tuning_config.get("enabled"):
            return
        
        # Store în history pentru training ulterior
        self.fine_tuning_history.append({
            "prompt": prompt,
            "response": response["content"],
            "provider": provider.value,
            "tokens": response["tokens"],
            "timestamp": time.time()
        })
        
        # Keep only recent history
        history_size = fine_tuning_config.get("history_size", 100)
        if len(self.fine_tuning_history) > history_size:
            self.fine_tuning_history = self.fine_tuning_history[-history_size:]
    
    def export_fine_tuning_data(self, output_path: str = "fine_tuning_data.jsonl") -> None:
        """
        Export training data pentru fine-tuning.
        Format: JSONL (JSON Lines) compatibil cu OpenAI/Anthropic fine-tuning APIs.
        """
        with open(output_path, "w") as f:
            for entry in self.fine_tuning_history:
                json_line = json.dumps({
                    "messages": [
                        {"role": "user", "content": entry["prompt"]},
                        {"role": "assistant", "content": entry["response"]}
                    ],
                    "metadata": {
                        "provider": entry["provider"],
                        "tokens": entry["tokens"]
                    }
                })
                f.write(json_line + "\n")
        
        print(f"✅ Exported {len(self.fine_tuning_history)} training examples to {output_path}")
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics."""
        return self.usage_stats


__all__ = ["AIOrchestrator", "AIProvider", "AIResponse"]

