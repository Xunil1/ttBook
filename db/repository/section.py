from sqlalchemy.orm import Session
from sqlalchemy import update

from fastapi import HTTPException

from db.models.file import File
from db.models.section import Section
from db.models.user import User
from db.models.company import Company
from db.models.department import Department
from db.models.position import Position

from schemas.section import SectionCreate, SectionUpdate

from db.repository.user import user_view
from db.repository.position import position_view
from db.repository.department import department_view
from db.repository.company import company_view

def section_view(section: Section):
    return {
        "id": section.id,
        "name": section.name,
        "allowed_all": section.allowed_all,
        "file_list": [{'id': file.id, "name": file.name} for file in section.files],
        "allowed_users": [user.id for user in section.users],
        "allowed_positions": [position.id for position in section.positions],
        "allowed_departments": [department.id for department in section.departments],
        "allowed_companies": [company.id for company in section.companies],

    }

def get_section_info_by_id(s_id:int, db: Session):
    section = db.query(Section).filter(Section.id == s_id).one_or_none()
    if not section:
        raise HTTPException(status_code=400, detail="Section not found")
    return section_view(section)


def create_our_section(secInfo: SectionCreate, db: Session):
    if len(secInfo.name) == 0:
        raise HTTPException(status_code=400, detail="Name cannot be empty")

    section_name = db.query(Section).filter(Section.name == secInfo.name).all()
    if section_name:
        raise HTTPException(status_code=400, detail="Name is taken")

    section = Section(
        name=secInfo.name,
        allowed_all=secInfo.allowed_all,
    )
    db.add(section)
    db.commit()
    db.refresh(section)
    return section_view(section)


def get_all_sections_info(db: Session):
    sections = db.query(Section).all()
    data = []
    for section in sections:
        data.append(section_view(section))
    return data


def add_allowed_user_to_section(s_id: int, u_id: int, db: Session):
    section = db.query(Section).filter(Section.id == s_id).one_or_none()
    if not section:
        raise HTTPException(status_code=400, detail="Section not found")

    user = db.query(User).filter(User.id == u_id).one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    allowed_users = section.users
    if user not in allowed_users:
        allowed_users.append(user)
        section.users = allowed_users

        db.commit()

        section = db.query(Section).filter(Section.id == s_id).one_or_none()

    return section_view(section)


def add_allowed_position_to_section(s_id: int, p_id: int, db: Session):
    section = db.query(Section).filter(Section.id == s_id).one_or_none()
    if not section:
        raise HTTPException(status_code=400, detail="Section not found")

    position = db.query(Position).filter(Position.id == p_id).one_or_none()
    if not position:
        raise HTTPException(status_code=400, detail="Position not found")

    allowed_position = section.positions
    if position not in allowed_position:
        allowed_position.append(position)
        section.positions = allowed_position
        for user in position.users:
            add_allowed_user_to_section(s_id, user.id, db)

        db.commit()

        section = db.query(Section).filter(Section.id == s_id).one_or_none()

    return section_view(section)


def add_allowed_department_to_section(s_id: int, d_id: int, db: Session):
    section = db.query(Section).filter(Section.id == s_id).one_or_none()
    if not section:
        raise HTTPException(status_code=400, detail="Section not found")

    department = db.query(Department).filter(Department.id == d_id).one_or_none()
    if not department:
        raise HTTPException(status_code=400, detail="Department not found")

    allowed_department = section.departments
    if department not in allowed_department:
        allowed_department.append(department)
        section.departments = allowed_department
        for position in department.positions:
            add_allowed_position_to_section(s_id, position.id, db)
        db.commit()

        section = db.query(Section).filter(Section.id == s_id).one_or_none()

    return section_view(section)


def add_allowed_company_to_section(s_id: int, c_id: int, db: Session):
    section = db.query(Section).filter(Section.id == s_id).one_or_none()
    if not section:
        raise HTTPException(status_code=400, detail="Section not found")

    company = db.query(Company).filter(Company.id == c_id).one_or_none()
    if not company:
        raise HTTPException(status_code=400, detail="Company not found")

    allowed_company = section.companies
    if company not in allowed_company:
        allowed_company.append(company)
        section.companies = allowed_company
        for department in company.departments:
            add_allowed_department_to_section(s_id, department.id, db)
        db.commit()

        section = db.query(Section).filter(Section.id == s_id).one_or_none()

    return section_view(section)


