from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
import secrets

app = Flask(__name__, static_url_path="/static")

app.config["SECRET_KEY"] = "491b8c0c72d4fdac6a8a2f3509dc414b"


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


@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", title="login", form=form)


if __name__ == "__main__":
    app.run(debug=True)
