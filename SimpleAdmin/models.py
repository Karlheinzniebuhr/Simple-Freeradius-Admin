from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.widgets import PasswordInput
from SimpleAdmin import db
from SimpleAdmin.dbmanager import Radcheck, Radgroupreply, Radusergroup, internet_profile_choice_query

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

    profile = SelectField(u'Internet Profile', choices=internet_profile_choice_query())

    submit = SubmitField('Save')

# class Client(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=True)
#     phone = db.Column(db.String(20), unique=True, nullable=True)
#     password = db.Column(db.String(20), nullable=False)

#     def __repr__(self):
#         return f"User('{self.username}','{self.email}', '{self.phone}', '{self.password}')"