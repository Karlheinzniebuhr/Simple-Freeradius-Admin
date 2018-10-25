from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from SimpleAdmin import keys
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = keys.APP_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' +keys.DB_USERNAME_PASSWORD+ '@127.0.0.1:3306/radius'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from SimpleAdmin import dbmanager
from SimpleAdmin import routes