from faker import Faker

from domain.models import OrderEvent, ClickstreamEvent, User
from domain.types import GeneratedRecord, ClickstreamEventType, OrderEventType
from generator.core.fake import make_faker
from config.models import NullRates
from generator.pipeline.base import PipelineStep


class NullifyStep(PipelineStep):

    def __init__(self, null_rates: NullRates, faker: Faker | None = None, *args, **kwargs):
        self.null_rates = null_rates
        self.faker = faker or make_faker()

    def applies_to(self, event: GeneratedRecord) -> bool:
        if isinstance(event, ClickstreamEvent) and event.new:
            return True
        
        if isinstance(event, OrderEvent) and event.event_type == OrderEventType.ORDER_CREATED:
            return True

        if isinstance(event, User):
            return True

        return False

    def _nullify_field(self, event: GeneratedRecord, field: str, value: float) -> None:
        if hasattr(event, field) and ( value < self.faker.pyfloat(min_value=0., max_value=1.) ):
            setattr(event, field, None)

    def process(self, event: GeneratedRecord) -> list[GeneratedRecord]:
        for field, value in self.null_rates.model_dump().items():
            self._nullify_field(event, field, value)
        return [event]
