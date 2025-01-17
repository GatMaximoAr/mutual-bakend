from app.data import member as dto_member
from sqlalchemy.orm import Session
from app.models.repository import MemberRepository
from app.models.model import Member
from app.utils import model_to_dto
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List


async def create(member: dto_member.CreateMember, session: Session) -> BaseModel:

    new_member = Member(**member.model_dump())

    repo = MemberRepository(session=session)

    create_member = repo.create(new_data=new_member)

    dto = model_to_dto(load=create_member, dto=dto_member.ReadMember)

    return dto


async def get_one(member_dni: str, session: Session) -> BaseModel:

    repo = MemberRepository(session=session)

    db_query = repo.get_member_by_dni(model=Member, dni=member_dni)

    if db_query != None:
        # print(db_query)

        dto = model_to_dto(load=db_query, dto=dto_member.ReadMember)

        return dto

    raise HTTPException(
        status_code=404, detail=f"Member with DNI {member_dni} not found."
    )


async def get_all(session: Session) -> List[BaseModel]:

    repo = MemberRepository(session=session)
    member_list = []

    for member in repo.get_all(Member):
        if member:

            member_list.append(model_to_dto(member, dto_member.ReadMember))

    return member_list


async def update(dni: str, update_member: dto_member.UpdateMember, session: Session):

    repo = MemberRepository(session=session)

    update_data = repo.update_by_dni(
        model=Member, update_data=update_member, dni=dni  # type: ignore
    )
    if update_data:

        dto = model_to_dto(update_data, dto_member.ReadMember)

        return dto

    raise HTTPException(status_code=404, detail=f"Member with DNI {dni} not found.")


async def delete(member_dni: str, session: Session):

    repo = MemberRepository(session=session)

    if repo.delete(model=Member, dni=member_dni) == False:

        raise HTTPException(
            status_code=404, detail=f"Member with DNI {member_dni} not found."
        )
