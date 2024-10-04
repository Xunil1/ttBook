from sqlalchemy.orm import Session
from sqlalchemy import update

from fastapi import HTTPException

from db.models.position import Position
from schemas.position import PositionCreate, PositionUpdate

from db.repository.user import user_view


def position_view(position: Position):
    return {
        "id": position.id,
        "name": position.name,
        "company_id": position.company_id,
        "departmant_id": position.department_id,
    }


def create_our_position(pInfo: PositionCreate, db: Session):
    position_name = db.query(Position).filter(Position.name == pInfo.name).all()

    if position_name:
        raise HTTPException(status_code=400, detail="Name is taken")

    position = Position(
        name=pInfo.name,
        company_id=pInfo.company_id,
        department_id=pInfo.department_id,
    )
    db.add(position)
    db.commit()
    db.refresh(position)
    return position_view(position)


def get_position_info(p_id: int, db: Session):
    pos = db.query(Position).filter(Position.id == p_id).one_or_none()
    if not pos:
        raise HTTPException(status_code=400, detail="Position not found")
    return position_view(pos)


def get_positions_info(db: Session):
    positions = db.query(Position).all()
    data = []
    for position in positions:
        data.append(position_view(position))
    return data


def get_all_users(p_id: int, db: Session):
    pos = db.query(Position).filter(Position.id == p_id).one_or_none()
    if not pos:
        raise HTTPException(status_code=400, detail="User not found")

    users = [user_view(user) for user in pos.users]

    return users


def update_info(newInfo: PositionUpdate, p_id: int, db: Session):
    pos = db.query(Position).filter(Position.id == p_id).one_or_none()
    if not pos:
        raise HTTPException(status_code=400, detail="User not found")

    stmt = (
        update(Position).
        where(Position.id == p_id).
        values(name=newInfo.name,
               company_id=newInfo.company_id,
               department_id=newInfo.department_id,
               )
    )

    db.execute(stmt)
    db.commit()

    pos = db.query(Position).filter(Position.id == p_id).one_or_none()
    return position_view(pos)


def delete_position(p_id: int, db: Session):
    pos = db.query(Position).filter(Position.id == p_id).one_or_none()
    if not pos:
        raise HTTPException(status_code=400, detail="User not found")

    db.delete(pos)
    db.commit()
