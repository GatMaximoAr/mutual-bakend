from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date
from typing import List


class BaseAddress(BaseModel):
    city: str
    province: str
    street: str
    reference: str
    model_config = ConfigDict(extra="forbid", from_attributes=True)


class CreateAddress(BaseAddress):
    member_dni: str


class ReadAddress(BaseAddress):
    id: int
    member_dni: str


class UpdateAddress(BaseAddress):
    id: int | None = None
    member_dni: str


class BaseMember(BaseModel):

    name: str = Field(max_length=30)
    surname: str = Field(max_length=30)
    phone: str = Field(max_length=30, pattern=r"^\+?[0-9 ]+$")
    active: bool = Field(default=True)
    note: str
    model_config = ConfigDict(extra="forbid", from_attributes=True)


class CreateMember(BaseMember):
    dni: str = Field(max_length=9, pattern=r"^\d*$")
    addresses: List[CreateAddress]


class UpdateMember(BaseMember):
    active: bool
    date_of_leaving: date | None = Field(default=None)
    date_of_entry: date
    addresses: List[UpdateAddress]


class ReadMember(BaseMember):
    dni: str = Field(max_length=9, pattern=r"^\d*$")
    active: bool
    date_of_entry: date
    date_of_leaving: date | None = Field(default=None)
    addresses: List[ReadAddress] = []  # type: ignore
