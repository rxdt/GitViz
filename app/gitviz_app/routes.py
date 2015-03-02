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
app.config['GITHUB_TOKEN'] = os.environ['GITHUB_TOKEN']
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
        return github.authorize()

  return render_template('login.html', form=form)

@app.route("/logout")
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
        login_user(user, remember=True)
        flash('User successfully signed up.')
        return github.authorize()
      except:
        flash('There was an issue creating the user. Try again')
        return render_template('signup.html', form=form)

  elif request.method == 'GET':
    return render_template('signup.html', form=form)

@github.access_token_getter
def token_getter():
  if current_user is not None:
    return current_user.github_access_token

@app.route('/callback') #http://goo.gl/s8pKEs
@github.authorized_handler
def authorized(access_token):
    if not current_user.is_authenticated:
      print '1 1 1'
      return redirect(url_for('login'))

    # next_url = request.args.get('next') or render_template('visualize.html')
    print '2 2 2'

    if access_token is None:
      print '3 3 3'
      # return redirect(next_url)
      return render_template('visualize.html', client_id=os.environ['GITHUB_CLIENT_ID'], client_secret=os.environ['GITHUB_CLIENT_SECRET'])

    current_user.github_access_token = oauth_token
    print '4 4 4'
    session.commit()
    print '5 5 5'

    return render_template('visualize.html')


@app.route('/user')
def user():
    return str(github.get('current_user'))

if __name__ == '__main__':
  app.run(debug=True)  





