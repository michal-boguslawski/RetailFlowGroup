from dataclasses import dataclass
from datetime import date
from typing import Optional

from domain.enums import (
    LoyaltyTier, AcquisitionChannel
)


@dataclass
class User:
    id: str
    email: str
    phone: Optional[str]
    first_name: Optional[str]
    date_of_birth: Optional[date]
    loyalty_tier: LoyaltyTier
    acquisition_channel: Optional[AcquisitionChannel]
    gdpr_consent: bool
    legacy_customer_no: Optional[int]
