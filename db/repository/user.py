import sqlalchemy.exc
from sqlalchemy.orm import Session
from sqlalchemy import update

from fastapi import HTTPException

from db.models.user import User
from db.models.file import File
from db.models.section import Section

from schemas.user import UserCreate, UserSelfUpdate, UserAdminUpdate

from core.jwt_token import verify_jwt_token
from core.hashing import Hasher
from core.jwt_token import create_jwt_token, EXPIRATION_TIME

from datetime import datetime, timedelta

from db.repository.file import file_view


def user_view(user: User):
    return {
        "id": user.id,
        "fname": user.firstname,
        "lname": user.lastname,
        "mname": user.middlename,
        "fullname": f'{user.lastname} {user.firstname} {user.middlename}',
        "company": user.company.name if user.company else None,
        "company_id": user.company.id if user.company else None,
        "department": user.department.name if user.department else None,
        "department_id": user.department.id if user.department else None,
        "position": user.position.name if user.position else None,
        "position_id": user.position.id if user.position else None,
        "email": user.email,
        "office_phone": user.office_phone,
        "phone": user.phone,
        "status": user.status,
        "is_admin": user.is_admin,
    }


def valid_token(token: str, db: Session):
    decoded_data = verify_jwt_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    c_user: User = db.query(User).filter(User.email == decoded_data["email"]).one_or_none()
    if not c_user:
        raise HTTPException(status_code=400, detail="User not found")
    return True


def isAdmin(token: str, db: Session):
    decoded_data = verify_jwt_token(token)
    c_user: User = db.query(User).filter(User.email == decoded_data["email"]).one_or_none()
    if not c_user.is_admin:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True


def auth_current_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).one_or_none()

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    is_password_correct = Hasher.verify_password(password, user.password)

    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if user.token and verify_jwt_token(user.token):
        return {"access_token": user.token, "token_type": "bearer", "isAdmin": user.is_admin}



    jwt_token = create_jwt_token({
        "exp": EXPIRATION_TIME,
        "email": user.email,
    })

    stmt = (
        update(User).
        where(User.email == user.email).
        values(token=jwt_token,
               )
    )

    db.execute(stmt)
    db.commit()

    return {"access_token": jwt_token, "token_type": "bearer", "isAdmin": user.is_admin }


def get_user_info(token: str, db: Session):
    decoded_data = verify_jwt_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    c_user: User = db.query(User).filter(User.email == decoded_data["email"]).one_or_none()
    if not c_user:
        raise HTTPException(status_code=400, detail="User not found")

    return user_view(c_user)


def get_user_info_by_id(u_id:int, token: str, db: Session):
    user = db.query(User).filter(User.id == u_id).one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user_view(user)


def get_users_info(db: Session):
    users = db.query(User).all()
    data = []
    for user in users:
        data.append(user_view(user))
    data.sort(key=lambda x: x["fullname"])
    return data


def create_new_user(user: UserCreate, db: Session):

    users_email = db.query(User).filter(User.email == user.email).all()
    users_phone = db.query(User).filter(User.phone == user.phone).all()

    if users_email:
        raise HTTPException(status_code=400, detail="Email is taken")
    if users_phone:
        raise HTTPException(status_code=400, detail="Phone is taken")
    if len(user.password) == 0:
        raise HTTPException(status_code=400, detail="Password can not be empty")

    user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        middlename=user.middlename,
        company_id=user.company_id if user.company_id else None,
        department_id=user.department_id if user.department_id else None,
        position_id=user.position_id if user.position_id else None,
        email=user.email,
        password=Hasher.get_password_hash(user.password),
        office_phone=user.office_phone,
        phone=user.phone,
        status=user.status,
        is_admin=user.is_admin,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user_view(user)


def self_update_info(newInfo: UserSelfUpdate, token: str, db: Session):
    decoded_data = verify_jwt_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    c_user: User = db.query(User).filter(User.email == decoded_data["email"]).one_or_none()
    if not c_user:
        raise HTTPException(status_code=400, detail="User not found")

    users_phone = db.query(User).filter(User.phone == newInfo.phone).all()

    if users_phone:
        raise HTTPException(status_code=400, detail="Phone is taken")

    stmt = (
        update(User).
        where(User.email == c_user.email).
        values(firstname=newInfo.firstname,
               lastname=newInfo.lastname,
               middlename=newInfo.middlename,
               phone=newInfo.phone,
               token=None,
               )
    )

    db.execute(stmt)
    db.commit()

    c_user = db.query(User).filter(User.email == c_user.email).one_or_none()
    return user_view(c_user)


