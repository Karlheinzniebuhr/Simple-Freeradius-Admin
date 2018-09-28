from flask_admin.contrib.sqla import ModelView
from sqlalchemy import MetaData, Table, Column
from sqlalchemy.ext.automap import automap_base
from flask_admin import Admin
from SimpleAdmin import db, app
from flask_login import UserMixin

admin = Admin(app)
# load existing db model
metadata = MetaData()
metadata.reflect(db.engine, only=['radcheck','radgroupreply'])

Base = automap_base(metadata=metadata)

class Radusergroup(db.Model):
    username = db.Column(db.String, primary_key = True)
    groupname = db.Column(db.String, primary_key = False)

    def __repr__(self):
        return "<Radusergroup (username='%s', groupname='%s')>" % (
            self.username, self.groupname)

class Radusergroupview(ModelView):
    column_list = ['username', 'groupname']

Base.prepare()

Radcheck = Base.classes.radcheck
Radgroupreply = Base.classes.radgroupreply

admin.add_view(ModelView(Radcheck, db.session))
admin.add_view(ModelView(Radgroupreply, db.session))
admin.add_view(Radusergroupview(Radusergroup, db.session))

def internet_profile_query():
    choices_arr = []
    choices_db = db.session.query(Radgroupreply).all()
    for c in choices_db:
        choices_arr.append((c.groupname, c.value))

    return choices_arr

def api_internet_profile_query():
    choices_arr = []
    choices_db = db.session.query(Radgroupreply).all()
    for c in choices_db:
        choices_arr.append(c.groupname)

    return choices_arr

# ************************ the tables below are not part of Freeradius ************************
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return f"User('{self.id}','{self.public_id}', '{self.name}', '{self.password}', '{self.admin}')"

