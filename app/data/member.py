from pydantic import BaseModel, Field
from datetime import datetime, date


class BaseMember(BaseModel):

    dni: str = Field(max_length=9, pattern=r"^\d*$")
    name: str = Field(max_length=30)
    surname: str = Field(max_length=30)
    phone: str = Field(max_length=30, pattern=r"^\+?[0-9 ]+$")
    active: bool = Field(default=True)
    address: int
    note: str


class CreateMember(BaseMember):
    pass


class UpdateMember(BaseMember):
    active: bool
    date_of_leaving: datetime | None = Field(default=None)


class ReadMember(BaseMember):
    active: bool
    date_of_entry: date
    date_of_leaving: date | None = Field(default=None)
