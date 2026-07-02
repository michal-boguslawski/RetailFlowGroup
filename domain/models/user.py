from dataclasses import dataclass
from datetime import date, datetime, UTC

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
    preferred_language: PrefferedLanguages | None
    size_preferences: dict[str, str]
    wishlist: list[str]
    loyalty_points: int | None
    gdpr_consent: bool | None
    created_at: str = datetime.now(UTC).isoformat()

    @classmethod
    def from_document(cls, doc: dict) -> "BetaUser":
        preferred_language = doc.get("preferredLanguage")
        return cls(
            id=doc["_id"],
            email_hash=doc.get("emailHash"),
            phone_hash=doc.get("phoneHash"),
            preferred_language=PrefferedLanguages(preferred_language) if preferred_language else None,
            size_preferences=doc.get("sizePreferences", {}),
            wishlist=doc.get("wishlist", []),
            loyalty_points=doc.get("loyaltyPoints"),
            gdpr_consent=doc.get("gdprConsent"),
        )

