class LegacyShapeStep(PipelineStep[dict]):
    """Collapses ~8% of beta product documents into the legacy flat shape."""

    def __init__(self, legacy_rate: float = 0.08):
        self.legacy_rate = legacy_rate

    def run(self, document: dict) -> dict:
        if random.random() >= self.legacy_rate:
            return document

        legacy = dict(document)

        # legacy integer string _id
        if random.random() < 0.5:
            legacy["_id"] = str(random.randint(10000, 99999))

        # flat category instead of categoryPath
        category_path = legacy.pop("categoryPath", [])
        legacy["category"] = category_path[-1] if category_path else None

        # flat price/currency instead of prices[]
        prices = legacy.pop("prices", [])
        if prices:
            primary = prices[0]
            legacy["price"] = primary["amount"]
            legacy["currency"] = primary["currency"]

        # flat integer stock instead of nested object
        stock = legacy.pop("stock", {})
        legacy["stock"] = stock.get("total", 0)

        # active: 0/1 instead of status string
        status = legacy.pop("status", "active")
        legacy["active"] = 1 if status == "active" else 0

        # variants absent entirely on legacy docs
        legacy.pop("variants", None)

        return legacy
