from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
import secrets

app = Flask(__name__, static_url_path="/static")

app.config["SECRET_KEY"] = "491b8c0c72d4fdac6a8a2f3509dc414b"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # unique id for our user
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), unique=False,
                           nullable=False, default="default.jpg")
    password = db.Column(db.String(60), unique=False, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


@app.route("/")
def home():
    return render_template("home.html", title="home")


@app.route("/products")
def products():
    return render_template("products.html", title="products")


@app.route("/services")
def services():
    return render_template("services.html", title="services")


@app.route("/arcade")
def arcade():
    return render_template("arcade.html", title="arcade")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))

    return render_template("register.html", title="register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "P@$$w0rd":
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
            return redirect(url_for("home"))

    return render_template("login.html", title="login", form=form)


if __name__ == "__main__":
    app.run(debug=True)
