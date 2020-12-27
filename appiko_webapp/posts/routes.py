from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from appiko_webapp import db
from appiko_webapp.models import Post
from appiko_webapp.posts.forms import ArticleForm

posts = Blueprint("posts", __name__)


@posts.route("/article/new", methods=["GET", "POST"])
@login_required
def new_article():
    form = ArticleForm()
    if form.validate_on_submit():
        article = Post(title=form.title.data,
                       content=form.content.data, account=current_user)
        db.session.add(article)
        db.session.commit()
        flash("Article published!", "success")
        return redirect(url_for("users.account"))
    return render_template("create_article.html", title="new article", form=form, legend="Create Article")


@posts.route("/article/<int:article_id>/update", methods=["GET", "POST"])
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
        return redirect(url_for("users.account"))
        # return redirect(url_for("article", article_id=article.id))
    elif request.method == "GET":
        form.title.data = article.title
        form.content.data = article.content
    return render_template("create_article.html", title="update article", form=form, legend="Update Article")


@posts.route("/article/<int:article_id>/delete", methods=["GET", "POST"])
@login_required
def delete_article(article_id):
    article = Post.query.get_or_404(article_id)
    if article.account != current_user:
        abort(403)
    db.session.delete(article)
    db.session.commit()
    flash("Your article has been deleted", "success")
    return redirect(url_for("users.account"))