def remove_allowed_user_to_section(s_id: int, u_id: int, db: Session):
    section = db.query(Section).filter(Section.id == s_id).one_or_none()
    if not section:
        raise HTTPException(status_code=400, detail="Section not found")

    user = db.query(User).filter(User.id == u_id).one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    allowed_users = section.users
    try:
        allowed_users.remove(user)
    except:
        pass
    section.users = allowed_users

    db.commit()

    section = db.query(Section).filter(Section.id == s_id).one_or_none()

    return section_view(section)


def remove_allowed_position_to_section(s_id: int, p_id: int, db: Session):
    section = db.query(Section).filter(Section.id == s_id).one_or_none()
    if not section:
        raise HTTPException(status_code=400, detail="Section not found")

    position = db.query(Position).filter(Position.id == p_id).one_or_none()
    if not position:
        raise HTTPException(status_code=400, detail="Position not found")

    allowed_position = section.positions
    try:
        allowed_position.remove(position)
    except:
        pass

    for user in position.users:
        remove_allowed_user_to_section(s_id, user.id, db)

    section.positions = allowed_position

    db.commit()

    section = db.query(Section).filter(Section.id == s_id).one_or_none()

    return section_view(section)


def remove_allowed_department_to_section(s_id: int, d_id: int, db: Session):
    section = db.query(Section).filter(Section.id == s_id).one_or_none()
    if not section:
        raise HTTPException(status_code=400, detail="File not found")

    department = db.query(Department).filter(Department.id == d_id).one_or_none()
    if not department:
        raise HTTPException(status_code=400, detail="Department not found")

    allowed_department = section.departments
    try:
        allowed_department.remove(department)
    except:
        pass

    for position in department.positions:
        remove_allowed_position_to_section(s_id, position.id, db)

    section.departments = allowed_department

    db.commit()

    section = db.query(Section).filter(Section.id == s_id).one_or_none()

    return section_view(section)


def remove_allowed_company_to_section(s_id: int, c_id: int, db: Session):
    section = db.query(Section).filter(Section.id == s_id).one_or_none()
    if not section:
        raise HTTPException(status_code=400, detail="File not found")

    company = db.query(Company).filter(Company.id == c_id).one_or_none()
    if not company:
        raise HTTPException(status_code=400, detail="Company not found")

    allowed_company = section.companies
    try:
        allowed_company.remove(company)
    except:
        pass

    for department in company.departments:
        remove_allowed_department_to_section(s_id, department.id, db)

    section.companies = allowed_company

    db.commit()

    section = db.query(Section).filter(Section.id == s_id).one_or_none()

    return section_view(section)


def add_file_to_section(s_id: int, f_id: int, db: Session):
    section = db.query(Section).filter(Section.id == s_id).one_or_none()
    if not section:
        raise HTTPException(status_code=400, detail="Section does not exist")

    file = db.query(File).filter(File.id == f_id).one_or_none()
    if not file:
        raise HTTPException(status_code=400, detail="File does not exist")

    file.section_id = section.id
    db.commit()

    return section_view(section)


def remove_file_in_section(s_id: int, f_id: int, db: Session):
    section = db.query(Section).filter(Section.id == s_id).one_or_none()
    if not section:
        raise HTTPException(status_code=400, detail="Section does not exist")

    file = db.query(File).filter(File.id == f_id).one_or_none()
    if not file:
        raise HTTPException(status_code=400, detail="File does not exist")

    file.section_id = None
    db.commit()

    return section_view(section)

def update_info_by_id(s_id: int, newInfo: SectionUpdate, db: Session):

    if len(newInfo.name) == 0:
        raise HTTPException(status_code=400, detail="Name cannot be empty")

    section = db.query(Section).filter(Section.id == s_id).one_or_none()
    if not section:
        raise HTTPException(status_code=400, detail="Section does not exist")

    if section.name != newInfo.name:
        files = db.query(Section).filter(Section.name == newInfo.name).all()
        if files:
            raise HTTPException(status_code=400, detail="Name is busy")


    stmt = (
        update(Section).
        where(Section.id == s_id).
        values(name=newInfo.name,
               allowed_all=newInfo.allowed_all,
               )
    )

    db.execute(stmt)
    db.commit()

    section = db.query(Section).filter(Section.id == s_id).one_or_none()
    return section_view(section)


def delete_section_by_id(s_id: int, db: Session):
    section = db.query(Section).filter(Section.id == s_id).one_or_none()
    if not section:
        raise HTTPException(status_code=400, detail="Section does not exist")
    db.delete(section)
    db.commit()