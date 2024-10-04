from pydantic import BaseModel


class SectionCreate(BaseModel):
    name: str
    allowed_all: bool


class SectionUpdate(BaseModel):
    name: str
    allowed_all: bool


class PermissionChange(BaseModel):
    target_id: int
    section_id: int


class AddDeleteFile(BaseModel):
    section_id: int
    file_id: int