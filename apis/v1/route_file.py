from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from pathlib import Path
import shutil
from datetime import datetime

from core.config import settings

from schemas.file import FileCreate, FileUpdate, PermissionChange
from db.session import get_db

from db.repository.file import create_our_file, add_allowed_user_to_file, add_allowed_position_to_file, add_allowed_department_to_file, add_allowed_company_to_file, update_info_by_id, delete_file_by_id, get_file_info_by_id, remove_allowed_user_to_file, remove_allowed_position_to_file, remove_allowed_department_to_file, remove_allowed_company_to_file, get_files_by_section_id
from db.repository.user import isAdmin, valid_token


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/auth")


UPLOAD_DIR = settings.UPLOAD_DIR_FILES_IMAGES
UPLOAD_DIR.mkdir(exist_ok=True)


@router.get("/getInfo/{file_id}")
def get_file_by_id(file_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    data = get_file_info_by_id(f_id=file_id, db=db)
    return data


@router.post("/create")
def create_file(fileInfo: FileCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = create_our_file(fInfo=fileInfo, db=db)
    return data


@router.get("/getFilesBySectionID")
def get_files(section_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = get_files_by_section_id(s_id=section_id, db=db)
    return data


@router.post("/addAllowedUser")
def add_allowed_user(permissions_ids: PermissionChange, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = add_allowed_user_to_file(f_id=permissions_ids.file_id, u_id=permissions_ids.target_id, db=db)
    return data


@router.delete("/removeAllowedUser")
def remove_allowed_user(permissions_ids: PermissionChange, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = remove_allowed_user_to_file(f_id=permissions_ids.file_id, u_id=permissions_ids.target_id, db=db)
    return data


@router.post("/addAllowedPosition")
def add_allowed_position(permissions_ids: PermissionChange, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = add_allowed_position_to_file(f_id=permissions_ids.file_id, p_id=permissions_ids.target_id, db=db)
    return data


@router.delete("/removeAllowedPosition")
def remove_allowed_position(permissions_ids: PermissionChange, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = remove_allowed_position_to_file(f_id=permissions_ids.file_id, p_id=permissions_ids.target_id, db=db)
    return data


@router.post("/addAllowedDepartment")
def add_allowed_department(permissions_ids: PermissionChange, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = add_allowed_department_to_file(f_id=permissions_ids.file_id, d_id=permissions_ids.target_id, db=db)
    return data


@router.delete("/removeAllowedDepartment")
def remove_allowed_department(permissions_ids: PermissionChange, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = remove_allowed_department_to_file(f_id=permissions_ids.file_id, d_id=permissions_ids.target_id, db=db)
    return data


@router.post("/addAllowedCompany")
def add_allowed_company(permissions_ids: PermissionChange, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = add_allowed_company_to_file(f_id=permissions_ids.file_id, c_id=permissions_ids.target_id, db=db)
    return data


@router.delete("/removeAllowedCompany")
def remove_allowed_company(permissions_ids: PermissionChange, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = remove_allowed_company_to_file(f_id=permissions_ids.file_id, c_id=permissions_ids.target_id, db=db)
    return data


@router.put("/update/{file_id}")
def update_file_by_id(file_id: int, file: FileUpdate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = update_info_by_id(f_id=file_id, newInfo=file, db=db)
    return data


@router.delete("/delete/{file_id}")
def delete_file(file_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = delete_file_by_id(f_id=file_id, db=db)
    return data


@router.post("/upload/")
def upload_image(file: UploadFile = File(...), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    settings.logger.debug(f"{__name__} - admin validation")
    save_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + "_" + file.filename
    file_location = UPLOAD_DIR / save_name
    settings.logger.debug(f"{__name__} - upload image {file.filename} to {file_location}")
    try:
        with file_location.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        settings.logger.debug(f"{__name__} - upload image {save_name} to {file_location} is success")
        return {"url": f"http://{settings.SERVER_IP}:{settings.PORT}/static/{save_name}"}
    except Exception as ex:
        settings.logger.debug(f"{__name__} - upload image {save_name} to {file_location} completed with error {ex}")
        raise HTTPException(status_code=500, detail="Error uploading image")
