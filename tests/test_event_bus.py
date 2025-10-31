"""Tests for EventBus."""
from core.event_bus import EventBus


def test_singleton():
    """EventBus should be singleton."""
    bus1 = EventBus()
    bus2 = EventBus()
    assert bus1 is bus2


def test_subscribe_and_emit():
    """Should call subscriber when event emitted."""
    bus = EventBus()
    bus.clear_all()
    
    results = []
    def handler(data):
        results.append(data)
    
    bus.subscribe("test_event", handler)
    bus.emit("test_event", {"value": 42})
    
    assert len(results) == 1
    assert results[0]["value"] == 42


def test_unsubscribe():
    """Should not call unsubscribed handler."""
    bus = EventBus()
    bus.clear_all()
    
    results = []
    def handler(data):
        results.append(data)
    
    bus.subscribe("test", handler)
    bus.emit("test", 1)
    bus.unsubscribe("test", handler)
    bus.emit("test", 2)
    
    assert len(results) == 1
    assert results[0] == 1


def test_multiple_subscribers():
    """Should call all subscribers."""
    bus = EventBus()
    bus.clear_all()
    
    results = []
    
    bus.subscribe("multi", lambda d: results.append(d * 2))
    bus.subscribe("multi", lambda d: results.append(d * 3))
    
    bus.emit("multi", 10)
    
    assert len(results) == 2
    assert 20 in results
    assert 30 in results


def test_error_handling():
    """Should continue on handler error."""
    bus = EventBus()
    bus.clear_all()
    
    results = []
    
    def bad_handler(data):
        raise ValueError("Oops")
    
    def good_handler(data):
        results.append(data)
    
    bus.subscribe("err", bad_handler)
    bus.subscribe("err", good_handler)
    
    bus.emit("err", 42)
    
    assert len(results) == 1
    assert results[0] == 42

