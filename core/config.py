import os
from pathlib import Path

from dotenv import load_dotenv

from datetime import timedelta, datetime
import logging
import socket

env_path = Path('') / '.env'
load_dotenv(dotenv_path=env_path)

log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"{log_directory}/ttbook_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"),
        logging.StreamHandler()
    ]
)


class Settings:
    PROJECT_NAME: str = "ttBook"
    PROJECT_VERSION: str = "1.0.0"

    SERVER_IP = socket.gethostbyname(socket.gethostname())
    PORT = "8000"

    logger = logging.getLogger("ttBook")

    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)  # default postgres port is 5432
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "ttBook")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
    JWT_EXPIRATION_TIME = timedelta(minutes=480)

    UPLOAD_DIR_FILES_IMAGES = Path("img")


settings = Settings()
