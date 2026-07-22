from pathlib import Path
import yaml

from ingestion.contracts.ingestion import IngestionContract


def load_contract(contract_name: str) -> IngestionContract:
    path = Path("config/contracts") / f"{contract_name}.yaml"

    with path.open() as f:
        data = yaml.safe_load(f)

    return IngestionContract(**data)