def update_info_by_id(u_id: int, newInfo: UserAdminUpdate, db: Session):

    user = db.query(User).filter(User.id == u_id).one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")

    if user.email != newInfo.email:
        users_email = db.query(User).filter(User.email == newInfo.email).all()
        if users_email:
            raise HTTPException(status_code=400, detail="Email is taken")
    if user.phone != newInfo.phone:
        users_phone = db.query(User).filter(User.phone == newInfo.phone).all()
        if users_phone:
            raise HTTPException(status_code=400, detail="Phone is taken")

    admin_count = len(db.query(User).filter(User.is_admin == True).all())
    if admin_count == 1 and not newInfo.is_admin:
        raise HTTPException(status_code=400, detail="The last admin cannot be removed")


    stmt = (
        update(User).
        where(User.id == u_id).
        values(firstname=newInfo.firstname,
               lastname=newInfo.lastname,
               middlename=newInfo.middlename,
               phone=newInfo.phone,
               company_id=newInfo.company_id if newInfo.company_id != 0 else None,
               department_id=newInfo.department_id if newInfo.department_id != 0 else None,
               position_id=newInfo.position_id if newInfo.position_id != 0 else None,
               email=newInfo.email,
               office_phone=newInfo.office_phone,
               is_admin=newInfo.is_admin,
               status=newInfo.status,
               token=None,
               )
    )

    db.execute(stmt)
    db.commit()

    user = db.query(User).filter(User.id == u_id).one_or_none()
    return user_view(user)


def user_change_pass(newPass: str, token: str, db: Session):
    decoded_data = verify_jwt_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    c_user: User = db.query(User).filter(User.email == decoded_data["email"]).one_or_none()
    if not c_user:
        raise HTTPException(status_code=400, detail="User not found")
    if len(newPass) == 0:
        raise HTTPException(status_code=400, detail="Password can not be empty")

    stmt = (
        update(User).
        where(User.id == c_user.id).
        values(password=Hasher.get_password_hash(newPass),
               token=None,
               )
    )

    db.execute(stmt)
    db.commit()
    pass


def user_change_pass_by_id(u_id: int, newPass: str, token: str, db: Session):
    user = db.query(User).filter(User.id == u_id).one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")
    if len(newPass) == 0:
        raise HTTPException(status_code=400, detail="Password can not be empty")
    stmt = (
        update(User).
        where(User.id == u_id).
        values(password=Hasher.get_password_hash(newPass),
               token=None,
               )
    )

    db.execute(stmt)
    db.commit()
    pass

def delete_user_by_id(u_id: int, db: Session):
    user = db.query(User).filter(User.id == u_id).one_or_none()
    admins = db.query(User).filter(User.is_admin).all()

    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")

    if user in admins and len(admins) == 1:
        raise HTTPException(status_code=400, detail="The user is the only admin, there is no way to delete him")

    try:
        db.delete(user)
        db.commit()
        return True
    except sqlalchemy.exc.InternalError as ex:
        return False


def get_files(token: str, db: Session):

    name_section_without_section = "Без раздела"

    decoded_token = verify_jwt_token(token)

    if decoded_token is None:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = db.query(User).filter(User.email == decoded_token["email"]).one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")



    allowed_sections = dict() # Все доступные разделы

    if not user.is_admin:
        allowed_sections_to_user = user.sections                                                # Все доступные разделы для пользователя
        allowed_sections_to_all = db.query(Section).filter(Section.allowed_all == True).all()   # Все общедоступные разделы

        all_allowed_sections = allowed_sections_to_all + allowed_sections_to_user
    else:
        all_allowed_sections = db.query(Section).all()

    structured_files = {}

    for i in all_allowed_sections:
        structured_files[i.name] = {
            "id": i.id,
            "files": [],
        }
        if i.id not in allowed_sections:
            allowed_sections[i.id] = i


    files_in_sections = []
    for i in allowed_sections.values():
        files_in_sections.extend(i.files)


    allowed_files = dict()
    if not user.is_admin:
        allowed_files_to_user = user.files                                                      # Все доступные файлы для пользователя
        allowed_files_to_all = db.query(File).filter(File.allowed_all == True).all()            # Все общедоступные файлы

        all_allowed_files = files_in_sections + allowed_files_to_all + allowed_files_to_user
    else:
        all_allowed_files = db.query(File).all()
    for i in all_allowed_files:
        if i.id not in allowed_files:
            allowed_files[i.id] = i
    structured_files[name_section_without_section] = {
        "id": "None",
        "files": [],
    }
    for i in allowed_files.values():
        if i.section:

            if i.section.name in structured_files:
                structured_files[i.section.name]["files"].append(i)
            else:
                structured_files[i.section.name] = {
                    "id": i.section.id,
                    "files": [i]
                }
        else:
            structured_files[name_section_without_section]["files"].append(i)

    return_data = []

    for key in structured_files:
        return_data.append({
            "sectionName": key,
            "section_id": structured_files[key]["id"],
            "pages": [{"pageName": page.name, "pageId": page.id} for page in structured_files[key]["files"]]
        })

    return_data.sort(key=lambda x: x["sectionName"] and x["sectionName"] != name_section_without_section, reverse=True)



    return return_data







