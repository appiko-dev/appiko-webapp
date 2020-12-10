from flask import Flask, render_template, url_for
import secrets

app = Flask(__name__, static_url_path="/static")

app.config["SECRET KEY"] = secrets.token_hex(16)


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


if __name__ == "__main__":
    app.run(debug=True)
