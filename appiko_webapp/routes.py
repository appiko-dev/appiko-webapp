from flask import render_template, url_for, flash, redirect, request
from appiko_webapp import app, db, bcrypt
from appiko_webapp.forms import RegistrationForm, LoginForm, UpdateAccountForm
from appiko_webapp.models import User, AccountEvents
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


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    events = AccountEvents.query.filter_by(user_id=current_user.id)
    form = UpdateAccountForm()
    if form.validate_on_submit():
        old_name = current_user.username
        current_user.username = form.username.data
        # add name change for event tied to users account
        event = AccountEvents(
            event=f"Changed {old_name} to {form.username.data}", account=current_user)
        db.session.add(event)
        db.session.commit()
        flash("Your account has been updated.", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
    return render_template("account.html", title="account", form=form, events=events)
    # post get redirect pattern (are you sure you want to reload?)


@app.route("/public/<int:account_id>")
def public(account_id):
    account = User.query.get_or_404(account_id)
    account.profile_visits += 1
    account.account_value += 0.001
    db.session.commit()
    return render_template("public.html", title=account.username, account=account)


@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "info")
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
                    email=form.email.data, password=hashed_password, account_value=0.00, profile_visits=0)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}", "success")
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
            next_page = request.args.get("next")
            flash("You have been logged in.", "success")
            event = AccountEvents(
                event=f"Login from ip {request.remote_addr}", account=current_user)
            db.session.add(event)
            db.session.commit()
            return redirect(next_page) if next_page else redirect(url_for("account"))
        else:
            flash(
                "Please check the email and password then try again.", "danger")

            if User.query.filter_by(email=form.email.data).first():
                event = AccountEvents(
                    event=f"Login attempt from {request.remote_addr}", account=User.query.filter_by(email=form.email.data).first())
                db.session.add(event)
                db.session.commit()

            return redirect(url_for("home"))

    return render_template("login.html", title="login", form=form)
