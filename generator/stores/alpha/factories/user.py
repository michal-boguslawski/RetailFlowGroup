from datetime import date
from faker import Faker
from typing import Optional

from domain.models import AlphaUser
from domain.enums import LoyaltyTier, AcquisitionChannel
from generator.core.fake import make_faker
from generator.core.id_generator import IdGenerator
from generator.stores.base import BaseFactory


class AlphaUserFactory(BaseFactory[AlphaUser]):
    def __init__(
        self,
        id_generator: IdGenerator,
        fake: Optional[Faker] = None,
        birth_start: date = date(1950, 1, 1),
        birth_end: date = date(2010, 12, 31),
    ):
        self.fake = fake or make_faker()
        self.id_generator = id_generator
        self.birth_start = birth_start
        self.birth_end = birth_end

    def make_one(self) -> AlphaUser:
        return AlphaUser(
            id = self.id_generator.make_id("user_id"),
            email = self.fake.email(),
            phone = self.fake.phone_number(),
            first_name = self.fake.first_name(),
            date_of_birth = self.fake.date_between(
                self.birth_start,
                self.birth_end
            ),
            loyalty_tier = self.fake.random_element(list(LoyaltyTier)),
            acquisition_channel = self.fake.random_element(
                list(AcquisitionChannel) + [None]
            ),
            gdpr_consent = self.fake.boolean(),
            legacy_customer_no = self.fake.unique.random_int(
                min=100_000,
                max=999_999_999
            ),
        )
    