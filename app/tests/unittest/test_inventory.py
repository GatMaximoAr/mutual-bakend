from fastapi.testclient import TestClient
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


def test_can_reject_bad_params_on_get_by_id(client: TestClient):

    response = client.get("/inventory/foo")

    assert response.status_code == 422


def test_can_get_all(client: TestClient, given_inventory):

    response = client.get("/inventory/")

    assert response.status_code == 200

    item_list: List = response.json()

    assert len(item_list) != 0


def test_can_update_a_item(client: TestClient, given_inventory):

    old_data = mock_inventory.MILK
    expected_code = "New code"
    expected_description = "A update description"

    old_data["code"] = expected_code
    old_data["description"] = expected_description

    response = client.put("/inventory/1", json=old_data)
    assert response.status_code == 200

    update_data = ReadInventory(**response.json())
    assert update_data.code == expected_code
    assert update_data.description == expected_description


def test_can_raise_not_found_on_update(client: TestClient):

    old_data = mock_inventory.MILK
    expected_code = "New code"
    expected_description = "A update description"

    old_data["code"] = expected_code
    old_data["description"] = expected_description

    response = client.put("/inventory/1", json=old_data)
    assert response.status_code == 404


def test_can_reject_bad_params_on_update_by_id(client: TestClient):

    response = client.put("/inventory/foo", json={"bad-data": "data"})

    assert response.status_code == 422

    response = client.put("/inventory/1", json={"bad-data": "data"})

    assert response.status_code == 422


def test_can_delete_inventory(client: TestClient, given_inventory):

    response = client.delete("/inventory/1")

    assert response.status_code == 204


def test_can_raise_not_found_on_delete(client: TestClient):

    response = client.delete("/inventory/1")

    assert response.status_code == 404


def test_can_raise_bad_param(client: TestClient):

    response = client.delete("/inventory/foo")

    assert response.status_code == 422
