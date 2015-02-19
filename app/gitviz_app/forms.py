from flask.ext.wtf import Form
from wtforms import TextField, SubmitField, PasswordField, validators, ValidationError
from wtforms.validators import Required
from flask.ext.wtf.html5 import URLField
from user_model import User

class SignupForm(Form):
  username = TextField("GitViz username", [validators.Required('Please enter your GitViz username')])
  password = PasswordField("GitViz password", [
    validators.Required(),
    validators.EqualTo('confirm', message='Passwords must match')
  ])
  confirm = PasswordField('Repeat Password')
  submit = SubmitField("Submit")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(username = self.username.data.lower()).first()
    if user:
      self.username.errors.append("That username is already taken")
      return False
    return True

class LoginForm(Form):
  username = TextField('Username', [validators.Required()])
  password = PasswordField('Password', [validators.Required()])
  submit = SubmitField("Submit")

  def __init__(self, *args, **kwargs):
      Form.__init__(self, *args, **kwargs)

  def validate(self):
      if not Form.validate(self):
          return False

      user = User.query.filter_by(username=self.username.data).first()
      if not user or not user.check_password(self.password.data):
          self.username.errors.append('Unknown login info')
          return False
      self.user = user
      return True

class RequestVisualization(Form):
  repo_url = URLField(validators.Required('Enter URL'))