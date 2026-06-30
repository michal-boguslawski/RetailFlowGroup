from datetime import datetime
from faker import Faker
from typing import Optional, cast

from domain.models import ClickstreamEvent, AlphaUser
from domain.enums import ClickstreamEventType, StoreId, DeviceType
from generator.core.fake import make_faker
from generator.core.id_generator import IdGenerator
from generator.stores.base import BaseFactory
from infrastructure.core.db_service import DBService
from generator.core.ip_generator import GeoIPGenerator


class AlphaClickstreamFactory(BaseFactory[ClickstreamEvent]):
    def __init__(
        self,
        id_generator: IdGenerator,
        db_service: DBService,
        fake: Optional[Faker] = None,
        clock_drift_seconds: int = 0,
        date_start: Optional[datetime] = None,
    ):
        self.fake = fake or make_faker()
        self.id_generator = id_generator
        self.db_service = db_service
        self.clock_drift_seconds = clock_drift_seconds
        self.date_start = date_start or datetime(2023, 1, 1)
        self.ip_generator = GeoIPGenerator()
        

    def make_one(self) -> ClickstreamEvent:
        server_ts = int(self.fake.past_datetime(self.date_start).timestamp())
        client_ts = server_ts + self.fake.random_int(-self.clock_drift_seconds, self.clock_drift_seconds)
        country_code = self.fake.random_element(["DE", "GB", "PL"])
        ip_address = self.ip_generator.random_ip(country_code, self.fake.random_element([4, 6]))

        user = cast(AlphaUser, self.db_service.get_random("users"))

        return ClickstreamEvent(
            event_id=self.id_generator.make_id("clickstream_event_id"),
            event_type=ClickstreamEventType.PAGE_VIEW,
            event_ts=client_ts,
            received_ts=server_ts,
            store_id=StoreId.ALPHA,
            session_id=self.id_generator.make_id("session_id"),
            user=user,
            anonymous_id=self.id_generator.make_id("anonymous_id"),
            product=None,
            device_type=self.fake.random_element(list(DeviceType)),
            ip_address=ip_address,
            country_code=country_code,
            ab_variant=self.fake.random_element(["A", "B", None]),
            scroll_depth_pct=self.fake.pyfloat(min_value=0, max_value=30),
            schema_version="2.1.0",
        )
