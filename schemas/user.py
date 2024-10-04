from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    firstname: str
    lastname: str
    middlename: str

    company_id: None | int = None
    department_id: None | int = None
    position_id: None | int = None

    email: EmailStr
    password: str = Field(..., min_length=4)

    office_phone: str
    phone: str

    is_admin: bool = False

    status: str


class UserSelfUpdate(BaseModel):
    firstname: str
    lastname: str
    middlename: str

    phone: str


class UserAdminUpdate(UserSelfUpdate):
    company_id: int
    department_id: int
    position_id: int

    email: EmailStr

    office_phone: str

    is_admin: bool = False

    status: str


class UserChangePassword(BaseModel):
    password: str


