from flask import flash
from SimpleAdmin import db
from SimpleAdmin.dbmanager import Radcheck, Radgroupreply, Radusergroup

def handle_edit_reply(form):
    
    username = form.username.data
    pwd = form.password.data
    prof = form.profile.data

    # Freeradius uses 2 tables. One table to validate the user/password and another one to respond with a user profile
    radchk = Radcheck(username=username, attribute='Cleartext-Password', op=':=', value=pwd)
    radusrgr = Radusergroup(username=username, groupname=prof)

    db.session.add(radchk)
    db.session.add(radusrgr)
    db.session.commit()

    flash(f'User { form.username.data } created!', 'success')
    print("%s:%s:%s" % (username, pwd, prof))