from flask import Flask
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from config import Config
from flask_sqlalchemy import SQLAlchemy


moment = Moment()
bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    moment.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)

    from .main import main
    from .admin import admin
    app.register_blueprint(main)
    app.register_blueprint(admin)

    return app