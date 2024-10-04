from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import Depends

from schemas.company import CompanyCreate, CompanyUpdate
from db.session import get_db

from db.repository.company import create_our_company, get_company_info, get_all_users, get_all_positions, get_all_departments, update_info, delete_company, get_companies_info
from db.repository.user import isAdmin, valid_token


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/auth")


@router.post("/create")
def create_company(companyInfo: CompanyCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token, db)
    data = create_our_company(cInfo=companyInfo, db=db)
    return data


@router.get("/getInfo/{company_id}")
def get_company_info_by_id(company_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token, db)
    data = get_company_info(c_id=company_id, db=db)
    return data


@router.get("/getAllCopmpanies")
def get_all_companies(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = get_companies_info(db=db)
    return data


@router.get("/getUsers/{company_id}")
def get_all_users_in_company(company_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token, db)
    data = get_all_users(c_id=company_id, db=db)
    return data


@router.get("/getPositions/{company_id}")
def get_all_positions_in_company(company_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token, db)
    data = get_all_positions(c_id=company_id, db=db)
    return data


@router.get("/getDepartments/{company_id}")
def get_all_departments_in_company(company_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token, db)
    data = get_all_departments(c_id=company_id, db=db)
    return data


@router.put("/update/{company_id}")
def update_company_by_id(company_id: int, company: CompanyUpdate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = update_info(c_id=company_id, newInfo=company, db=db)
    return data


@router.delete("/delete/{company_id}", description="ПРЕДУПРЕЖДЕНИЕ: Удаление компании повлечет за собой удаление отделов и должностей.")
def delete_company_by_id(company_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = delete_company(c_id=company_id, db=db)
    return data