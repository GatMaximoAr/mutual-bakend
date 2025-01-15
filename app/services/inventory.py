from fastapi import HTTPException
from sqlalchemy.orm import Session, DeclarativeBase
from app.data import inventory as dto_inventory
from app.models.model import Inventory
from app.models.repository import Repository
from app.utils import model_to_dto
from pydantic import BaseModel


async def create_inventory(
    item: dto_inventory.CreateInventory, session: Session
) -> BaseModel:

    repo = Repository(session=session)

    new_item = repo.create(Inventory(**item.model_dump()))

    dto = model_to_dto(new_item, dto_inventory.ReadInventory)

    return dto


async def get_one(item_id: int, session: Session) -> BaseModel:

    repo = Repository(session=session)

    item = repo.get_one(model=Inventory, id=item_id)

    if item:

        return model_to_dto(load=item, dto=dto_inventory.ReadInventory)

    raise HTTPException(status_code=404, detail="Item {id} not found")


async def get_all(session: Session):

    repo = Repository(session=session)
    item_list = []

    for item in repo.get_all(Inventory):
        if item:

            item_list.append(model_to_dto(item, dto_inventory.ReadInventory))

    return item_list
