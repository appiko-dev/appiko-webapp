from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
from flask import current_app
from appiko_webapp import db, login_manager
from flask_login import UserMixin
# usermixin deals with authentication login manager expects


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), unique=False,
                           nullable=False, default="default.jpg")
    password = db.Column(db.String(60), unique=False, nullable=False)
    account_value = db.Column(db.Float, unique=False, nullable=False)
    profile_visits = db.Column(db.Integer, unique=False, nullable=False)
    events = db.relationship("AccountEvents", backref="account", lazy=True)
    posts = db.relationship("Post", backref="account", lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = serializer(current_app.secret_key, expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = serializer(current_app.secret_key)
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None

        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.account_value}')"


class AccountEvents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(24), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"AccountEvents('{self.event}', {self.date}, '{self.user_id}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
