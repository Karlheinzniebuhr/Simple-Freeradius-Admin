from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from SimpleAdmin import keys

app = Flask(__name__)
app.config['SECRET_KEY'] = keys.APP_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' +keys.DB_USERNAME_PASSWORD+ '@localhost:3306/radius'
db = SQLAlchemy(app)

# don't use this in production
app.run(host= '0.0.0.0')

from SimpleAdmin import dbmanager
from SimpleAdmin import routes