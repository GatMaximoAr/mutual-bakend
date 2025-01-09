from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    func,
    Boolean,
    ForeignKey,
    Float,
)
import datetime
from typing import List


class Base(DeclarativeBase):
    """SQlAlchemy Base model class."""

    pass


class Inventory(Base):
    """User model class."""

    __tablename__ = "inventory"

    id = Column(
        Integer, primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    code = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)

    def __init__(self, code, description, price, quantity, weight):
        self.code = code
        self.description = description
        self.price = price
        self.quantity = quantity
        self.weight = weight

    def __repr__(self):
        """Str respresentation model."""
        return f"""Inventory(id={self.id}, code={self.code}, description={self.description},
                    price={self.price}, quantity={self.quantity}, weight={self.weight})"""
