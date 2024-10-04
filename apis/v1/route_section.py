from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import Depends

from schemas.section import SectionCreate, SectionUpdate, PermissionChange, AddDeleteFile
from db.session import get_db

from db.repository.section import create_our_section, add_allowed_user_to_section, add_allowed_company_to_section, add_allowed_department_to_section, add_allowed_position_to_section, update_info_by_id, delete_section_by_id, get_section_info_by_id, remove_allowed_position_to_section, remove_allowed_user_to_section, remove_allowed_department_to_section, remove_allowed_company_to_section, get_all_sections_info, add_file_to_section, remove_file_in_section
from db.repository.user import isAdmin, valid_token


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/auth")


@router.get("/getInfo/{section_id}")
def get_section_by_id(section_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    isAdmin(token=token, db=db)
    data = get_section_info_by_id(s_id=section_id, db=db)
    return data


@router.post("/create")
def create_section(sectionInfo: SectionCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token, db)
    data = create_our_section(secInfo=sectionInfo, db=db)
    return data


@router.get("/getAllSections")
def get_all_sections(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    isAdmin(token=token, db=db)
    data = get_all_sections_info(db=db)
    return data


@router.post("/addAllowedUser")
def add_allowed_user(permissions_ids: PermissionChange, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token, db)
    data = add_allowed_user_to_section(s_id=permissions_ids.section_id, u_id=permissions_ids.target_id, db=db)
    return data


@router.delete("/removeAllowedUser")
def remove_allowed_user(permissions_ids: PermissionChange, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token, db)
    data = remove_allowed_user_to_section(s_id=permissions_ids.section_id, u_id=permissions_ids.target_id, db=db)
    return data


@router.post("/addAllowedPosition")
def add_allowed_position(permissions_ids: PermissionChange, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token, db)
    data = add_allowed_position_to_section(s_id=permissions_ids.section_id, p_id=permissions_ids.target_id, db=db)
    return data


@router.delete("/removeAllowedPosition")
def remove_allowed_position(permissions_ids: PermissionChange, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token, db)
    data = remove_allowed_position_to_section(s_id=permissions_ids.section_id, p_id=permissions_ids.target_id, db=db)
    return data


@router.post("/addAllowedDepartment")
def add_allowed_department(permissions_ids: PermissionChange, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token, db)
    data = add_allowed_department_to_section(s_id=permissions_ids.section_id, d_id=permissions_ids.target_id, db=db)
    return data


@router.delete("/removeAllowedDepartment")
def remove_allowed_department(permissions_ids: PermissionChange, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token, db)
    data = remove_allowed_department_to_section(s_id=permissions_ids.section_id, d_id=permissions_ids.target_id, db=db)
    return data


@router.post("/addAllowedCompany")
def add_allowed_company(permissions_ids: PermissionChange, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token, db)
    data = add_allowed_company_to_section(s_id=permissions_ids.section_id, c_id=permissions_ids.target_id, db=db)
    return data


@router.delete("/removeAllowedCompany")
def remove_allowed_company(permissions_ids: PermissionChange, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token, db)
    data = remove_allowed_company_to_section(s_id=permissions_ids.section_id, c_id=permissions_ids.target_id, db=db)
    return data


@router.post("/addFile")
def add_file(sect_file_ids: AddDeleteFile, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = add_file_to_section(s_id=sect_file_ids.section_id, f_id=sect_file_ids.file_id, db=db)
    return data


@router.delete("/removeFile")
def remove_file(sect_file_ids: AddDeleteFile, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = remove_file_in_section(s_id=sect_file_ids.section_id, f_id=sect_file_ids.file_id, db=db)
    return data


@router.put("/update/{section_id}")
def update_file_by_id(section_id: int, section: SectionUpdate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = update_info_by_id(s_id=section_id, newInfo=section, db=db)
    return data


@router.delete("/delete/{section_id}")
def delete_section(section_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = delete_section_by_id(s_id=section_id, db=db)
    return data