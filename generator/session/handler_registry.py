from domain.types import EventType
from generator.session.handlers.base import TransitionHandler


class HandlerRegistry:
    def __init__(self):
        self._handler_classes: dict[
            EventType,
            type[TransitionHandler]
        ] = {}

        self._handlers: dict[
            EventType,
            TransitionHandler
        ] = {}

    def register(
        self,
        event_type: EventType,
        handler_cls: type[TransitionHandler],
    ):
        self._handler_classes[event_type] = handler_cls

    def create(self, **deps):
        print(f"Creating handlers with deps: {deps} and {self._handler_classes}")
        self._handlers = {
            event_type: cls(
                expected_event_type=event_type,
                **deps
            )
            for event_type, cls
            in self._handler_classes.items()
        }

    def get(self, event_type: EventType) -> TransitionHandler:
        try:
            return self._handlers[event_type]
        except KeyError:
            raise ValueError(f"No handler registered for {event_type}")


registry = HandlerRegistry()


def handler(event_type: EventType):
    """
    Decorator for registering handlers
    """
    def decorator(handler_cls: type[TransitionHandler]):
        print("REGISTERING", event_type, handler_cls)

        registry.register(
            event_type,
            handler_cls
        )

        return handler_cls

    return decorator
