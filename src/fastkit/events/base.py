from typing import Any, Dict, List, Optional, Type, Generic, TypeVar
from functools import wraps
from abc import ABC, abstractmethod
from src.fastkit.routers.base import T  # Import the BaseRouter class from your routers.

class BaseEvent(ABC, Generic[T]):
    """
    Base event class for handling domain events.
    """
    @abstractmethod
    def emit(self, event_type: str, data: Dict[str, Any]) -> None:
        """Emit an event to the message queue."""
        pass

class QueueBase(ABC):
    """
    Abstract base class for event queues (e.g., RabbitMQ, Kafka, etc.).
    """
    
    @abstractmethod
    def publish(self, event_type: str, payload: Dict[str, Any]) -> None:
        """Publish event to queue."""
        pass

class EventListener(ABC):
    """
    Abstract base class for listening and handling events.
    """
    
    @abstractmethod
    def on_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        """Handle incoming events."""
        pass

# Decorator for emitting events on method execution
def emit_event(event_type: str):
    """
    Decorator that emits an event after method execution.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            result = await func(self, *args, **kwargs)
            if self.event_queue:
                self.event_queue.publish(event_type, {"result": result})
            return result
        return wrapper
    return decorator