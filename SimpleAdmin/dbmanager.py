from flask_admin.contrib.sqla import ModelView
from sqlalchemy import MetaData, Table, Column
from sqlalchemy.ext.automap import automap_base
from flask_admin import Admin

from SimpleAdmin import db, app

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

def internet_profile_choice_query():
    choices_arr = []
    choices_db = db.session.query(Radgroupreply).all()
    for c in choices_db:
        choices_arr.append((c.groupname, c.value))

    return choices_arr