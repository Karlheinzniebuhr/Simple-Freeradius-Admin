from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.widgets import PasswordInput
from SimpleAdmin import db
from SimpleAdmin.dbmanager import Radcheck, Radgroupreply, Radusergroup, internet_profile_query

class Client(object):
    def __init__(self, username, password, profile):
        self.username = username
        self.password = password
        self.profile  = profile

class Unique(object):
    def __init__(self, model, field, message='This element already exists.'):
        self.model = model
        self.field = field
        if not message:
            message = u'Field must be between %i and %i characters long.' % (min, max)
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)

class AddClientForm(FlaskForm):
    username = StringField('Username',
        validators=[DataRequired(),Length(min=2, max=20),
        Unique(
            Radusergroup,
            Radusergroup.username,
            message='There is already an user with that name!')])

    # We use a widget here to enable population of the pwd field
    password = StringField('Password', widget=PasswordInput(hide_value=False),
        validators=[DataRequired(),Length(min=2, max=20)])

    profile = SelectField(u'Internet Profile', choices=internet_profile_query())

    # delete = SubmitField('Delete User')

    submit = SubmitField('Save')

class EditClientForm(FlaskForm):
    username = StringField('Username',
        validators=[DataRequired(),Length(min=2, max=20)])

    # We use a widget here to enable population of the pwd field
    password = StringField('Password', widget=PasswordInput(hide_value=False),
        validators=[DataRequired(),Length(min=2, max=20)])

    profile = SelectField(u'Internet Profile', choices=internet_profile_query())

    delete = SubmitField('Delete User')

    submit = SubmitField('Save')

class LoginForm(FlaskForm):
    username = StringField('Username',
        validators=[DataRequired(),Length(min=2)])

    # We use a widget here to enable population of the pwd field
    password = StringField('Password',
        validators=[DataRequired(),Length(min=4)])

    submit = SubmitField('Login')
