from flask import Flask, render_template, url_for
import secrets

app = Flask(__name__, static_url_path="/static")

app.config["SECRET KEY"] = secrets.token_hex(16)


@app.route("/")
def home():
    return render_template("home.html", title="home", posts=posts)


if __name__ == "__main__":
    app.run(debug=True)
