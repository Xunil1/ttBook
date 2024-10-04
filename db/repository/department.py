from sqlalchemy.orm import Session
from sqlalchemy import update

from fastapi import HTTPException

from db.models.department import Department
from schemas.department import DepartmentCreate, DepartmentUpdate

from db.repository.user import user_view
from db.repository.position import position_view

def department_view(department: Department):
    return {
        "id": department.id,
        "name": department.name,
        "company_id": department.company_id,
    }


def create_our_department(dInfo: DepartmentCreate, db: Session):
    department_name = db.query(Department).filter(Department.name == dInfo.name).all()

    if department_name:
        raise HTTPException(status_code=400, detail="Name is taken")

    department = Department(
        name=dInfo.name,
        company_id=dInfo.company_id,
    )
    db.add(department)
    db.commit()
    db.refresh(department)
    return department


def get_department_info(d_id: int, db: Session):
    dep = db.query(Department).filter(Department.id == d_id).one_or_none()
    if not dep:
        raise HTTPException(status_code=400, detail="Department not found")
    return department_view(dep)


def get_departments_info(db: Session):
    departments = db.query(Department).all()
    data = []
    for department in departments:
        data.append(department_view(department))
    return data


def get_all_users(d_id: int, db: Session):
    dep = db.query(Department).filter(Department.id == d_id).one_or_none()
    if not dep:
        raise HTTPException(status_code=400, detail="Department not found")

    users = [user_view(user) for user in dep.users]

    return users


def get_all_positions(d_id: int, db: Session):
    dep = db.query(Department).filter(Department.id == d_id).one_or_none()

    if not dep:
        raise HTTPException(status_code=400, detail="Department not found")

    positions = [position_view(position) for position in dep.positions]

    return positions


def update_info(newInfo: DepartmentUpdate, d_id: int, db: Session):
    dep = db.query(Department).filter(Department.id == d_id).one_or_none()

    if not dep:
        raise HTTPException(status_code=400, detail="Department not found")

    stmt = (
        update(Department).
        where(Department.id == d_id).
        values(name=newInfo.name,
               company_id=newInfo.company_id,
               )
    )

    db.execute(stmt)
    db.commit()

    dep = db.query(Department).filter(Department.id == d_id).one_or_none()
    return department_view(dep)


def delete_department(d_id: int, db: Session):
    dep = db.query(Department).filter(Department.id == d_id).one_or_none()

    if not dep:
        raise HTTPException(status_code=400, detail="Department not found")

    for position in dep.positions:
        db.delete(position)

    db.delete(dep)
    db.commit()

    return {"status": "OK"}