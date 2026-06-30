from dataclasses import dataclass
from datetime import date

from domain.enums import (
    LoyaltyTier, AcquisitionChannel, PrefferedLanguages
)


@dataclass
class User:
    id: str
    gdpr_consent: bool | None


@dataclass
class AlphaUser(User):
    email: str
    phone: str | None
    first_name: str | None
    date_of_birth: date | None
    loyalty_tier: LoyaltyTier
    acquisition_channel: AcquisitionChannel | None
    legacy_customer_no: int | None


@dataclass
class BetaUser(User):
    email_hash: str | None
    phone_hash: str | None
    preferredLanguage: PrefferedLanguages | None
    size_preferences: dict[str, str]
    wishlist: list[str]
    loyalty_points: int | None
    gdpr_consent: bool | None
