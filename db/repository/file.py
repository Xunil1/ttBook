from sqlalchemy.orm import Session
from sqlalchemy import update

from fastapi import HTTPException

from db.models.file import File
from db.models.section import Section
from db.models.user import User
from db.models.company import Company
from db.models.department import Department
from db.models.position import Position

from schemas.file import FileUpdate, FileCreate, PermissionChange


def file_view(file: File):
    return {
        "id": file.id,
        "name": file.name,
        "url": file.url,
        "code": file.code if file.code else "",
        "allowed_all": file.allowed_all,
        "section_id": file.section.id if file.section else None,
        "allowed_users": [user.id for user in file.users],
        "allowed_positions": [position.id for position in file.positions],
        "allowed_departments": [department.id for department in file.departments],
        "allowed_companies": [company.id for company in file.companies],
    }


def get_file_info_by_id(f_id: int, db: Session):
    file = db.query(File).filter(File.id == f_id).one_or_none()
    if not file:
        raise HTTPException(status_code=400, detail="File not found")
    return file_view(file)


def create_our_file(fInfo: FileCreate, db: Session):
    file_name = db.query(File).filter(File.name == fInfo.name).all()
    if file_name:
        raise HTTPException(status_code=400, detail="Name is taken")

    try:
        fInfo.section_id = int(fInfo.section_id)
    except:
        fInfo.section_id = None

    if fInfo.section_id is not None:
        section = db.query(Section).filter(Section.id == fInfo.section_id).one_or_none()
        if section is None:
            raise HTTPException(status_code=400, detail="Section does not exist")

    file = File(
        name=fInfo.name,
        url=fInfo.url,
        code=fInfo.code,
        allowed_all=fInfo.allowed_all,
        section_id=fInfo.section_id,
    )
    db.add(file)
    db.commit()
    db.refresh(file)
    return file_view(file)


def get_files_by_section_id(s_id: int | None, db: Session):
    if s_id != 0:
        section = db.query(Section).filter(Section.id == s_id).one_or_none()
        if not section:
            raise HTTPException(status_code=400, detail="Section not found")
    else:
        s_id = None

    files = db.query(File).filter(File.section_id == s_id).all()
    return [{"id": file.id, "name": file.name} for file in files]



def add_allowed_user_to_file(f_id, u_id, db: Session):
    file = db.query(File).filter(File.id == f_id).one_or_none()
    if not file:
        raise HTTPException(status_code=400, detail="File not found")

    user = db.query(User).filter(User.id == u_id).one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    allowed_users = file.users
    if user not in allowed_users:
        allowed_users.append(user)
        file.users = allowed_users

        db.commit()

        file = db.query(File).filter(File.id == f_id).one_or_none()

    return file_view(file)


def add_allowed_position_to_file(f_id, p_id, db: Session):
    file = db.query(File).filter(File.id == f_id).one_or_none()
    if not file:
        raise HTTPException(status_code=400, detail="File not found")

    position = db.query(Position).filter(Position.id == p_id).one_or_none()
    if not position:
        raise HTTPException(status_code=400, detail="Position not found")

    allowed_position = file.positions
    if position not in allowed_position:
        allowed_position.append(position)
        file.positions = allowed_position
        for user in position.users:
            add_allowed_user_to_file(f_id, user.id, db)

        db.commit()

        file = db.query(File).filter(File.id == f_id).one_or_none()

    return file_view(file)


def add_allowed_department_to_file(f_id, d_id, db: Session):
    file = db.query(File).filter(File.id == f_id).one_or_none()
    if not file:
        raise HTTPException(status_code=400, detail="File not found")

    department = db.query(Department).filter(Department.id == d_id).one_or_none()
    if not department:
        raise HTTPException(status_code=400, detail="Department not found")

    allowed_department = file.departments
    if department not in allowed_department:
        allowed_department.append(department)
        file.departments = allowed_department
        for position in department.positions:
            add_allowed_position_to_file(f_id, position.id, db)
        db.commit()

        file = db.query(File).filter(File.id == f_id).one_or_none()

    return file_view(file)


