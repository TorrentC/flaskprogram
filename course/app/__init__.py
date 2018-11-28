from flask import Flask
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


moment = Moment()
bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()


login_manager.login_view = 'main.login'
login_manager.session_protection = 'strong'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    moment.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main
    from .admin import admin
    app.register_blueprint(main)
    app.register_blueprint(admin)

    return app