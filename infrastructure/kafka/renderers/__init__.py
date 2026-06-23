from typing import Callable

from . import clickstreams, orders

CLICKSTREAMS_RENDERERS_REGISTRY: dict[str, Callable] = {
    "alpha": clickstreams.alpha.alpha_clickstream_renderer,
    "beta": clickstreams.beta.beta_clickstream_renderer,
}


ORDERS_RENDERERS_REGISTRY: dict[str, Callable] = {
    "alpha": orders.alpha.alpha_order_renderer,
    "beta": orders.beta.beta_order_renderer,
}

