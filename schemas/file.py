from pydantic import BaseModel


class FileCreate(BaseModel):
    name: str
    url: str | None = None
    code: str | None = None
    allowed_all: bool = False
    section_id: int | str | None = None


class FileUpdate(BaseModel):
    name: str
    url: str | None = None
    code: str | None = None
    allowed_all: bool = False
    section_id: int | str | None = None


class PermissionChange(BaseModel):
    target_id: int
    file_id: int

