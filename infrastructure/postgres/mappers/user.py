from domain.models import User
from domain.enums import LoyaltyTier, AcquisitionChannel
from infrastructure.postgres.models import AlphaUserORM


def orm_to_model(orm: AlphaUserORM) -> User:
    user = User(
        id=orm.user_id,
        email=orm.email,
        phone=orm.phone,
        first_name=orm.first_name,
        date_of_birth=orm.date_of_birth,
        loyalty_tier=LoyaltyTier(orm.loyalty_tier),
        acquisition_channel=AcquisitionChannel(orm.acquisition_channel) if orm.acquisition_channel else None,
        gdpr_consent=orm.gdpr_consent,
        legacy_customer_no=orm.legacy_customer_no,
    )
    return user


def model_to_row(record: User) -> dict:
    return {
        "user_id": record.id,
        "email": record.email,
        "phone": record.phone,
        "first_name": record.first_name,
        "date_of_birth": record.date_of_birth,
        "loyalty_tier": record.loyalty_tier.value,
        "acquisition_channel": 
            record.acquisition_channel.value
            if record.acquisition_channel
            else None,
        "gdpr_consent": record.gdpr_consent,
        "legacy_customer_no": record.legacy_customer_no,
    }
