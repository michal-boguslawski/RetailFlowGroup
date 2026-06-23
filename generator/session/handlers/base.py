from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from domain.models import ClickstreamEvent, OrderEvent
from domain.types import EventType, ClickstreamEventType, OrderEventType
from generator.core.id_generator import IdGenerator
from generator.session.state import Session


EventT = TypeVar('EventT', bound=EventType)
ClickstreamT = TypeVar('ClickstreamT', bound=ClickstreamEventType)
OrderT = TypeVar("OrderT", bound=OrderEventType)


class TransitionHandler(ABC, Generic[EventT]):
    def __init__(
        self,
        expected_event_type: EventT,
        *args,
        **kwargs
    ):
        self.expected_event_type = expected_event_type

    @abstractmethod
    def handle(self, session: Session, *args, **kwargs) -> ClickstreamEvent | OrderEvent:
        pass


class ClickstreamTransitionHandler(TransitionHandler[ClickstreamT], Generic[ClickstreamT]):
    def __init__(
        self,
        expected_event_type: ClickstreamT,
        id_generator: IdGenerator,
        *args,
        **kwargs
    ):
        self.expected_event_type = expected_event_type
        self.id_generator = id_generator

    def handle(self, session: Session, *args, **kwargs) -> ClickstreamEvent:
        if session.clickstream_event is None:
            raise ValueError("Session must have a clickstream event")

        session.current_state = self.expected_event_type
        session.clickstream_event.event_id = self.id_generator.make_id("clickstream_event_id")
        session.clickstream_event.event_type = self.expected_event_type
        session.clickstream_event.new = False
        return self._post_handle(session, *args, **kwargs)

    @abstractmethod
    def _post_handle(self, session: Session, *args, **kwargs) -> ClickstreamEvent:
        pass


class OrderTransitionHandler(TransitionHandler[OrderT], Generic[OrderT]):
    def __init__(
        self,
        expected_event_type: OrderT,
        id_generator: IdGenerator,
        *args,
        **kwargs
    ):
        self.expected_event_type = expected_event_type
        self.id_generator = id_generator

    def handle(self, session: Session, *args, **kwargs) -> OrderEvent:
        if session.order_event is None:
            raise ValueError("Session must have a clickstream event")

        session.current_state = self.expected_event_type
        session.order_event.event_id = self.id_generator.make_id("order_event_id")
        session.order_event.event_type = self.expected_event_type
        return self._post_handle(session, *args, **kwargs)

    @abstractmethod
    def _post_handle(self, session: Session, *args, **kwargs) -> OrderEvent:
        pass
