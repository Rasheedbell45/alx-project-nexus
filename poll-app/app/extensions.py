from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_caching import Cache

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
api = Api(
    title="Polling API",
    version="1.0",
    description="APIs for polls, voting, and results",
    doc="/api/docs"  # Swagger UI served here
)
cache = Cache()
