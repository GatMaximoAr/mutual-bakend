from sqlalchemy.orm import Session
from app.data import inventory as dto_inventory
from app.models.model import Inventory


def create_invnetory(
    item: dto_inventory.CreateInventory, session: Session
) -> dto_inventory.ReadInventory:

    new_item = Inventory(**item.model_dump())
    session.add(new_item)
    session.commit()

    dto = dto_inventory.ReadInventory(
        id=int(new_item.id),
        code=str(new_item.code),
        description=str(new_item.description),
        price=float(new_item.price),
        quantity=int(new_item.quantity),
        weight=int(new_item.weight),
    )

    return dto
