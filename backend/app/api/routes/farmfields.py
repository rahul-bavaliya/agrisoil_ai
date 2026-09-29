import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import col, func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import FarmField
from app.schemas import (
    FarmFieldCreate,
    FarmFieldPublic,
    FarmFieldsPublic,
    FarmFieldUpdate,
    Message,
)

router = APIRouter(prefix="/farmfields", tags=["farmfields"])


@router.get("/", response_model=FarmFieldsPublic)
def read_farmfields(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve farm fields.
    """
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(FarmField)
        count = session.exec(count_statement).one()
        statement = (
            select(FarmField)
            .order_by(col(FarmField.created_at).desc())
            .offset(skip)
            .limit(limit)
        )
        fields = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(FarmField)
            .where(FarmField.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(FarmField)
            .where(FarmField.owner_id == current_user.id)
            .order_by(col(FarmField.created_at).desc())
            .offset(skip)
            .limit(limit)
        )
        fields = session.exec(statement).all()

    fields_public = [FarmFieldPublic.model_validate(f) for f in fields]
    return FarmFieldsPublic(data=fields_public, count=count)


@router.get("/{id}", response_model=FarmFieldPublic)
def read_farmfield(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get farm field by ID.
    """
    farmfield = session.get(FarmField, id)
    if not farmfield:
        raise HTTPException(status_code=404, detail="Farm field not found")
    if not current_user.is_superuser and (farmfield.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return farmfield


@router.post("/", response_model=FarmFieldPublic)
def create_farmfield(
    *, session: SessionDep, current_user: CurrentUser, farmfield_in: FarmFieldCreate
) -> Any:
    """
    Create new farm field.
    """
    farmfield = FarmField.model_validate(
        farmfield_in, update={"owner_id": current_user.id}
    )
    session.add(farmfield)
    session.commit()
    session.refresh(farmfield)
    return farmfield


@router.put("/{id}", response_model=FarmFieldPublic)
def update_farmfield(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    farmfield_in: FarmFieldUpdate,
) -> Any:
    """
    Update a farm field.
    """
    farmfield = session.get(FarmField, id)
    if not farmfield:
        raise HTTPException(status_code=404, detail="Farm field not found")
    if not current_user.is_superuser and (farmfield.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    update_dict = farmfield_in.model_dump(exclude_unset=True)
    farmfield.sqlmodel_update(update_dict)
    session.add(farmfield)
    session.commit()
    session.refresh(farmfield)
    return farmfield


@router.delete("/{id}")
def delete_farmfield(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a farm field.
    """
    farmfield = session.get(FarmField, id)
    if not farmfield:
        raise HTTPException(status_code=404, detail="Farm field not found")
    if not current_user.is_superuser and (farmfield.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    session.delete(farmfield)
    session.commit()
    return Message(message="Farm field deleted successfully")
