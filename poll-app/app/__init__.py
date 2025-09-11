from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, api, cache
from .resources.auth import auth_ns
from .resources.polls import polls_ns
from .resources.votes import votes_ns
from .resources.results import results_ns

def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cache.init_app(app)

    # RESTX API / Swagger
    api.init_app(app)
    # register namespaces
    api.add_namespace(auth_ns, path="/api/auth")
    api.add_namespace(polls_ns, path="/api/polls")
    api.add_namespace(votes_ns, path="/api/votes")
    api.add_namespace(results_ns, path="/api/results")

    # Swagger UI is auto-shown at /api/docs/ - see config below
    return app
