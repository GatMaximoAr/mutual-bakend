from fastapi.testclient import TestClient
from app.main import app
from app.mocks import inventory as mock_inventory
from app.data.inventory import ReadInventory
from unittest import TestCase
from app.models.model import Inventory
from typing import List

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


def test_can_reject_malformed_data_on_create(client: TestClient):

    bad_data = {"some": "bad_data"}
    response = client.post(url="/inventory/", json=bad_data)
    assert response.status_code == 422


def test_can_return_valid_data_on_create(client: TestClient, session: Session):
    response = client.post(url="/inventory/", json=mock_inventory.RICE)

    data = ReadInventory(**response.json())
    TestCase().assertIsInstance(data, ReadInventory)


def test_can_raise_not_found_on_get(client: TestClient):

    response = client.get("/inventory/1")

    assert response.status_code == 404


def test_can_get_one_by_id(client: TestClient, given_inventory):

    response = client.get("/inventory/1")

    assert response.status_code == 200

    data = ReadInventory(**response.json())
    assert data.id == 1


def test_can_reject_bad_params_on_get_by_id(client: TestClient, fake_repository):

    response = client.get("/inventory/foo")

    assert response.status_code == 422


def test_can_get_all(client: TestClient, given_inventory):

    response = client.get("/inventory/")

    assert response.status_code == 200

    item_list: List = response.json()
    test_ = TestCase()

    assert len(item_list) != 0
