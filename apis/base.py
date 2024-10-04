from fastapi import APIRouter

from apis.v1 import route_user
from apis.v1 import route_company
from apis.v1 import route_department
from apis.v1 import route_position
from apis.v1 import route_section
from apis.v1 import route_file


api_router = APIRouter()
api_router.include_router(route_user.router, prefix="/user", tags=["User"])
api_router.include_router(route_company.router, prefix="/company", tags=["Company"])
api_router.include_router(route_department.router, prefix="/department", tags=["Department"])
api_router.include_router(route_position.router, prefix="/position", tags=["Position"])
api_router.include_router(route_section.router, prefix="/section", tags=["Section"])
api_router.include_router(route_file.router, prefix="/file", tags=["File"])