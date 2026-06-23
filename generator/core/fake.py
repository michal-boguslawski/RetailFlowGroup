from faker import Faker


def make_faker(locale: str = "en_US") -> Faker:
    return Faker(locale)
