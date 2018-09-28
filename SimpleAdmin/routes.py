from flask import render_template, flash, redirect, url_for, request, jsonify, make_response
from SimpleAdmin.addclient import handle_add_reply
from SimpleAdmin.editclient import handle_edit_reply
from SimpleAdmin.deleteclient import handle_delete_client
from SimpleAdmin import app, db, login_manager
from SimpleAdmin.dbmanager import Radcheck, Radgroupreply, Radusergroup, User
from SimpleAdmin.models import Client, AddClientForm, EditClientForm, LoginForm
from SimpleAdmin.list import list_clients
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from SimpleAdmin import api
import datetime
import jwt
from functools import wraps
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@login_required
def home():
    return render_template('home.html')

@app.route("/about")
@login_required
def about():
    return render_template('about.html')

@app.route("/add_client", methods=['GET', 'POST'])
@login_required
def add_client():
    
    form = AddClientForm()
    if form.validate_on_submit():
        handle_add_reply(form)

        return redirect(url_for('list'))
    else:
        for input, err in form.errors.items():
            flash("%s: %s" %(input,err[0]), 'warning')
    return render_template('add_client.html', form=form)

@app.route("/edit_client", methods=['GET', 'POST'])
@login_required
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
@login_required
def list():
    
    table = list_clients()

    return render_template('list.html', table=table)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return render_template('home.html')

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(name=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
                    login_user(user, remember=False)
                    next_page = request.args.get('next')
                    return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login Unsuccessful. Please check username and password", 'warning')
    else:
        for input, err in form.errors.items():
            print(input, err)
            flash("%s: %s" %(input,str(err)), 'warning')
    return render_template('login.html', form=form)

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    form = LoginForm()
    return render_template('login.html', form=form)

# API
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_api_client = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_api_client, *args, **kwargs)

    return decorated


@app.route("/api/auth", methods=['GET', 'POST'])
def api_auth():
    auth = request.authorization
    try:
        if not auth or not auth.username or not auth.password:
            return make_response('Could not verify', 401, {'WWW-Authenticate':'Basic realm="Login required!"'})

        user = db.session.query(User).filter_by(name=auth.username).first()

        if not user:
            return make_response('Could not verify', 401, {'WWW-Authenticate':'Basic realm="Login required!"'})

        if check_password_hash(user.password, auth.password):
                token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

                return jsonify({'token' : token.decode('UTF-8')})

        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    except Exception as e:
        err_message = "Api encountered an error: " + str(e)
        print(err_message)
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


@app.route("/api/add_api_client", methods=['POST'])
@token_required
def add_api_client(current_user):
    # if not current_user.admin:
    #     return jsonify({'message' : 'Cannot perform that function!'})

    data = request.get_json()
    status, error = api.add_api_client(data)

    if status:
        return jsonify({'message' : 'New user created!'})
    return jsonify({'status': status, 'message' : error})


@app.route("/api/add_client", methods=['POST'])
@token_required
def api_add_client(current_user):
    data = request.get_json()
    status, error = api.add_client(data)
    return jsonify({'status': status, 'message': error})


@app.route("/api/get_client", methods=['POST'])
@token_required
def api_get_client(current_user):
    data = request.get_json()
    status, username, prof, err = api.get_client(data)
    if status:
        return jsonify({'status': status, 'username': username, 'profile': prof})
    return jsonify({'status': status, 'error': err})


@app.route("/api/edit_client", methods=['POST'])
@token_required
def api_edit_client(current_user):
    data = request.get_json()
    status, error = api.edit_client(data)
    return jsonify({'status': status, 'message': error})


@app.route("/api/delete_client", methods=['POST'])
@token_required
def api_delete_client(current_user):
    data = request.get_json()
    status = api.delete_client(data)
    return jsonify({"status": status})


@app.route("/api/block_client", methods=['POST'])
@token_required
def api_block_client(current_user):

    return ''


@app.route("/api/activate_client", methods=['POST'])
@token_required
def api_activate_client(current_user):

    return ''


@app.route("/api/list_profiles", methods=['GET'])
@token_required
def api_list_profiles(current_user):
    status, profiles = api.list_profiles()
    return jsonify({"status": status, "profiles": profiles})