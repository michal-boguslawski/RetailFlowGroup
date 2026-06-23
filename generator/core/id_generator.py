# generator/core/id_generator.py
from datetime import datetime
import itertools
from pathlib import Path
import json
import threading
import uuid
from typing import Iterator

from config.models import IdConfig, IdFormat
from domain.enums import StoreId


_DEFAULT_STATE_DIR = Path(".generator_state")


class IdGenerator:
    _instances: dict[str, "IdGenerator"] = {}
    _instances_lock = threading.Lock()

    def __new__(cls, store_id: str, config: IdConfig, state_path: Path | None = None):
        if store_id not in cls._instances:
            with cls._instances_lock:
                if store_id not in cls._instances:
                    instance = super().__new__(cls)
                    instance._initialized = False
                    cls._instances[store_id] = instance
        return cls._instances[store_id]

    def __init__(self, store_id: StoreId, config: IdConfig, state_path: Path | None = None):
        if self._initialized:
            return
        self._initialized = True

        self.store_id = store_id
        self.config = config
        self._state_path = state_path or (_DEFAULT_STATE_DIR / f"{store_id}.json")
        self._lock = threading.Lock()

        self._ensure_state_file()

        self._offsets = self._load_state()
        self._counters: dict[str, Iterator[int]] = {
            id_type: itertools.count(start=value + 1, step=1)
            for id_type, value in self._offsets.items()
        }

    @classmethod
    def for_store(cls, store_id: StoreId, config: IdConfig, state_path: Path | None = None) -> "IdGenerator":
        return cls(store_id, config, state_path)

    @classmethod
    def reset_registry(cls) -> None:
        """Clear cached instances. Intended for test teardown only."""
        with cls._instances_lock:
            cls._instances.clear()

    def _ensure_state_file(self) -> None:
        self._state_path.parent.mkdir(parents=True, exist_ok=True)

        if not self._state_path.exists():
            self._state_path.write_text("{}")

    def _get_counter(self, id_type: str) -> Iterator[int]:
        if id_type not in self._counters:
            self._counters[id_type] = itertools.count(start=1, step=1)
        return self._counters[id_type]

    def make_id(self, id_type: str) -> str:
        fmt: IdFormat = getattr(self.config, id_type) or IdFormat(style="uuid")
        match fmt.style:
            case "uuid":
                return f"{fmt.prefix}{uuid.uuid4()}"
            case "integer":
                with self._lock:
                    value = next(self._get_counter(id_type))
                    self._save_offset(id_type, value)
                return f"{fmt.prefix}{value}"
            case "ret_prefixed":
                with self._lock:
                    value = next(self._get_counter(id_type))
                    self._save_offset(id_type, value)
                date = datetime.now().strftime("%Y%m%d")
                return f"{fmt.prefix}{date}-{value}"

    def _load_state(self) -> dict[str, int]:
        if self._state_path.exists():
            state = self._state_path.read_text()
            print(f"State loaded for '{self.store_id}': {state}")
            return json.loads(state)
        return {}

    def _save_offset(self, id_type: str, value: int) -> None:
        self._offsets[id_type] = value
        self._state_path.write_text(json.dumps(self._offsets))
