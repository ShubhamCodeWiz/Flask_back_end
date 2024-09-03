from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = '7789e8a23b5ab923c1c2808a'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"

from market import api_routes  # Add this line