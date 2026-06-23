from abc import ABC, abstractmethod
from domain.types import GeneratedRecord


class PipelineStep(ABC):

    @abstractmethod
    def applies_to(self, event: GeneratedRecord) -> bool: ...

    @abstractmethod
    def process(self, event: GeneratedRecord) -> list[GeneratedRecord]: ...


class Pipeline:

    def __init__(
        self,
        steps: list[PipelineStep]
    ):
        self.steps = steps

    def run(
        self,
        record: GeneratedRecord
    ) -> list[GeneratedRecord]:

        events = [record]

        for step in self.steps:

            output: list[GeneratedRecord] = []

            for event in events:

                if step.applies_to(event):
                    output.extend(
                        step.process(event)
                    )
                else:
                    output.append(event)

            events = output

        return events
