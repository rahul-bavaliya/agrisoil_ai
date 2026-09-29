import uuid
from datetime import datetime
from typing import Any

from sqlmodel import Field, SQLModel


# Shared properties
class FarmFieldBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    geom: Any | None = None


# Properties to receive on farmfield creation
class FarmFieldCreate(FarmFieldBase):
    pass


# Properties to receive on farmfield update
class FarmFieldUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    geom: Any | None = None


# Properties to return via API, id is always required
class FarmFieldPublic(SQLModel):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime | None = None
    name: str
    description: str | None = None
    geom: Any | None = None


class FarmFieldsPublic(SQLModel):
    data: list[FarmFieldPublic]
    count: int
