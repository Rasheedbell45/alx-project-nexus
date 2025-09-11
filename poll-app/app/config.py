import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://postgres:changeme@localhost:5432/polls_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)

    # Flask-RESTX / Swagger
    RESTX_MASK_SWAGGER = False
    API_TITLE = "Polling API"
    API_VERSION = "1.0"
    API_DESCRIPTION = "API for creating polls, voting, and retrieving results"
    SWAGGER_UI_DOC_EXPANSION = 'list'
    ERROR_404_HELP = False

    # Caching (Redis)
    CACHE_TYPE = "redis"
    CACHE_REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
