from faker import Faker
from faker.providers import BaseProvider
import hashlib


class HasherProvider(BaseProvider):
    def hashed(self, value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()



def make_faker(locale: str = "en_US") -> Faker:
    fake = Faker(locale)
    fake.add_provider(HasherProvider)
    return fake


if __name__ == "__main__":
    fake = make_faker()
    print(fake.hashed("test"))
