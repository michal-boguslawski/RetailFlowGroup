from faker import Faker

from domain.models import OrderEvent, ClickstreamEvent, User
from domain.types import GeneratedRecord, ClickstreamEventType, OrderEventType
from generator.core.fake import make_faker
from config.models import FieldCorruptRates
from generator.pipeline.base import PipelineStep


class FieldCorruptionStep(PipelineStep):

    def __init__(self, field_corrupt_rates: FieldCorruptRates, faker: Faker | None = None, *args, **kwargs):
        self.field_corrupt_rates = field_corrupt_rates
        self.faker = faker or make_faker()

    def applies_to(self, event: GeneratedRecord) -> bool:
        return True

    def _corrupt_field(self, event: GeneratedRecord, field: str, value: float) -> None:
        if hasattr(event, field) and ( self.faker.pyfloat(min_value=0., max_value=1.) < value ):
            field_value = getattr(event, field)
            setattr(event, field, field_value.capitalize())
            

    def process(self, event: GeneratedRecord) -> list[GeneratedRecord]:
        for field, value in self.field_corrupt_rates.model_dump().items():
            self._corrupt_field(event, field, value)
        return [event]
