from domain.models import BetaUser


def model_to_document(user: BetaUser):
    return {
        "_id": user.id,
        "emailHash": user.email_hash,
        "phoneHash": user.phone_hash,
        "preferredLanguage": user.preferred_language.value if user.preferred_language else None,
        "sizePreferences": user.size_preferences,
        "wishlist": user.wishlist,
        "loyaltyPoints": user.loyalty_points,
        "gdprConsent": user.gdpr_consent,
        "createdAt": user.created_at
    }
