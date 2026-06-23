from generator.session.state import Session


def not_empty_cart(session: Session) -> bool:
        return len(session.cart) > 0
