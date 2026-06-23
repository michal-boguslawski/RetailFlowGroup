from dataclasses import dataclass
from collections import defaultdict, OrderedDict
from faker import Faker
from typing import Callable

from domain.enums import ExitEventType
from domain.types import EventType
from generator.core.fake import make_faker
from generator.session.state import Session


@dataclass(frozen=True)
class Transition:
    from_state: EventType
    to_state: EventType
    probability: float = 1.0
    guard: Callable | None = None


class TransitionMap:

    def __init__(
        self,
        transitions: list[Transition],
        fake: Faker | None = None
    ):
        self.transitions = defaultdict(list)
        self.fake = fake or make_faker()

        for transition in transitions:
            self.transitions[transition.from_state].append(transition)


    def available(self, state: EventType, context=None) -> list[Transition]:
        transitions = self.transitions.get(state, [])

        return [
            t
            for t in transitions
            if t.guard is None or t.guard(context)
        ]


    def next_state(self, state: EventType, context: Session | None = None) -> EventType:

        transitions = self.available(
            state,
            context
        )

        if not transitions:
            return ExitEventType.EXIT

        if len(transitions) == 1:
            return transitions[0].to_state
        probs = OrderedDict({t.to_state: t.probability for t in transitions})
        return self.fake.random_element(elements=probs)
