from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError
from wtforms.validators import Required

class SignupForm(Form):
  username = TextField("GitViz username", [validators.Required('Please enter your GitViz username')])
  password = TextField("GitViz password", [validators.Required('Please enter your GitViz password')])
  password_confirmation = TextField("Password Confirmation", [validators.Required('Enter your password confirmation')])
  submit = SubmitField("Submit")