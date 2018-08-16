from SimpleAdmin import db
from SimpleAdmin.dbmanager import Radcheck, Radgroupreply, Radusergroup
from flask_table import Table, Col, LinkCol
from SimpleAdmin.models import Client

def list_clients():
    
    class ClientTable(Table):
        username = Col('Username')
        password = Col('Password')
        profile = Col('Profile')
        edit = LinkCol('Edit', 'edit_client', url_kwargs=dict(user='username'))

    radcheck_radusergroup_list = db.session.query(Radcheck, Radusergroup).filter(Radcheck.username == Radusergroup.username).all() 
    
    items = []
    for item in radcheck_radusergroup_list:
        assert (item[0].username == item[1].username)
        usrname = item[0].username
        pwd = item[0].value
        prof = item[1].groupname
        client_obj = Client(username=usrname, password=pwd, profile=prof)
        items.append(client_obj)
        
    table = ClientTable(items, classes=['table is-striped is-fullwidth'])
    return table