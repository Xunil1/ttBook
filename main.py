from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from apis.base import api_router
from core.config import settings
from db.base import Base
from db.session import engine


origins = [
    "*"
]


def create_tables():
    Base.metadata.create_all(bind=engine)


def include_router(app):
    app.include_router(api_router)


def start_application():
    settings.logger.info("Starting application")
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()
    include_router(app)
    return app


app = start_application()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=settings.UPLOAD_DIR_FILES_IMAGES), name="static")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Логируем данные запроса
    settings.logger.info(f"Request: {request.method} {request.url}")
    settings.logger.info(f"Headers: {request.headers}")

    # Выполнение запроса
    response = await call_next(request)

    # Логируем данные ответа и время выполнения
    settings.logger.info(f"Response status: {response.status_code}")

    return response