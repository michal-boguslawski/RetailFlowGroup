import copy
from faker import Faker

from domain.types import GeneratedRecord
from generator.core.fake import make_faker
from config.models import TrailingSpacesCorruptRates
from generator.pipeline.base import PipelineStep


class TrailingSpacesCorruptionStep(PipelineStep):

    def __init__(self, trailing_spaces_corrupt_rates: TrailingSpacesCorruptRates, faker: Faker | None = None, *args, **kwargs):
        self.trailing_spaces_corrupt_rates = trailing_spaces_corrupt_rates
        self.faker = faker or make_faker()

    def applies_to(self, event: GeneratedRecord) -> bool:
        return True

    def _corrupt_field(self, event: GeneratedRecord, field: str, value: float) -> None:
        if hasattr(event, field) and ( self.faker.pyfloat(min_value=0., max_value=1.) < value ):
            field_value = getattr(event, field)
            if not isinstance(field_value, str):
                return

            setattr(event, field, field_value + " " * self.faker.random_int(min=1, max=5))

    def process(self, event: GeneratedRecord) -> list[GeneratedRecord]:
        event = copy.deepcopy(event)

        for field, value in self.trailing_spaces_corrupt_rates.rates.items():
            self._corrupt_field(event, field, value)

        return [event]
