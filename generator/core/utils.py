from pathlib import Path
import geoip2.database


BASE_DIR = Path("data/static")
path = BASE_DIR / "GeoLite2-Country.mmdb"
reader = geoip2.database.Reader(str(path))


def get_country_code_from_ip(ip_address: str):

    try:
        response = reader.country(ip_address)

        return response.country.iso_code

    except Exception:
        return None
