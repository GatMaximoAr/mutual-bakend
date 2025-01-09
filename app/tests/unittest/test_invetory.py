from fastapi.testclient import TestClient
from app.main import app
from app.mocks import inventory as mock_inventory
from app.data.inventory import ReadInventory
from unittest import TestCase
from app.models.model import Inventory

# from sqlalchemy import select
from sqlalchemy.orm import Session


def test_can_create_by_end_point(client, session: Session):

    response = client.post(url="/inventory/", json=mock_inventory.RICE)

    assert response.status_code == 200

    response_item = ReadInventory(**response.json())

    created_item: Inventory | None = session.get(Inventory, response_item.id)

    if created_item:
        assert created_item.description == response_item.description
    else:
        assert False


def test_can_reject_malformed_data_on_create(client):

    bad_data = {"some": "bad_data"}
    response = client.post(url="/inventory/", json=bad_data)
    assert response.status_code == 422


def test_can_return_valid_data_on_create(client, session: Session):
    response = client.post(url="/inventory/", json=mock_inventory.RICE)

    data = ReadInventory(**response.json())
    TestCase().assertIsInstance(data, ReadInventory)


def test_can_create_by_model(session: Session):
    item: Inventory = Inventory(**mock_inventory.RICE)
    session.add(item)
    session.commit()

    query = session.get(Inventory, item.id)
    # print(query)

    if query:
        assert query.id == item.id
    else:
        assert False
