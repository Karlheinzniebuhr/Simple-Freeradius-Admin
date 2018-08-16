from flask import flash
from SimpleAdmin import db
from SimpleAdmin.dbmanager import Radcheck, Radgroupreply, Radusergroup

def handle_edit_reply(form, former_name):
    
    username = form.username.data
    pwd = form.password.data
    prof = form.profile.data

    # Freeradius uses 2 tables. One table to validate the user/password and another one to respond with a user profile
    radchk = db.session.query(Radcheck).filter(Radcheck.username == former_name).first()
    radusrgr = db.session.query(Radusergroup).filter(Radusergroup.username == former_name).first()

    radchk.username = username
    radchk.pwd = pwd
    radchk.prof = prof

    radusrgr.username = username
    radusrgr.groupname = prof

    db.session.commit()

    flash(f'User { form.username.data } created!', 'success')
    print("%s:%s:%s" % (username, pwd, prof))