from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import secrets

app = Flask(__name__, static_url_path="/static")

app.config["SECRET_KEY"] = "491b8c0c72d4fdac6a8a2f3509dc414b"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)

from appiko_webapp import routes

login_manager.login_view = "home"
login_manager.login_message_category = "info"
