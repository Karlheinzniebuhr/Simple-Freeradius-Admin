from flask import render_template, flash, redirect, url_for, request
from SimpleAdmin.addclient import handle_add_reply
from SimpleAdmin.editclient import handle_edit_reply
from SimpleAdmin.deleteclient import handle_delete_client
from SimpleAdmin import app, db
from SimpleAdmin.dbmanager import Radcheck, Radgroupreply, Radusergroup
from SimpleAdmin.models import Client, AddClientForm, EditClientForm
from SimpleAdmin.list import list_clients

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/add_client", methods=['GET', 'POST']) 
def add_client():
    
    form = AddClientForm()
    if form.validate_on_submit():
        handle_add_reply(form)

        return redirect(url_for('list'))
    else:
        for input, err in form.errors.items():
            flash("%s: %s" %(input,err[0]), 'warning')
    return render_template('add_client.html', form=form)

# @app.route("/delete_client", methods=['GET', 'POST']) 
# def delete_client():
    
#     if form.validate_on_submit():
        

#         return redirect(url_for('home'))
#     else:
        
#     return render_template('add_client.html', form=form)

@app.route("/edit_client", methods=['GET', 'POST'])
def edit_client():
    
    if request.method == 'GET':
        user_param = request.args.get('user')
        radcheck_radusergroup_list = db.session.query(Radcheck, Radusergroup).filter(Radcheck.username==user_param).filter(Radcheck.username == Radusergroup.username).first()
        radcheck = radcheck_radusergroup_list[0]
        radusergroup = radcheck_radusergroup_list[1]
        client = Client(username=radcheck.username, password=radcheck.value, profile=radusergroup.groupname)

        form = EditClientForm(obj=client)

        return render_template('edit_client.html', form=form)
    else:

        user_param = request.args.get('user')
        form = EditClientForm()
        if form.validate_on_submit():

            if(form.delete.data):
                handle_delete_client(form)
                return redirect(url_for('list'))
                
            else:
                handle_edit_reply(form, user_param)

                return redirect(url_for('list'))
        else:
            for input, err in form.errors.items():
                flash("%s: %s" %(input,err[0]), 'warning')
        return render_template('edit_client.html', form=form)

@app.route("/list", methods=['GET', 'POST'])
def list():
    
    table = list_clients()

    return render_template('list.html', table=table)