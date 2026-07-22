from pathlib import Path
import yaml

from ingestion.contracts.ingestion import IngestionContract


def load_contract(contract_name: str) -> IngestionContract:
    path = Path("config/ingestion") / f"{contract_name}.yaml"

    with path.open() as f:
        data = yaml.safe_load(f)

    return IngestionContract(**data)


if __name__ == "__main__":
    contract = load_contract("alpha_orders")
    print(contract)
