from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from SimpleAdmin import keys
from flask_login import LoginManager

from werkzeug.security import generate_password_hash
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = keys.APP_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' +keys.DB_USERNAME_PASSWORD+ '@mysql:3306/radius'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from SimpleAdmin import dbmanager
from SimpleAdmin import routes

# initialize the DB with a default admin
db.create_all()
name = 'flaskadmin'
hashed_password = generate_password_hash('flaskadmin', method='sha256')
new_user = dbmanager.User(public_id=str(uuid.uuid4()), name=name, password=hashed_password, admin=False)
db.session.add(new_user)
db.session.commit()