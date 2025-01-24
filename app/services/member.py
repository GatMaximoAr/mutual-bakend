from app.data import member as dto_member
from sqlalchemy.orm import Session
from app.models.repository import MemberRepository
from app.models.model import Member, Address
from app.utils import model_to_dto
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List


async def create(member: dto_member.CreateMember, session: Session) -> BaseModel:

    new_member = Member(
        dni=member.dni,
        name=member.name,
        surname=member.surname,
        phone=member.phone,
        note=member.note,
        active=member.active,
    )

    for address in member.addresses:
        member_address = Address(
            member_dni=member.dni,
            city=address.city,
            province=address.province,
            reference=address.reference,
            street=address.street,
        )
        new_member.addresses.append(member_address)

    repo = MemberRepository(session=session)

    create_member = repo.create(new_member)

    return dto_member.ReadMember.model_validate(create_member)


async def get_one(member_dni: str, session: Session) -> BaseModel:

    repo = MemberRepository(session=session)

    db_query = repo.get_member_by_dni(model=Member, dni=member_dni)

    if db_query != None:
        # print(db_query)

        dto = dto_member.ReadMember.model_validate(db_query)

        return dto

    raise HTTPException(
        status_code=404, detail=f"Member with DNI {member_dni} not found."
    )


async def get_all(session: Session) -> List[dto_member.ReadMember]:

    repo = MemberRepository(session=session)
    member_list = []

    for member in repo.get_all(Member):
        if member:

            member_list.append(dto_member.ReadMember.model_validate(member))

    return member_list


async def update(dni: str, update_member: dto_member.UpdateMember, session: Session):

    repo = MemberRepository(session=session)

    update_data = repo.update_by_dni(
        model=Member, update_data=update_member, dni=dni  # type: ignore
    )
    if update_data:

        dto = dto_member.UpdateMember.model_validate(update_data)
        return dto

    raise HTTPException(status_code=404, detail=f"Member with DNI {dni} not found.")


async def delete(member_dni: str, session: Session):

    repo = MemberRepository(session=session)

    if repo.delete(model=Member, dni=member_dni) == False:

        raise HTTPException(
            status_code=404, detail=f"Member with DNI {member_dni} not found."
        )
