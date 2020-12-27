from flask import render_template, request, Blueprint
from appiko_webapp.models import Post, User


main = Blueprint("main", __name__)


@main.route("/")
def home():
    applicationdata = [f'{sum([_.account_value for _ in User.query.all()]):.2f}', sum(
        [_.profile_visits for _ in User.query.all()])]
    return render_template("home.html", title="home", applicationdata=applicationdata)


@main.route("/explore", methods=["GET"])
def explore():
    users = User.query.all()
    articles = Post.query.all()
    return render_template("explore.html", title="explore", articles=articles, users=users)
