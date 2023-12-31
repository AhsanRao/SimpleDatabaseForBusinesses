import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module

db = SQLAlchemy()
login_manager = LoginManager()

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module(f'apps.{module_name}.routes')
        app.register_blueprint(module.blueprint)

def configure_database(app):
    @app.before_first_request
    def initialize_database():
        # Try to create all database tables
        try:
            db.create_all()
        except Exception as e:
            print(f'> Error: DBMS Exception: {e}')

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

from apps.authentication.oauth import github_blueprint

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    app.register_blueprint(github_blueprint, url_prefix="/login")
    configure_database(app)
    return app
