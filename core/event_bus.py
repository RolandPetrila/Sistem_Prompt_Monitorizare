"""Event bus for decoupled communication between components."""
from __future__ import annotations

from typing import Callable, Dict, List, Any
from threading import Lock


class EventBus:
    """
    Singleton event bus for publish-subscribe pattern.
    
    Example:
        >>> bus = EventBus()
        >>> def handler(data): print(f"Got: {data}")
        >>> bus.subscribe("my_event", handler)
        >>> bus.emit("my_event", {"key": "value"})
    """
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls) -> EventBus:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._subscribers: Dict[str, List[Callable]] = {}
        return cls._instance
    
    def subscribe(self, event_type: str, callback: Callable) -> None:
        """Subscribe callback to event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        if callback not in self._subscribers[event_type]:
            self._subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """Unsubscribe callback from event type."""
        if event_type in self._subscribers:
            if callback in self._subscribers[event_type]:
                self._subscribers[event_type].remove(callback)
    
    def emit(self, event_type: str, data: Any = None) -> None:
        """Emit event to all subscribers."""
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Error in event handler: {e}")
    
    def clear_all(self) -> None:
        """Clear all subscriptions (useful for testing)."""
        self._subscribers.clear()


__all__ = ["EventBus"]

