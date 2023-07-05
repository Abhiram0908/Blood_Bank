from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "25acc13e620e037d213b91ba0404b30f"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"  # setting location
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

from app import routes
