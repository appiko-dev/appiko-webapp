from flask import render_template, url_for, flash, redirect
from appiko_webapp import app, db, bcrypt
from appiko_webapp.forms import RegistrationForm, LoginForm
from appiko_webapp.models import User
from flask_login import login_user, current_user, logout_user, login_required


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


@app.route("/learn")
def learn():
    return render_template("learn.html", title="learn")


@app.route("/account")
@login_required
def account():
    return render_template("account.html", title="account")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))

    return render_template("register.html", title="register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash(
                "Login Failed, please check the email and password then try again.", "danger")
            return redirect(url_for("home"))

    return render_template("login.html", title="login", form=form)
