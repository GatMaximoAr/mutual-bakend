from app.models.model import Member, Address
from app.mocks import members as mock_member
from app.data import member as dto_member


def test_can_repository_create_member(fake_member_repository):
    data = mock_member.MEMBERS[0]

    member = Member(
        dni=data["dni"],
        name=data["name"],
        surname=data["surname"],
        phone=data["phone"],
        note=data["note"],
    )
    address = Address(**data["addresses"][0])
    member.addresses.append(address)

    expected = fake_member_repository.create(member)

    # print(expected)
    assert expected.dni == "12345678", "something wrong"


def test_can_repository_get_one_by_dni(fake_member_repository, given_member):

    db_query = fake_member_repository.get_member_by_dni(model=Member, dni="12345678")

    assert db_query != None


def test_can_repository_return_false_if_not_found_member(fake_member_repository):

    db_query = fake_member_repository.get_member_by_dni(model=Member, dni="123456789")
    assert db_query == None


def test_can_repository_update_address_relationship(
    fake_member_repository, given_member
):

    expected_reference = "some nicely update reference"

    before_ = fake_member_repository.get_member_by_dni(model=Member, dni="12345678")

    update_data = dto_member.UpdateMember.model_validate(before_)
    update_data.addresses[0].reference = expected_reference
    # print(update_data.addresses[0])

    then_ = fake_member_repository.update_by_dni(
        model=Member, dni=before_.dni, update_data=update_data
    )
    # print(then_)

    assert then_.addresses[0].reference == expected_reference


def test_can_repository_update_address_relationship_to_add(
    fake_member_repository, given_member
):
    expected_addreess = dto_member.UpdateAddress(
        member_dni="12345678",
        province="Cordoba",
        city="La paz",
        street="some street",
        reference="in a house",
    )

    before_ = fake_member_repository.get_member_by_dni(model=Member, dni="12345678")

    update_data = dto_member.UpdateMember.model_validate(before_)

    update_data.addresses.append(expected_addreess)

    then_ = fake_member_repository.update_by_dni(
        model=Member, dni=before_.dni, update_data=update_data
    )
    print(then_)

    assert len(then_.addresses) == 2


def test_can_repository_update_address_relationship_to_delete(
    fake_member_repository, given_member
):
    expected_addreess = dto_member.UpdateAddress(
        member_dni="12345678",
        province="Cordoba",
        city="La paz",
        street="some street",
        reference="in a house",
    )

    before_ = fake_member_repository.get_member_by_dni(model=Member, dni="12345678")

    update_data = dto_member.UpdateMember.model_validate(before_)

    update_data.addresses = [expected_addreess]

    then_ = fake_member_repository.update_by_dni(
        model=Member, dni=before_.dni, update_data=update_data
    )
    print(then_)

    assert then_.addresses[0].province == expected_addreess.province


def test_can_repository_update_address_relationship_with_empty(
    fake_member_repository, given_member
):

    before_ = fake_member_repository.get_member_by_dni(model=Member, dni="12345678")
    # print(before_)

    assert len(before_.addresses) > 0

    update_data = dto_member.UpdateMember.model_validate(before_)
    update_data.addresses = []
    # print(update_data)

    then_ = fake_member_repository.update_by_dni(
        model=Member, dni=before_.dni, update_data=update_data
    )
    # print(then_)

    assert len(then_.addresses) == 0


def test_can_repository_delete(fake_member_repository, given_member):

    assert fake_member_repository.delete(model=Member, dni="12345678") == True
