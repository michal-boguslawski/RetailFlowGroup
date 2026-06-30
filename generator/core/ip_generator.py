import random
import ipaddress
import pandas as pd
import geoip2.database


class GeoIPGenerator:
    def __init__(self):
        self.reader = geoip2.database.Reader(
            "data/static/GeoLite2-Country.mmdb"
        )

        self.ipv4 = pd.read_csv(
            "data/static/GeoLite2-Country-Blocks-IPv4.csv"
        )

        self.ipv6 = pd.read_csv(
            "data/static/GeoLite2-Country-Blocks-IPv6.csv"
        )

        self.locations = pd.read_csv(
            "data/static/GeoLite2-Country-Locations-en.csv"
        )

        self.country_geonames = self._build_country_map()


    def _build_country_map(self):
        """
        {
            "PL": [798544],
            "DE": [2921044],
            "GB": [2635167]
        }
        """

        result = {}

        for _, row in self.locations.iterrows():
            iso = row.get("country_iso_code")

            if pd.notna(iso):
                result.setdefault(iso, []).append(
                    row["geoname_id"]
                )

        return result


    def _get_country_networks(self, country_code, version):

        df = self.ipv4 if version == 4 else self.ipv6

        geonames = self.country_geonames.get(
            country_code,
            []
        )

        return df[
            df["geoname_id"].isin(geonames)
        ]["network"].tolist()


    def _random_ip_from_network(self, network):

        net = ipaddress.ip_network(network)

        if net.num_addresses <= 2:
            return None

        return str(
            net.network_address
            + random.randint(
                1,
                net.num_addresses - 2
            )
        )


    def random_ip(self, country_code, version):

        networks = self._get_country_networks(
            country_code,
            version
        )

        if not networks:
            return None

        while True:

            network = random.choice(networks)

            ip = self._random_ip_from_network(
                network
            )

            if not ip:
                continue

            try:
                result = self.reader.country(ip)

                if result.country.iso_code == country_code:
                    return ip

            except Exception:
                continue


if __name__ == "__main__":
    ip_generator = GeoIPGenerator()
    print(ip_generator.random_ip("PL", 4))
    print(ip_generator.random_ip("GB", 6))
    print(ip_generator.random_ip("DE", 6))
