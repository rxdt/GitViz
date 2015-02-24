from flask import Flask, render_template, url_for, request, redirect, flash, render_template
from flask import session as flask_session
from forms import SignupForm, LoginForm, RequestVisualization
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from flask.ext.github import GitHub
from user_model import User, db, session
import os
import sqlalchemy.exc

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['GITHUB_CLIENT_ID'] = os.environ['GITHUB_CLIENT_ID']
app.config['GITHUB_CLIENT_SECRET'] = os.environ['GITHUB_CLIENT_SECRET']
github = GitHub(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
  user = session.query(User).get(userid)
  return User(user.username, user.id)

@app.route('/', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = session.query(User).filter_by(username=form.username.data).first()
    if user:
      if user.check_password(form.password.data):
        user.authenticated = True
        flask_session['username'] = form.username.data
        login_user(user, remember=True)
        flash(u'Successfully logged in as %s' % form.user.username)
        return redirect(url_for('visualize'))
  return render_template('login.html', form=form)
  # return github.authorize()

@app.route("/logout")
@login_required
def logout():
  user = current_user
  user.authenticated = False
  logout_user()
  return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()

  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('signup.html', form=form)
    else:
      try:
        newuser = User(form.username.data, form.password.data)
        session.add(newuser)
        session.commit()
        flask_session['username'] = newuser.username
        flash('User successfully signed up.')
        return redirect(url_for('visualize'))
      except:
        flash('There was an issue creating the user. Try again')
        return render_template('signup.html', form=form)

  elif request.method == 'GET':
    return render_template('signup.html', form=form)

@login_required
@app.route('/visualize')
def visualize():
  if 'username' not in flask_session:
    return redirect(url_for('login'))
  # return render_template('visualize.html', client_id=app.config['GITHUB_CLIENT_ID'], client_secret=app.config['GITHUB_CLIENT_SECRET'])
  # return github.authorize()

@github.access_token_getter
def token_getter():
  user = current_user
  if user is not None:
    return user.github_access_token

@app.route('/callback') #http://goo.gl/s8pKEs
@github.authorized_handler
def authorized(oauth_token):
  if oauth_token is None:
    flash("Authorization failed.")
    return redirect(url_for('visualize'))
  else:
    flash("Successfully authorized")

  user = User.query.filter_by(github_access_token=oauth_token).first()
  if user is None:
      user = User(oauth_token)
      session.add(user)

  user.github_access_token = oauth_token
  session.commit()
  return redirect(next_url)

if __name__ == '__main__':
  app.run(debug=True)  





