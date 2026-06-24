from faker import Faker

from domain.models import User
from domain.types import GeneratedRecord
from generator.core.fake import make_faker
from generator.pipeline.base import PipelineStep


class UserLegacyStep(PipelineStep):

    def __init__(self, legacy_rate: float = 0., faker: Faker | None = None, *args, **kwargs):
        self.legacy_rate = legacy_rate
        self.faker = faker or make_faker()

    def applies_to(self, event: GeneratedRecord) -> bool:
        if isinstance(event, User):
            return True

        return False

    def _process_legacy(self, user: GeneratedRecord) -> GeneratedRecord:
        assert isinstance(user, User)
        if self.faker.pyfloat(min_value=0., max_value=1.) < self.legacy_rate:
            user.id = str(self.faker.random_int(min=10_000, max=999_999_999))
            user.acquisition_channel = None
        else:
            user.legacy_customer_no = None
            
        return user

    def process(self, event: GeneratedRecord) -> list[GeneratedRecord]:
        return [self._process_legacy(event)]
