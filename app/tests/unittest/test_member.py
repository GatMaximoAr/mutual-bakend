from fastapi.testclient import TestClient
from app.mocks import members
from app.data import member as dto_member


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


def test_can_update(client: TestClient, given_member):

    new_data = members.MEMBERS[0]
    expected_name = "Maximo"
    new_data["active"] = True
    new_data["date_of_entry"] = ("2025-01-17",)
    new_data["date_of_leaving"] = None

    new_data["name"] = expected_name

    response = client.put("/member/12345678/", json=new_data)
    assert response.status_code == 200

    assert response.json()["name"] == expected_name


def test_can_raise_not_found_on_update(client: TestClient):

    new_data = members.MEMBERS[0]
    new_data["active"] = True
    new_data["date_of_entry"] = ("2025-01-17",)
    new_data["date_of_leaving"] = None

    response = client.put("/member/12333/", json=new_data)
    assert response.status_code == 404


def test_can_delete_member(client: TestClient, given_member):

    response = client.delete("/member/12345678")

    assert response.status_code == 204
