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
