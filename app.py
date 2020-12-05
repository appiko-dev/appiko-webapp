from flask import Flask, render_template, url_for
import secrets

app = Flask(__name__, static_url_path="/static")

app.config["SECRET KEY"] = secrets.token_hex(16)


@app.route("/")
def home():
    return render_template("home.html", title="Home Page")


@app.route("/learn")
def learn():
    return render_template("learn.html", title="Learn Page")


@app.route("/services")
def services():
    return render_template("services.html", title="Services Page")


@app.route("/products")
def products():
    return render_template("products.html", title="Products Page")


@app.route("/arcade")
def arcade():
    return render_template("arcade.html", title="Arcade Page")


if __name__ == "__main__":
    app.run(debug=True)
