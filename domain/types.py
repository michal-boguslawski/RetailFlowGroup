# generator/core/types.py

from typing import TypeAlias

from domain.enums import OrderEventType, ClickstreamEventType, ExitEventType
from domain.models import User, OrderEvent, Order, Product, ClickstreamEvent, GammaOrder, Promotion, OrderReturn, Formatter


GeneratedRecord: TypeAlias = User | OrderEvent | Order | Product | ClickstreamEvent | GammaOrder | Promotion | OrderReturn | Formatter

EventType = (
    OrderEventType
    | ClickstreamEventType
    | ExitEventType
)
