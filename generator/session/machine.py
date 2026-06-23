from typing import cast

from domain.enums import ClickstreamEventType, ExitEventType
from domain.models import ClickstreamEvent, OrderEvent
from generator.core.id_generator import IdGenerator
from generator.session.handler_registry import HandlerRegistry
from generator.session.handler_registry import registry as initiated_registry
from generator.session.state import Session
from generator.session.transitions import TransitionMap
from generator.stores.factory import StoreFactory
from infrastructure.core.db_service import DBService


class StateMachine:
    def __init__(
        self,
        store_factory: StoreFactory,
        db_service: DBService,
        transition_map: TransitionMap,
        id_generator: IdGenerator,
        session: Session | None = None,
        handler_registry: HandlerRegistry | None = None,
    ):
        self.store_factory = store_factory
        self.db_service = db_service
        self.transition_map = transition_map
        self.id_generator = id_generator
        self.session = session or Session()
        self.handler_registry = handler_registry or initiated_registry
        self._initiated = False

    def _reset_event(self) -> ClickstreamEvent:
        next_state = ClickstreamEventType.PAGE_VIEW

        clickstream_event = self.store_factory.make_one("clickstreams")
        assert type(clickstream_event) is ClickstreamEvent, "Generated clickstream event must be of type ClickstreamEvent"

        self.session.cart = []
        self.session.order_event = None
        self.session.clickstream_event = clickstream_event
        self.session.current_state = next_state
        return clickstream_event

    def _initiate(self):
        self.handler_registry.create(
            db_service=self.db_service,
            store_factory=self.store_factory,
            id_generator=self.id_generator,
        )
        self._initiated = True

    def step(self) -> ClickstreamEvent | OrderEvent:
        if not self._initiated:
            self._initiate()

        if self.session.current_state is None:
            return self._reset_event()

        next_state = self.transition_map.next_state(
            self.session.current_state,
            context=self.session
        )

        if next_state == ExitEventType.EXIT:
            return self._reset_event()

        next_state_handler = self.handler_registry.get(next_state)

        return next_state_handler.handle(
            self.session
        )
