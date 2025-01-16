from abc import ABC, abstractmethod
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy.inspection import inspect
from typing import Type, Optional, List
from pydantic import BaseModel
import copy


class AbstracRepository(ABC):

    @abstractmethod
    def create(self, new_model: DeclarativeBase) -> DeclarativeBase:
        pass

    @abstractmethod
    def get_one(self, model: DeclarativeBase, id: int) -> DeclarativeBase | None:
        pass

    @abstractmethod
    def get_all(self, model):
        pass

    @abstractmethod
    def update(
        self, update_model: DeclarativeBase, update_data: Type[BaseModel], id: int
    ):
        pass

    @abstractmethod
    def delete(self, model: DeclarativeBase, id: int) -> bool:
        pass


class Repository(AbstracRepository):
    """Class to manage basic CRUD database transactions."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, new_data: DeclarativeBase) -> DeclarativeBase:
        """
        Create a record of the given model.

        Arguments:
            new_data (SQLAlchemy model): Data to storage.

        Raises: SQLAlchemy exception
        """
        try:

            self.session.add(new_data)
            self.session.commit()

            return new_data

        except Exception as e:
            self.session.rollback()
            raise e

    def get_one(self, model, id: int) -> DeclarativeBase | None:
        """
        Return specific given model by given id.

        Arguments:
            model (SQLAlchemy model): Given model.
            id (int): data unique id
        """
        return self.session.get(entity=model, ident=id)

    def get_all(self, model) -> List[DeclarativeBase]:
        """
        Retrieve all records of the specified model.

        Arguments:
            model (SQLAlchemy model): Model to query.

        Returns:
            List of model instances.
        """
        try:
            return self.session.query(model).all()
        except Exception as e:
            self.session.rollback()
            raise e

    def update(
        self, model, update_data: Type[BaseModel], id: int
    ) -> Optional[DeclarativeBase]:
        """
        Update a specific model by given id and return its updated data.

        Arguments:
            model (SQLAlchemy model): Model to update.
            update_data (Pydantic model): Data for the update.
            id (int): ID of the record to update.

        Returns:
            Updated model instance or None if not found.
        """

        db_query = self.get_one(model=model, id=id)
        if not db_query:
            return None

        data_keys = set(update_data.model_fields.keys())
        model_keys = set(column.name for column in inspect(model).columns)
        shared_keys = data_keys & model_keys

        update_dict = update_data.model_dump()  # type: ignore
        for key in shared_keys:
            setattr(db_query, key, update_dict[key])

        try:
            self.session.add(db_query)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

        return db_query

    def delete(self, model, id: int) -> bool:
        """
        Delete record to specific model by given id.

        Argument:
            model (SQLAlchemy model): Given model.
            id (int): Data unique id.

        Return: True for success operation else False.
        """
        db_query = self.get_one(model=model, id=id)

        if db_query:
            self.session.delete(db_query)
            self.session.commit()

            return True
        else:
            return False
