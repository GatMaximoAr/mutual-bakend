from app.data.inventory import ReadInventory
from app.models.model import Inventory
from app.mocks import inventory as mock_inventory
from unittest import TestCase


def test_can_repository_create(fake_repository):

    given = Inventory(**mock_inventory.RICE)
    expected = fake_repository.create(given)

    assert expected.id, "error in assert"


def test_repository_can_get_one(fake_repository, given_inventory):

    db_query = fake_repository.get_one(model=Inventory, id=1)

    assert db_query, "not matching result from db"


def test_repository_can_return_none_if_not_found(fake_repository):

    db_query = fake_repository.get_one(model=Inventory, id=1)

    assert db_query is None, "something is wrong here!"


def test_repository_can_get_all(fake_repository, given_inventory):

    item_list = fake_repository.get_all(Inventory)

    # print(item_list)

    assert len(item_list) == 1


def test_repository_can_update(fake_repository, given_inventory):

    expected_ = "new code"

    data = fake_repository.get_one(model=Inventory, id=1)

    data.code = expected_
    data = ReadInventory(
        code=data.code,
        id=data.id,
        description=data.description,
        price=data.price,
        quantity=data.quantity,
        weight=data.weight,
    )

    update_data = fake_repository.update(model=Inventory, update_data=data, id=1)

    assert update_data.code == expected_


def test_can_repository_delete(fake_repository, given_inventory):

    assert fake_repository.delete(model=Inventory, id=1) == True


def test_can_repository_return_false_if_not_found(fake_repository):

    assert fake_repository.delete(model=Inventory, id=1) == False
