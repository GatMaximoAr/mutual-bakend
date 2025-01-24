from fastapi.testclient import TestClient
from app.mocks import members
from app.data import member as dto_member
from app.models.model import Member


def test_can_create_member(client: TestClient):

    response = client.post("/member/", json=members.MEMBERS[0])
    assert response.status_code == 200

    member = dto_member.ReadMember(**response.json())
    # print(member)

    assert member != None


def test_can_get_one_member_by_dni(client: TestClient, given_member):

    response = client.get("/member/12345678")
    assert response.status_code == 200

    assert response.json()["dni"] == "12345678"


def test_can_return_exception_if_not_found(client: TestClient):

    response = client.get("/member/12345678")
    assert response.status_code == 404


def test_repository_can_get_all(client: TestClient, given_member):

    response = client.get("/member/")

    assert response.status_code == 200

    list_ = response.json()
    # print(list_)

    assert len(list_) > 0


def test_can_update(client: TestClient, given_member, fake_member_repository):
    existing_member = fake_member_repository.get_member_by_dni(
        model=Member, dni="12345678"
    )
    existing_member = dto_member.UpdateMember.model_validate(existing_member)

    existing_member.name = "Maximo"
    existing_member.addresses[0].city = "La paz"

    new_data = existing_member.model_dump_json()

    response = client.put("/member/12345678/", content=new_data)
    assert response.status_code == 200

    # update simple fields
    assert response.json()["name"] == "Maximo"
    # update address relationship fields
    assert response.json()["addresses"][0]["city"] == "La paz"


def test_can_on_update_add_new_address(
    client: TestClient, given_member, fake_member_repository
):
    existing_member = fake_member_repository.get_member_by_dni(
        model=Member, dni="12345678"
    )
    existing_member = dto_member.UpdateMember.model_validate(existing_member)

    expected_addreess = dto_member.UpdateAddress(
        member_dni="12345678",
        province="Cordoba",
        city="La paz",
        street="some street",
        reference="in a house",
    )
    existing_member.addresses.append(expected_addreess)

    update_data = existing_member.model_dump_json()

    response = client.put("/member/12345678/", content=update_data)
    assert response.status_code == 200

    assert len(response.json()["addresses"]) == 2


def test_can_on_update_delete_all_address_related(
    client: TestClient, given_member, fake_member_repository
):
    existing_member = fake_member_repository.get_member_by_dni(
        model=Member, dni="12345678"
    )
    existing_member = dto_member.UpdateMember.model_validate(existing_member)

    existing_member.addresses = []

    update_data = existing_member.model_dump_json()

    response = client.put("/member/12345678/", content=update_data)
    assert response.status_code == 200

    assert len(response.json()["addresses"]) == 0


def test_can_raise_not_found_on_update(client: TestClient):

    new_data = {
        "name": "Maximo",
        "surname": "Pérez",
        "phone": "+54 911 1234 5678",
        "active": True,
        "note": "Activo en el club.",
        "date_of_leaving": None,
        "date_of_entry": "2025-01-21",
        "addresses": [
            {
                "city": "Buenos Aires",
                "province": "Buenos Aires",
                "street": "Av. Corrientes 1234",
                "reference": "Frente al teatro.",
                "id": 1,
                "member_dni": "12345678",
            }
        ],
    }

    response = client.put("/member/12333/", json=new_data)
    assert response.status_code == 404


def test_can_delete_member(client: TestClient, given_member):

    response = client.delete("/member/12345678")

    assert response.status_code == 204
