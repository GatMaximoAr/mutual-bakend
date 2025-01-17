from sqlalchemy.orm import DeclarativeBase, relationship
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
from datetime import date
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


class Member(Base):

    __tablename__ = "member"

    dni = Column(String(9), primary_key=True, nullable=False, unique=True)
    name = Column(String(30), nullable=False)
    surname = Column(String(30), nullable=False)
    phone = Column(String(30), nullable=False)
    active = Column(Boolean, nullable=False)
    address = Column(Integer, nullable=False)
    note = Column(String(150))
    date_of_entry = Column(Date, nullable=False)
    date_of_leaving = Column(Date, nullable=True)

    def __init__(
        self,
        dni,
        name,
        surname,
        phone,
        address,
        note=None,
        active=True,
        date_of_leaving=None,
        date_of_entry=None,
    ):
        self.dni = dni
        self.name = name
        self.surname = surname
        self.phone = phone
        self.address = address
        self.note = note
        self.active = active
        self.date_of_entry = date.today()
        self.date_of_leaving = date_of_leaving

    def __str__(self):
        return (
            f"<Member(dni={self.dni}, name={self.name}, surname={self.surname}, "
            f"active={self.active}, address={self.address}, "
            f"date_of_entry={self.date_of_entry}, date_of_leaving={self.date_of_leaving})>"
        )
