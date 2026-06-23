from typing import Callable

from . import CLICKSTREAMS_RENDERERS_REGISTRY, ORDERS_RENDERERS_REGISTRY


def build_renderer(topic: str, store_id: str) -> Callable:
    
    if topic.endswith("clickstreams"):
        return CLICKSTREAMS_RENDERERS_REGISTRY[store_id]
    
    if topic.endswith("orders"):
        return ORDERS_RENDERERS_REGISTRY[store_id]

    raise KeyError(f"Unknown topic: {topic}")
