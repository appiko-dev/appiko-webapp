from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from appiko_webapp.config import Config

mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

login_manager.login_view = "users.login"  # where to redirect
login_manager.login_message_category = "info"


def create_app(config_class=Config):

    app = Flask(__name__, static_url_path="/static")
    app.config.from_object(Config)

    mail.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from appiko_webapp.users.routes import users
    from appiko_webapp.posts.routes import posts
    from appiko_webapp.main.routes import main
    from appiko_webapp.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
