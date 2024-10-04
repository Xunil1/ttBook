from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import Depends

from core.jwt_token import verify_jwt_token
from typing import Annotated, Union

from db.models.user import User

from schemas.user import UserCreate, UserSelfUpdate, UserAdminUpdate, UserChangePassword
from db.session import get_db
from db.repository.user import create_new_user, auth_current_user, isAdmin, get_user_info, get_users_info, self_update_info, get_user_info_by_id, update_info_by_id, user_change_pass, user_change_pass_by_id, delete_user_by_id, get_files, valid_token


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/auth")


@router.post("/auth")
def auth_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    data = auth_current_user(form_data.username, form_data.password, db=db)
    return data


@router.get("/checkAuth")
def check_auth(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return valid_token(token=token, db=db)


@router.get("/getInfo")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    data = get_user_info(token=token, db=db)
    return data


@router.get("/getInfo/{user_id}")
def get_user_by_id(user_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = get_user_info_by_id(u_id=user_id, token=token, db=db)
    return data


@router.get("/getAllUsers")
def get_all_users(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = get_users_info(db=db)
    return data


@router.post("/add")
def create_user(user: UserCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = create_new_user(user=user, db=db)
    return data

# @router.post("/add")
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     data = create_new_user(user=user, db=db)
#     return data


@router.put("/update")
def update_current_user(user: UserSelfUpdate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    data = self_update_info(newInfo=user, token=token, db=db)
    return data


@router.put("/update/{user_id}")
def update_user_by_id(user_id: int, user: UserAdminUpdate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = update_info_by_id(u_id=user_id, newInfo=user, db=db)
    return data


@router.put("/changePass")
def change_self_password(change: UserChangePassword, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    data = user_change_pass(newPass=change.password, token=token, db=db)
    return data


@router.put("/changePass/{user_id}")
def change_user_password_by_id(user_id: int, change: UserChangePassword, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = user_change_pass_by_id(u_id=user_id, newPass=change.password, token=token, db=db)
    return data


@router.delete("/delete/{user_id}")
def delete_user(user_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = delete_user_by_id(u_id=user_id, db=db)
    return data


@router.get("/getAllowedFiles")
def get_allowed_files(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    data = get_files(token=token, db=db)
    return data