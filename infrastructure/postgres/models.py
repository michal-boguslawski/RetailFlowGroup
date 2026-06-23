from datetime import date, datetime
from decimal import Decimal
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import (
    String,
    Integer,
    Boolean,
    Date,
    TIMESTAMP,
    CheckConstraint,
    text,
    Text,
    Numeric,
    ForeignKey,
)
from typing import Optional, List


class Base(DeclarativeBase):
    pass


class AlphaProductORM(Base):
    __tablename__ = 'products'

    product_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    category_path: Mapped[str] = mapped_column(String(256), nullable=True)
    name: Mapped[str] = mapped_column(String(256))
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 4))

    order_items: Mapped[List["AlphaOrderItemORM"]] = relationship(
        back_populates="product"
    )

    def __repr__(self):
        return f"Product(id='{self.product_id}', name='{self.name}', price={self.unit_price})"


class AlphaUserORM(Base):
    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint(
            "loyalty_tier IN ('standard', 'silver', 'gold', 'vip')",
            name="chk_loyalty_tier",
        ),
    )

    user_id: Mapped[str] = mapped_column(String(64), primary_key=True)

    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)

    first_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)

    date_of_birth: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )

    loyalty_tier: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    acquisition_channel: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
    )

    gdpr_consent: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    legacy_customer_no: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("NOW()"),
    )

    # Relationship
    orders: Mapped[List["AlphaOrderORM"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )


class AlphaOrderORM(Base):
    __tablename__ = "orders"

    __table_args__ = (
        CheckConstraint(
            "user_id IS NOT NULL OR guest_email IS NOT NULL",
            name="chk_orders_user_or_guest",
        ),
    )

    order_id: Mapped[str] = mapped_column(String(64), primary_key=True)

    user_id: Mapped[Optional[str]] = mapped_column(
        String(64),
        ForeignKey("users.user_id"),
        nullable=True,
    )

    currency: Mapped[Optional[str]] = mapped_column(
        String(4),
        nullable=True,
    )

    guest_email: Mapped[Optional[str]] = mapped_column(
        String(128),
        nullable=True,
    )

    total_price: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )

    tax_price: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )

    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # status: Mapped[str] = mapped_column(
    #     String(32),
    #     nullable=False,
    # )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("NOW()"),
    )

    items: Mapped[List["AlphaOrderItemORM"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan"
    )

    user: Mapped[AlphaUserORM] = relationship(
        back_populates="orders"
    )


class AlphaOrderItemORM(Base):
    __tablename__ = "order_items"

    order_item_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("1"))
    discount_pct: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )

    order_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("orders.order_id"),
        nullable=False,
    )

    product_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("products.product_id"),
        nullable=False,
    )

    # Relationships
    order: Mapped[AlphaOrderORM] = relationship(
        back_populates="items"
    )

    product: Mapped[AlphaProductORM] = relationship(
        back_populates="order_items"
    )
