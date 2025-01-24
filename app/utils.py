from typing import Type
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase


def model_to_dto(load: DeclarativeBase, dto: type[BaseModel]) -> BaseModel:
    """
    Converts an SQLAlchemy object (load) to a DTO object.

    :param load: Instance of the SQLAlchemy model.

    :return: DTO instance with data mapped from 'load'.
    """
    # print(load)

    dto_fields = dto.model_fields

    dto_data = {field: getattr(load, field, None) for field in dto_fields}

    return dto(**dto_data)  # type: ignore
