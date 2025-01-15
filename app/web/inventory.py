from fastapi import APIRouter, Depends
from app.models.database import get_db
from app.mocks import inventory as mock_inventory
from app.data import inventory as dto_inventory
from sqlalchemy.orm import Session
from typing import List
from app.services import inventory as service
from app.models.model import Inventory

router = APIRouter(prefix="/inventory", tags=["invetory"])


@router.post("/", response_model=dto_inventory.ReadInventory)
async def create_invnetory(
    item: dto_inventory.CreateInventory, session: Session = Depends(get_db)
):

    new_item = await service.create_inventory(item, session)

    return new_item


@router.get("/", response_model=List[dto_inventory.ReadInventory])
async def get_all(session: Session = Depends(get_db)):

    item_list = await service.get_all(session=session)

    return item_list


@router.get("/{item_id}", response_model=dto_inventory.ReadInventory)
async def get_one(item_id: int, session: Session = Depends(get_db)):
    item = await service.get_one(item_id=item_id, session=session)

    return item
