import uuid

from sqlmodel import Session

from app.models import FarmField
from app.schemas import FarmFieldCreate


def create_farmfield(
    *, session: Session, farmfield_in: FarmFieldCreate, owner_id: uuid.UUID
) -> FarmField:
    db_farmfield = FarmField.model_validate(
        farmfield_in, update={"owner_id": owner_id}
    )
    session.add(db_farmfield)
    session.commit()
    session.refresh(db_farmfield)
    return db_farmfield
