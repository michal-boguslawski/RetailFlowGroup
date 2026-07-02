from faker import Faker

from domain.models import AlphaUser, BetaUser
from domain.types import GeneratedRecord
from generator.core.fake import make_faker
from generator.pipeline.base import PipelineStep


class AlphaUserLegacyStep(PipelineStep):

    def __init__(self, legacy_rate: float = 0., faker: Faker | None = None, *args, **kwargs):
        self.legacy_rate = legacy_rate
        self.faker = faker or make_faker()

    def applies_to(self, event: GeneratedRecord) -> bool:
        if isinstance(event, AlphaUser):
            return True

        return False

    def _process_legacy(self, user: GeneratedRecord) -> GeneratedRecord:
        assert isinstance(user, AlphaUser)
        if self.faker.pyfloat(min_value=0., max_value=1.) < self.legacy_rate:
            user.id = str(self.faker.random_int(min=10_000, max=999_999_999))
            user.acquisition_channel = None
        else:
            user.legacy_customer_no = None
            
        return user

    def process(self, event: GeneratedRecord) -> list[GeneratedRecord]:
        return [self._process_legacy(event)]


class BetaUserLegacyStep(PipelineStep):

    def __init__(self, legacy_rate: float = 0., faker: Faker | None = None, *args, **kwargs):
        self.legacy_rate = legacy_rate
        self.faker = faker or make_faker()

    def applies_to(self, event: GeneratedRecord) -> bool:
        if isinstance(event, BetaUser):
            return True

        return False

    def _process_legacy(self, user: GeneratedRecord) -> GeneratedRecord:
        assert isinstance(user, BetaUser)
        if self.faker.pyfloat(min_value=0., max_value=1.) < self.legacy_rate:
            user.loyalty_points = None
            user.gdpr_consent = False
            user.created_at = user.created_at[:10]
        return user

    def process(self, event: GeneratedRecord) -> list[GeneratedRecord]:
        return [self._process_legacy(event)]
