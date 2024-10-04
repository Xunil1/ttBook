from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import Depends

from schemas.department import DepartmentCreate, DepartmentUpdate
from db.session import get_db

from db.repository.department import create_our_department, get_department_info, get_all_users, get_all_positions, update_info, delete_department, get_departments_info
from db.repository.user import isAdmin, valid_token


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/auth")


@router.post("/create")
def create_department(departmentInfo: DepartmentCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token, db)
    data = create_our_department(dInfo=departmentInfo, db=db)
    return data


@router.get("/getInfo/{department_id}")
def get_department_info_by_id(department_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token, db)
    data = get_department_info(d_id=department_id, db=db)
    return data


@router.get("/getAllDepartments")
def get_all_departments(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = get_departments_info(db=db)
    return data


@router.get("/getUsers/{department_id}")
def get_all_users_in_department(department_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token, db)
    data = get_all_users(d_id=department_id, db=db)
    return data


@router.get("/getPositions/{department_id}")
def get_all_positions_in_department(department_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token, db)
    data = get_all_positions(d_id=department_id, db=db)
    return data


@router.put("/update/{department_id}")
def update_department_by_id(department_id: int, department: DepartmentUpdate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = update_info(d_id=department_id, newInfo=department, db=db)
    return data


@router.delete("/delete/{department_id}", description="ПРЕДУПРЕЖДЕНИЕ: Удаление отдела повлечет за собой удаление должностей.")
def delete_department_by_id(department_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = delete_department(d_id=department_id, db=db)
    return data