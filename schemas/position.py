from pydantic import BaseModel


class PositionCreate(BaseModel):
    name: str
    company_id: int
    department_id: int


class PositionUpdate(BaseModel):
    name: str
    company_id: int
    department_id: int


