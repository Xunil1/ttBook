from sqlalchemy.orm import Session
from sqlalchemy import update

from fastapi import HTTPException

from db.models.company import Company
from schemas.company import CompanyCreate, CompanyUpdate

from db.repository.user import user_view
from db.repository.position import position_view
from db.repository.department import department_view


def company_view(company: Company):
    return {
        "id": company.id,
        "name": company.name,
    }


def create_our_company(cInfo: CompanyCreate, db: Session):
    company_name = db.query(Company).filter(Company.name == cInfo.name).all()

    if company_name:
        raise HTTPException(status_code=400, detail="Name is taken")

    company = Company(
        name=cInfo.name,
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company_view(company)


def get_company_info(c_id: int, db: Session):
    company = db.query(Company).filter(Company.id == c_id).one_or_none()
    if not company:
        raise HTTPException(status_code=400, detail="Company not found")
    return company_view(company)


def get_companies_info(db: Session):
    companies = db.query(Company).all()
    data = []
    for company in companies:
        data.append(company_view(company))
    return data


def get_all_users(c_id: int, db: Session):
    comp = db.query(Company).filter(Company.id == c_id).one_or_none()
    if not comp:
        raise HTTPException(status_code=400, detail="Company not found")

    users = [user_view(user) for user in comp.users]

    return users


def get_all_positions(c_id: int, db: Session):
    comp = db.query(Company).filter(Company.id == c_id).one_or_none()

    if not comp:
        raise HTTPException(status_code=400, detail="Company not found")

    positions = [position_view(position) for position in comp.positions]

    return positions


def get_all_departments(c_id: int, db: Session):
    comp = db.query(Company).filter(Company.id == c_id).one_or_none()
    if not comp:
        raise HTTPException(status_code=400, detail="Company not found")

    departments = [department_view(department) for department in comp.departments]

    return departments


def update_info(newInfo: CompanyUpdate, c_id: int, db: Session):
    company = db.query(Company).filter(Company.id == c_id).one_or_none()
    if not company:
        raise HTTPException(status_code=400, detail="Company not found")

    stmt = (
        update(Company).
        where(Company.id == c_id).
        values(name=newInfo.name,
               )
    )

    db.execute(stmt)
    db.commit()

    company = db.query(Company).filter(Company.id == c_id).one_or_none()
    return company_view(company)


def delete_company(c_id: int, db: Session):
    company = db.query(Company).filter(Company.id == c_id).one_or_none()

    for department in company.departments:
        db.delete(department)
    for position in company.positions:
        db.delete(position)

    if not company:
        raise HTTPException(status_code=400, detail="Company does not exist")
    db.delete(company)
    db.commit()
    return {"status": "OK"}
