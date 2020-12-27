from flask import render_template, url_for, flash, redirect, request
from appiko_webapp import app, db, bcrypt, mail
from appiko_webapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, ArticleForm, RequestResetForm, ResetPasswordForm
from appiko_webapp.models import User, AccountEvents, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/")
def home():
    applicationdata = [f'{sum([_.account_value for _ in User.query.all()]):.2f}', sum(
        [_.profile_visits for _ in User.query.all()])]
    return render_template("home.html", title="home", applicationdata=applicationdata)


@app.route("/explore", methods=["GET"])
def explore():
    users = User.query.all()
    articles = Post.query.all()
    return render_template("explore.html", title="explore", articles=articles, users=users)


@app.route("/article/new", methods=["GET", "POST"])
@login_required
def new_article():
    form = ArticleForm()
    if form.validate_on_submit():
        article = Post(title=form.title.data,
                       content=form.content.data, account=current_user)
        db.session.add(article)
        db.session.commit()
        flash("Article published!", "success")
        return redirect(url_for("account"))
    return render_template("create_article.html", title="new article", form=form, legend="Create Article")


@app.route("/article/<int:article_id>/update", methods=["GET", "POST"])
@login_required
def update_article(article_id):
    article = Post.query.get_or_404(article_id)
    if article.account != current_user:
        abort(403)
    form = ArticleForm()
    if form.validate_on_submit():
        article.title = form.title.data
        article.content = form.content.data
        db.session.commit()
        flash("Your article has been updated!", "success")
        return redirect(url_for("account"))
        # return redirect(url_for("article", article_id=article.id))
    elif request.method == "GET":
        form.title.data = article.title
        form.content.data = article.content
    return render_template("create_article.html", title="update article", form=form, legend="Update Article")


@app.route("/article/<int:article_id>/delete", methods=["GET", "POST"])
@login_required
def delete_article(article_id):
    article = Post.query.get_or_404(article_id)
    if article.account != current_user:
        abort(403)
    db.session.delete(article)
    db.session.commit()
    flash("Your article has been deleted", "success")
    return redirect(url_for("account"))


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    events = AccountEvents.query.order_by(
        AccountEvents.date.desc()).filter_by(user_id=current_user.id)
    page = request.args.get("page", default=1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).filter_by(
        user_id=current_user.id).paginate(page=page, per_page=2)
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
    return render_template("account.html", title="account", form=form, events=events, posts=posts)
    # post get redirect pattern (are you sure you want to reload?)


@app.route("/article/<int:article_id>")
def article(article_id):
    article = Post.query.get_or_404(article_id)
    account = User.query.filter_by(username=article.account.username).first()
    if account != current_user:
        account.account_value += 0.001
        db.session.commit()
    return render_template("article.html", title=article.title, article=article)


@app.route("/public/<string:username>")
def public(username):
    account = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.order_by(
        Post.date_posted.desc()).filter_by(user_id=account.id)
    if account != current_user:
        account.account_value += 0.00025
        account.profile_visits += 1
        db.session.commit()
    return render_template("public.html", title=account.username, account=account, posts=posts)


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


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request",
                  sender="rstpswrd@gmail.com", recipients=[user.email])

    msg.body = f"""To reset your password, visit the following link:
{url_for("reset_token", token=token, _external=True)}

If you did not make this request, simply ignore this email.
    """

    mail.send(msg)


@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():

    if current_user.is_authenticated:
        redirect(url_for("home"))

    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions", "info")
        return redirect(url_for("home"))

    return render_template("reset_request.html", title="password reset", form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        redirect(url_for("home"))

    user = User.verify_reset_token(token)

    if user is None:
        flash("That token is invalid or expired", "warning")
        return redirect(url_for("reset_request"))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash(f"Your password has been reset", "success")
        return redirect(url_for("home"))

    return render_template("reset_token.html", title="reset password", form=form)
