from pathlib import Path
import geoip2.database
from geoip2.errors import AddressNotFoundError


BASE_DIR = Path("data/static")
path = BASE_DIR / "GeoLite2-Country.mmdb"

reader = geoip2.database.Reader(str(path))


def get_country_code_from_ip(ip_address: str):
    try:
        response = reader.country(ip_address)
        return response.country.iso_code
    except AddressNotFoundError:
        print(f"No country found for IP: {ip_address}")
        return None


if __name__ == "__main__":
    print(get_country_code_from_ip("f218:666c:d47e:8fa3:d47c:2c9e:9f0c:ec99"))
