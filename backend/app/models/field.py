import uuid
from datetime import UTC, datetime
from typing import Any

from geoalchemy2 import Geometry
from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel

from app.models.user import User


def get_datetime_utc() -> datetime:
    return datetime.now(UTC)


class FarmField(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)

    # GIS Geometry Polygon Field (PostGIS SRID 4326 for WGS84 GPS Coordinates)
    geom: Any | None = Field(
        default=None,
        sa_type=Geometry(geometry_type="POLYGON", srid=4326, spatial_index=True),  # type: ignore
    )

    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship()

    # Audit Fields
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )

