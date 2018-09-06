from flask import flash
from SimpleAdmin import db
from SimpleAdmin.dbmanager import Radcheck, Radgroupreply, Radusergroup

def handle_delete_client(form):
    
    username = form.username.data

    radchk_res = db.session.query(Radcheck).filter(Radcheck.username == username).delete()
    radusrgr_res = db.session.query(Radusergroup).filter(Radusergroup.username == username).delete()

    db.session.commit()

    flash("User %s deleted!" %(username), 'warning')