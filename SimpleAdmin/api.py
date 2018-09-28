from flask import flash, jsonify
from SimpleAdmin import db
from SimpleAdmin.dbmanager import Radcheck, Radgroupreply, Radusergroup, api_internet_profile_query, User
import jwt
import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash


def add_api_client(data):
    
    try:
        name = data['name']
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(public_id=str(uuid.uuid4()), name=name, password=hashed_password, admin=False)
        db.session.add(new_user)
        db.session.commit()

        print("Api added:%s:%s" % (name, hashed_password))
        return True, ""
    except Exception as e:
        err_message = "Api encountered an error: " + str(e)
        print(err_message)
        return False, str(err_message)


def add_client(json):

    try:
        username = json['username']
        pwd = json['password']
        prof = json['profile']

        radchk = Radcheck(username=username, attribute='Cleartext-Password', op=':=', value=pwd)
        radusrgr = Radusergroup(username=username, groupname=prof)

        db.session.add(radchk)
        db.session.add(radusrgr)
        db.session.commit()

        print("Api added: %s:%s:%s" % (username, pwd, prof))
        return True, ""
    except Exception as e:
        err_message = "Api encountered an error: " + str(e)
        print(err_message)
        return False, str(err_message)


def get_client(json):
    
    try:
        username = json['username']

        radusrgr = db.session.query(Radusergroup).filter(Radusergroup.username == username).first()

        prof = radusrgr.groupname

        print("Api added: %s:%s" % (username, prof))
        return True, username, prof, ""
    except Exception as e:
        err_message = "Api encountered an error: " + str(e)
        print(err_message)
        return False, "","",str(err_message)


def edit_client(json):
    
    try:
        former_name = json['former_name']
        username = json['username']
        pwd = json['password']
        prof = json['profile']

        radchk = db.session.query(Radcheck).filter(Radcheck.username == former_name).first()
        radusrgr = db.session.query(Radusergroup).filter(Radusergroup.username == former_name).first()

        radchk.username = username
        radchk.pwd = pwd
        radchk.prof = prof

        radusrgr.username = username
        radusrgr.groupname = prof

        db.session.commit()

        print("Api added: %s:%s:%s" % (username, pwd, prof))
        return True, ""
    except Exception as e:
        err_message = "Api encountered an error: " + str(e)
        print(err_message)
        return False, str(err_message)


def delete_client(json):

    try:
        username = json['username']

        db.session.query(Radcheck).filter(Radcheck.username == username).delete()
        db.session.query(Radusergroup).filter(Radusergroup.username == username).delete()

        db.session.commit()
        return True, ""

    except Exception as e:
        err_message = "Api encountered an error: " + str(e)
        print(err_message)
        return False, str(err_message)


def list_profiles():
    
    try:
        profiles = api_internet_profile_query()

        print("Api selected all profiles")
        return True, profiles

    except Exception as e:
        err_message = "Api encountered an error: " + str(e)
        print(err_message)
        return False, str(err_message)