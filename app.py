from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")


@app.route("/login")
def login():
    return render_template("index.html")

if __name__ == "__main__":
    app.secret_key = "secretkey"
    app.run(debug=True)
