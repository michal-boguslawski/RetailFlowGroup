from . import CLICKSTREAM_EVENTS_REGISTRY, ORDER_EVENTS_REGISTRY


def build_avro_schema(topic: str, store_id: str) -> str:
    
    if topic.endswith("clickstreams"):
        return CLICKSTREAM_EVENTS_REGISTRY[store_id].avro_schema()
    
    if topic.endswith("orders"):
        return ORDER_EVENTS_REGISTRY[store_id].avro_schema()

    raise KeyError(f"Unknown topic: {topic}")
