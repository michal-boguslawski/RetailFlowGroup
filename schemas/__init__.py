from dataclasses_avroschema import AvroModel
from . import clickstreams, orders

CLICKSTREAM_EVENTS_REGISTRY: dict[str, type[AvroModel]] = {
    "alpha": clickstreams.alpha.ClickstreamEvent,
    "beta": clickstreams.beta.ClickstreamEvent,
}

ORDER_EVENTS_REGISTRY: dict[str, type[AvroModel]] = {
    "alpha": orders.alpha.OrderEvent,
    "beta": orders.beta.OrderEvent,
}
