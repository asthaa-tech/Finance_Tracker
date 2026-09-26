from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(255)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="user"
    )

    budgets: Mapped[list["Budget"]] = relationship(
        back_populates="user"
    )

    memberships: Mapped[list["FamilyMembership"]] = relationship(
        back_populates="user"
    )

    accounts: Mapped[list["FinancialAccount"]] = relationship(
        back_populates="user"
    )


class Family(Base):
    __tablename__ = "families"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(255)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    memberships: Mapped[list["FamilyMembership"]] = relationship(
        back_populates="family",
        cascade="all, delete-orphan",
    )


class FamilyMembership(Base):
    __tablename__ = "family_memberships"

    id: Mapped[int] = mapped_column(primary_key=True)

    family_id: Mapped[int] = mapped_column(
        ForeignKey("families.id"),
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        default="member",
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="active",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    family: Mapped["Family"] = relationship(
        back_populates="memberships"
    )

    user: Mapped["User"] = relationship(
        back_populates="memberships"
    )

    __table_args__ = (
        UniqueConstraint(
            "family_id",
            "user_id",
            name="uq_family_user",
        ),
    )


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="category"
    )

    budgets: Mapped[list["Budget"]] = relationship(
        back_populates="category"
    )


class FinancialAccount(Base):
    __tablename__ = "financial_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
    )

    account_name: Mapped[str] = mapped_column(
        String(255)
    )

    account_type: Mapped[str] = mapped_column(
        String(30)
    )

    provider_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    identifier: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user: Mapped["User"] = relationship(
        back_populates="accounts"
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="account"
    )

    connections: Mapped[list["FinancialConnection"]] = relationship(
        back_populates="account",
        cascade="all, delete-orphan",
    )


class FinancialConnection(Base):
    __tablename__ = "financial_connections"

    id: Mapped[int] = mapped_column(primary_key=True)

    account_id: Mapped[int] = mapped_column(
        ForeignKey("financial_accounts.id"),
        index=True,
    )

    provider_name: Mapped[str] = mapped_column(
        String(100)
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="pending",
    )

    external_account_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    last_synced_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    account: Mapped["FinancialAccount"] = relationship(
        back_populates="connections"
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
    )

    account_id: Mapped[int | None] = mapped_column(
        ForeignKey("financial_accounts.id"),
        nullable=True,
        index=True,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        index=True,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2)
    )

    transaction_type: Mapped[str] = mapped_column(
        String(20)
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    merchant_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    transaction_date: Mapped[date] = mapped_column(
        Date,
        index=True,
    )

    categorization_source: Mapped[str] = mapped_column(
    String(30),
    default="manual",
    server_default="manual",
    )

    categorization_confidence: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 4),
        nullable=True,
    )

    external_transaction_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user: Mapped["User"] = relationship(
        back_populates="transactions"
    )

    account: Mapped["FinancialAccount"] = relationship(
        back_populates="transactions"
    )

    category: Mapped["Category"] = relationship(
        back_populates="transactions"
    )


class Budget(Base):
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        index=True,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2)
    )

    month: Mapped[date] = mapped_column(
        Date,
        index=True,
    )

    user: Mapped["User"] = relationship(
        back_populates="budgets"
    )

    category: Mapped["Category"] = relationship(
        back_populates="budgets"
    )