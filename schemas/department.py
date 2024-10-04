from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    name: str
    company_id: int


class DepartmentUpdate(BaseModel):
    name: str
    company_id: int


