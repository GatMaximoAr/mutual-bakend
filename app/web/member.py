from fastapi import APIRouter, Depends
from app.data import member as dto_member
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.services import member as service
from typing import List

router = APIRouter(prefix="/member", tags=["member"])


@router.post("/", response_model=dto_member.ReadMember)
async def create(member: dto_member.CreateMember, session: Session = Depends(get_db)):

    new_member = await service.create(member=member, session=session)
    return new_member


@router.get("/", response_model=List[dto_member.ReadMember])
async def get_all(session: Session = Depends(get_db)):

    members = await service.get_all(session=session)

    return members


@router.get("/{member_dni}", response_model=dto_member.ReadMember)
async def get_one(member_dni: str, session: Session = Depends(get_db)):

    return await service.get_one(member_dni=member_dni, session=session)


@router.put("/{member_dni}", response_model=dto_member.UpdateMember)
async def update(
    member_dni: str,
    update_member: dto_member.UpdateMember,
    session: Session = Depends(get_db),
):

    update_data = await service.update(
        dni=member_dni, update_member=update_member, session=session
    )
    return update_data


@router.delete("/{member_dni}", status_code=204)
async def delete(member_dni: str, session: Session = Depends(get_db)):
    return await service.delete(member_dni=member_dni, session=session)
