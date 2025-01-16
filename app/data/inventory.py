from pydantic import BaseModel, ConfigDict


class BaseInventory(BaseModel):
    code: str
    description: str
    price: float
    quantity: int
    weight: int
    model_config = ConfigDict(extra="forbid", from_attributes=True)


class CreateInventory(BaseInventory):
    pass


class ReadInventory(BaseInventory):
    id: int
