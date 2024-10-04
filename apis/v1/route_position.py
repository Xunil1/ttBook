from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import Depends

from schemas.position import PositionCreate, PositionUpdate
from db.session import get_db

from db.repository.position import create_our_position, get_position_info, get_all_users, update_info, delete_position, get_positions_info
from db.repository.user import isAdmin, valid_token


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/auth")


@router.post("/create")
def create_position(positionInfo: PositionCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token, db)
    data = create_our_position(pInfo=positionInfo, db=db)
    return data


@router.get("/getInfo/{position_id}")
def get_position_info_by_id(position_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token, db)
    data = get_position_info(p_id=position_id, db=db)
    return data


@router.get("/getAllPositions")
def get_all_position(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = get_positions_info(db=db)
    return data


@router.get("/getUsers/{position_id}")
def get_all_users_in_position(position_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token, db)
    data = get_all_users(p_id=position_id, db=db)
    return data


@router.put("/update/{position_id}")
def update_position_by_id(position_id: int, position: PositionUpdate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = update_info(p_id=position_id, newInfo=position, db=db)
    return data


@router.delete("/delete/{position_id}")
def delete_position_by_id(position_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    valid_token(token=token, db=db)
    isAdmin(token=token, db=db)
    data = delete_position(p_id=position_id, db=db)
    return data