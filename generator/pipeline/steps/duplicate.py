from faker import Faker

from domain.models import ClickstreamEvent
from domain.types import GeneratedRecord
from generator.core.fake import make_faker
from generator.pipeline.base import PipelineStep


class DuplicateStep(PipelineStep):

    def __init__(self, duplication_rate: float = 0., faker: Faker | None = None, *args, **kwargs):
        self.duplication_rate = duplication_rate
        self.faker = faker or make_faker()

    def applies_to(self, event: GeneratedRecord) -> bool:
        if isinstance(event, ClickstreamEvent):
            return True

        return False

    def process(self, event: GeneratedRecord) -> list[GeneratedRecord]:
        if self.faker.pyfloat(min_value=0., max_value=1.) < self.duplication_rate:
            return [event, event]
        return [event]
