from flask import Flask, session, render_template, url_for, request, redirect, flash
from flask import Flask, render_template
from forms import SignupForm

from user_model import User
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def login():
  error = None

  if 'username' in session:
    return 'Logged in as %s' % escape(session['username']) # or flash message instead
    # and link to or redirect to next page

  if request.method == 'POST':
    username = request.form['username']
    pw = request.form['password']
    username_result = User.query.filter_by(username=username)

    # if username_query:
    #   session['username'] = request.form['username']
    #   return log_the_user_in(request.form['username'])
    # else:
    #   error = 'Invalid username/password'
  print "HERE "
  return render_template('login.html', error=error)

@app.route('/logout')
def logout():
  # session.pop('username', None)
  del session['username']
  del session['email']

  return redirect(url_for('/'))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
  form = SignupForm()

  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('signup.html', form=form)
    else:
      return 'User successfully created.'
  if request.method == 'GET':
    return render_template('signup.html', form=form)

    # email = request.form['email']
    # password = request.form['password']
    # u = User(email=email, password=password)
    # db_session.add(u) 
    # db_session.commit()
    # return redirect("/")


if __name__ == '__main__':
  app.run(debug=True)






