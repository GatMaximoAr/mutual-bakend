from app.models.model import Member
from app.mocks import members as mock_member


def test_can_repository_create_member(fake_member_repository):

    member = Member(**mock_member.MEMBERS[1])

    expected = fake_member_repository.create(member)

    # print(expected)

    assert expected.dni, "something wrong"


def test_can_repository_get_one_by_dni(fake_member_repository, given_member):

    db_query = fake_member_repository.get_member_by_dni(model=Member, dni="12345678")

    assert db_query != None


def test_can_repository_return_false_if_not_found_member(fake_member_repository):

    db_query = fake_member_repository.get_member_by_dni(model=Member, dni="123456789")
    assert db_query == None


def test_can_repository_delete(fake_member_repository, given_member):

    assert fake_member_repository.delete(model=Member, dni="12345678") == True
