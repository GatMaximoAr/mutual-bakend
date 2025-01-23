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
    addresses: Mapped[List["Address"]] = relationship(
        "Address", cascade="all, delete", back_populates="member"
    )
    note = Column(String(150))
    date_of_entry = Column(Date, nullable=False)
    date_of_leaving = Column(Date, nullable=True)

    def __init__(
        self,
        dni,
        name,
        surname,
        phone,
        note=None,
        active=True,
        date_of_leaving=None,
        date_of_entry=None,
    ):
        self.dni = dni
        self.name = name
        self.surname = surname
        self.phone = phone
        self.note = note
        self.active = active
        self.date_of_entry = date.today()
        self.date_of_leaving = date_of_leaving

    def __repr__(self):
        return (
            f"Member(dni={self.dni}, name={self.name}, surname={self.surname}, "
            f"active={self.active}, addresses={self.addresses}, "
            f"date_of_entry={self.date_of_entry}, date_of_leaving={self.date_of_leaving})"
        )


class Address(Base):

    __tablename__ = "address"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    member_dni = Column(String(9), ForeignKey("member.dni"), nullable=False)
    city = Column(String(50))
    province = Column(String(50))
    street = Column(String(50))
    reference = Column(String(150))
    member: Mapped["Member"] = relationship("Member", back_populates="addresses")

    def __init__(self, member_dni, city, province, street, reference):

        self.member_dni = member_dni
        self.city = city
        self.province = province
        self.street = street
        self.reference = reference

    def __repr__(self):

        return (
            f"Address(id={self.id}, member_dni={self.member_dni}, city={self.city}, province={self.province}, "
            f"street={self.street}, reference={self.reference})"
        )
