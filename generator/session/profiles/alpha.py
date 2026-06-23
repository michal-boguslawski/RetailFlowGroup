from generator.session.transitions import Transition
from generator.session.guards.not_empty_cart import not_empty_cart

from domain.enums import (
    OrderEventType,
    ClickstreamEventType,
    ExitEventType,
)


TRANSITIONS = [

    # Clickstream

    Transition(
        ClickstreamEventType.PAGE_VIEW,
        ClickstreamEventType.PRODUCT_VIEW,
        0.60,
    ),

    Transition(
        ClickstreamEventType.PAGE_VIEW,
        ClickstreamEventType.PAGE_VIEW,
        0.25,
    ),

    Transition(
        ClickstreamEventType.PAGE_VIEW,
        ExitEventType.EXIT,
        0.15,
    ),

    Transition(
        ClickstreamEventType.PRODUCT_VIEW,
        ClickstreamEventType.ADD_TO_CART,
        0.35,
    ),

    Transition(
        ClickstreamEventType.PRODUCT_VIEW,
        ClickstreamEventType.PRODUCT_VIEW,
        0.45,
    ),

    Transition(
        ClickstreamEventType.PRODUCT_VIEW,
        ClickstreamEventType.PAGE_VIEW,
        0.10,
    ),

    Transition(
        ClickstreamEventType.PRODUCT_VIEW,
        ExitEventType.EXIT,
        0.10,
    ),

    Transition(
        ClickstreamEventType.ADD_TO_CART,
        ClickstreamEventType.CHECKOUT_START,
        0.55,
    ),

    Transition(
        ClickstreamEventType.ADD_TO_CART,
        ClickstreamEventType.REMOVE_FROM_CART,
        0.20,
    ),

    Transition(
        ClickstreamEventType.ADD_TO_CART,
        ClickstreamEventType.PRODUCT_VIEW,
        0.15,
    ),

    Transition(
        ClickstreamEventType.ADD_TO_CART,
        ExitEventType.EXIT,
        0.10,
    ),

    Transition(
        ClickstreamEventType.REMOVE_FROM_CART,
        ClickstreamEventType.PRODUCT_VIEW,
        0.50,
    ),

    Transition(
        ClickstreamEventType.REMOVE_FROM_CART,
        ExitEventType.EXIT,
        0.50,
    ),

    # Checkout → Order

    Transition(
        ClickstreamEventType.CHECKOUT_START,
        OrderEventType.ORDER_CREATED,
        0.90,
        not_empty_cart
    ),

    Transition(
        ClickstreamEventType.CHECKOUT_START,
        ClickstreamEventType.CHECKOUT_ABANDON,
        0.10,
    ),

    Transition(
        ClickstreamEventType.CHECKOUT_ABANDON,
        ExitEventType.EXIT,
        1.0,
    ),

    # Order lifecycle

    Transition(
        OrderEventType.ORDER_CREATED,
        OrderEventType.PAYMENT_INITIATED,
        0.95,
    ),

    Transition(
        OrderEventType.ORDER_CREATED,
        OrderEventType.CANCELLED,
        0.05,
    ),


    Transition(
        OrderEventType.PAYMENT_INITIATED,
        OrderEventType.PAYMENT_CONFIRMED,
        0.85,
    ),

    Transition(
        OrderEventType.PAYMENT_INITIATED,
        OrderEventType.PAYMENT_FAILED,
        0.15,
    ),

    Transition(
        OrderEventType.PAYMENT_CONFIRMED,
        OrderEventType.SHIPPED,
        0.98,
    ),

    Transition(
        OrderEventType.PAYMENT_CONFIRMED,
        OrderEventType.CANCELLED,
        0.02,
    ),

    Transition(
        OrderEventType.PAYMENT_FAILED,
        OrderEventType.PAYMENT_INITIATED,
        0.60,
    ),

    Transition(
        OrderEventType.PAYMENT_FAILED,
        OrderEventType.CANCELLED,
        0.40,
    ),

    Transition(
        OrderEventType.SHIPPED,
        OrderEventType.DELIVERED,
        0.99,
    ),

    Transition(
        OrderEventType.SHIPPED,
        ExitEventType.EXIT,
        0.01,
    ),

    Transition(
        OrderEventType.DELIVERED,
        ExitEventType.EXIT,
        0.95,
    ),

    Transition(
        OrderEventType.DELIVERED,
        OrderEventType.RETURN_REQUESTED,
        0.05,
    ),

    Transition(
        OrderEventType.RETURN_REQUESTED,
        OrderEventType.REFUNDED,
        0.90,
    ),

    Transition(
        OrderEventType.RETURN_REQUESTED,
        ExitEventType.EXIT,
        0.10,
    ),

    Transition(
        OrderEventType.REFUNDED,
        ExitEventType.EXIT,
        1.0,
    ),

    Transition(
        OrderEventType.CANCELLED,
        ExitEventType.EXIT,
        1.0,
    ),
]