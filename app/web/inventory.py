from fastapi import APIRouter
from fastapi import Depends
from app.models.database import get_db
from app.mocks import inventory as mock_inventory
from app.data import inventory as dto_inventory
from sqlalchemy.orm import Session
from app.services import inventory as service
from app.models.model import Inventory

router = APIRouter(prefix="/inventory", tags=["invetory"])


@router.post("/", response_model=dto_inventory.ReadInventory)
async def create_invnetory(
    item: dto_inventory.CreateInventory, session: Session = Depends(get_db)
):

    new_item = service.create_invnetory(item, session)

    return new_item