def add_allowed_company_to_file(f_id, c_id, db: Session):
    file = db.query(File).filter(File.id == f_id).one_or_none()
    if not file:
        raise HTTPException(status_code=400, detail="File not found")

    company = db.query(Company).filter(Company.id == c_id).one_or_none()
    if not company:
        raise HTTPException(status_code=400, detail="Company not found")

    allowed_company = file.companies
    if company not in allowed_company:
        allowed_company.append(company)
        file.companies = allowed_company
        for department in company.departments:
            add_allowed_department_to_file(f_id, department.id, db)
        db.commit()

        file = db.query(File).filter(File.id == f_id).one_or_none()

    return file_view(file)


def remove_allowed_user_to_file(f_id, u_id, db: Session):
    file = db.query(File).filter(File.id == f_id).one_or_none()
    if not file:
        raise HTTPException(status_code=400, detail="File not found")

    user = db.query(User).filter(User.id == u_id).one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    allowed_users = file.users
    try:
        allowed_users.remove(user)
    except:
        pass
    file.users = allowed_users

    db.commit()

    file = db.query(File).filter(File.id == f_id).one_or_none()

    return file_view(file)


def remove_allowed_position_to_file(f_id, p_id, db: Session):
    file = db.query(File).filter(File.id == f_id).one_or_none()
    if not file:
        raise HTTPException(status_code=400, detail="File not found")

    position = db.query(Position).filter(Position.id == p_id).one_or_none()
    if not position:
        raise HTTPException(status_code=400, detail="Position not found")

    allowed_position = file.positions
    try:
        allowed_position.remove(position)
    except:
        pass

    for user in position.users:
        remove_allowed_user_to_file(f_id, user.id, db)

    file.positions = allowed_position

    db.commit()

    file = db.query(File).filter(File.id == f_id).one_or_none()

    return file_view(file)


def remove_allowed_department_to_file(f_id, d_id, db: Session):
    file = db.query(File).filter(File.id == f_id).one_or_none()
    if not file:
        raise HTTPException(status_code=400, detail="File not found")

    department = db.query(Department).filter(Department.id == d_id).one_or_none()
    if not department:
        raise HTTPException(status_code=400, detail="Department not found")

    allowed_department = file.departments
    try:
        allowed_department.remove(department)
    except:
        pass

    for position in department.positions:
        remove_allowed_position_to_file(f_id, position.id, db)

    file.departments = allowed_department

    db.commit()

    file = db.query(File).filter(File.id == f_id).one_or_none()

    return file_view(file)


def remove_allowed_company_to_file(f_id, c_id, db: Session):
    file = db.query(File).filter(File.id == f_id).one_or_none()
    if not file:
        raise HTTPException(status_code=400, detail="File not found")

    company = db.query(Company).filter(Company.id == c_id).one_or_none()
    if not company:
        raise HTTPException(status_code=400, detail="Company not found")

    allowed_company = file.companies
    try:
        allowed_company.remove(company)
    except:
        pass

    for department in company.departments:
        remove_allowed_department_to_file(f_id, department.id, db)

    file.companies = allowed_company

    db.commit()

    file = db.query(File).filter(File.id == f_id).one_or_none()

    return file_view(file)


def update_info_by_id(f_id: int, newInfo: FileUpdate, db: Session):
    file = db.query(File).filter(File.id == f_id).one_or_none()
    if not file:
        raise HTTPException(status_code=400, detail="File does not exist")

    if file.name != newInfo.name:
        files = db.query(File).filter(File.name == newInfo.name).all()
        if files:
            raise HTTPException(status_code=400, detail="Name is taken")

    try:
        newInfo.section_id = int(newInfo.section_id)
    except:
        newInfo.section_id = None

    if newInfo.section_id is not None:
        section = db.query(Section).filter(Section.id == newInfo.section_id).one_or_none()
        if section is None:
            raise HTTPException(status_code=400, detail="Section does not exist")

    stmt = (
        update(File).
        where(File.id == f_id).
        values(name=newInfo.name,
               url=newInfo.url,
               code=newInfo.code,
               allowed_all=newInfo.allowed_all,
               section_id=newInfo.section_id,
               )
    )

    db.execute(stmt)
    db.commit()

    file = db.query(File).filter(File.id == f_id).one_or_none()
    return file_view(file)


def delete_file_by_id(f_id: int, db: Session):
    file = db.query(File).filter(File.id == f_id).one_or_none()
    if not file:
        raise HTTPException(status_code=400, detail="File does not exist")
    db.delete(file)
    db.commit()
