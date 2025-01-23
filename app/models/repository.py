from abc import ABC, abstractmethod
from sqlalchemy import delete
from sqlalchemy.orm import Session, DeclarativeBase, SessionTransaction
from sqlalchemy.inspection import inspect
from typing import Type, Optional, List
from pydantic import BaseModel
from app.models.model import Member, Address
from app.data import member as dto_member


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

    def _mapped_object_value(self, model, db_query, update_data: Type[BaseModel]):
        """
        Update SQLAlchemy model mapping values using DTO objects.

        Arguments:
            model (DeclarativeBase): The SQLAlchemy model.
            db_query (DeclarativeBase): Database instance object
            update_data (type BaseModel): Pydantyc data transfer object.
        """
        data_keys = set(update_data.model_fields.keys())
        model_keys = set(column.name for column in inspect(model).columns)
        shared_keys = data_keys & model_keys

        update_dict = update_data.model_dump()  # type: ignore
        for key in shared_keys:
            setattr(db_query, key, update_dict[key])

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
            self.session.flush()

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

        self._mapped_object_value(
            model=model, db_query=db_query, update_data=update_data
        )

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


class MemberRepository(Repository):

    def update(self, model, update_data: Type[BaseModel], id: int):
        pass

    def get_member_by_dni(self, model: Type[Member], dni: str):

        return self.session.query(model).filter_by(dni=dni).first()  # type: ignore

    def update_by_dni(
        self,
        model,
        update_data: Type[BaseModel],
        dni: str,
    ) -> Optional[DeclarativeBase]:
        """
        Update a specific model by given id and return its updated data.

        Arguments:
            model (SQLAlchemy model): Model to update.
            update_data (Pydantic model): Data for the update.
            dni (str): ID of the record to update.

        Returns:
            Updated model instance or None if not found.
        """

        member_query = self.get_member_by_dni(model=model, dni=dni)
        if not member_query:
            return None
        # update data on simple fields
        member_query.name = update_data.name  # type: ignore
        member_query.surname = update_data.surname  # type: ignore
        member_query.phone = update_data.phone  # type: ignore
        member_query.active = update_data.active  # type: ignore
        member_query.note = update_data.note  # type: ignore
        member_query.date_of_entry = update_data.date_of_entry  # type: ignore
        member_query.date_of_leaving = update_data.date_of_leaving  # type: ignore
        self.session.commit()

        if member_query.addresses:
            existing_addresses = [addr.id for addr in member_query.addresses]
        else:
            existing_addresses = []

        if len(update_data.addresses) == 0:  # type: ignore

            delete_stmt = delete(Address).where(Address.member_dni == member_query.dni)
            self.session.execute(delete_stmt)
            self.session.refresh(member_query)
        else:
            update_address_ids = [addr.id for addr in update_data.addresses if addr.id != None]  # type: ignore
            if existing_addresses:
                for iden in existing_addresses:
                    if iden not in update_address_ids:
                        delete_stmt = delete(Address).where(Address.id == iden)
                        self.session.execute(delete_stmt)
                        self.session.refresh(member_query)

            for address in update_data.addresses:  # type: ignore
                if address.id != None:
                    db_address = self.get_one(model=Address, id=address.id)
                    self._mapped_object_value(
                        model=Address, db_query=db_address, update_data=address
                    )
                else:
                    new_address = Address(
                        member_dni=address.member_dni,
                        city=address.city,
                        province=address.province,
                        street=address.street,
                        reference=address.reference,
                    )
                    member_query.addresses.append(new_address)

        try:
            self.session.add(member_query)
            self.session.commit()
            self.session.flush()
        except Exception as e:
            self.session.rollback()
            raise e

        return member_query

    def delete(self, model, dni) -> bool:
        """
        Delete record to specific model by given id.

        Argument:
            model (SQLAlchemy model): Given model.
            dni (str): Data unique id.

        Return: True for success operation else False.
        """
        db_query = self.get_member_by_dni(model=model, dni=dni)

        if db_query:
            self.session.delete(db_query)
            self.session.commit()

            return True
        else:
            return False
