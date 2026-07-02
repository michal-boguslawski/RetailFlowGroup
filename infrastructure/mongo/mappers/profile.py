from domain.models.user import BetaUser, PrefferedLanguages


def document_to_model(doc: dict) -> BetaUser:
    preferred_language = doc.get("preferredLanguage")
    return BetaUser(
        id=doc["_id"],
        email_hash=doc.get("emailHash"),
        phone_hash=doc.get("phoneHash"),
        preferred_language=PrefferedLanguages(preferred_language) if preferred_language else None,
        size_preferences=doc.get("sizePreferences", {}),
        wishlist=doc.get("wishlist", []),
        loyalty_points=doc.get("loyaltyPoints"),
        gdpr_consent=doc.get("gdprConsent"),
    )
