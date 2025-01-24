from fastapi import HTTPException
from sqlalchemy.orm import Session, DeclarativeBase
from app.data import inventory as dto_inventory
from app.models.model import Inventory
from app.models.repository import Repository
from typing import List


async def create_inventory(
    item: dto_inventory.CreateInventory, session: Session
) -> dto_inventory.ReadInventory:

    repo = Repository(session=session)

    new_item = repo.create(Inventory(**item.model_dump()))

    dto = dto_inventory.ReadInventory.model_validate(new_item)

    return dto


async def get_one(id: int, session: Session) -> dto_inventory.ReadInventory:

    repo = Repository(session=session)

    item = repo.get_one(model=Inventory, id=id)

    if item:

        return dto_inventory.ReadInventory.model_validate(item)

    raise HTTPException(status_code=404, detail=f"Item {id} not found")


async def get_all(session: Session) -> List[dto_inventory.ReadInventory]:

    repo = Repository(session=session)
    item_list = []

    for item in repo.get_all(Inventory):
        if item:

            valid_item = dto_inventory.ReadInventory.model_validate(item)

            item_list.append(valid_item)

    return item_list


async def update(
    id: int, update_data: dto_inventory.CreateInventory, session: Session
) -> dto_inventory.ReadInventory:
    repo = Repository(session=session)

    update_item = repo.update(Inventory, update_data=update_data, id=id)  # type: ignore

    if update_item:
        return dto_inventory.ReadInventory.model_validate(update_item)

    raise HTTPException(status_code=404, detail=f"Item {id} not found")


async def delete(id: int, session: Session):

    repo = Repository(session=session)

    if repo.delete(model=Inventory, id=id) is False:

        raise HTTPException(status_code=404, detail=f"Item {id} not found")
