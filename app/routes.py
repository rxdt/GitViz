from flask import Flask, session, render_template, url_for, request, redirect, flash
from flask import Flask, render_template
from forms import SignupForm, RequestVisualization
from user_model import User, db
import os
import sys
import sqlalchemy.exc

app = Flask(__name__)
db.init_app(app)
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
        db.session.add(newuser)
        db.session.commit()
        session['username'] = newuser.username
        flash('User successfully signed up.')
        return redirect(url_for('visualizer'))
      except sqlalchemy.exc.SQLAlchemyError, e:
        print 'There was an issue creating the user.  Error %s. ' % e   
        flash('There was an issue creating the user. Try again')
        return render_template('signup.html', form=form)

      

  if request.method == 'GET':
    return render_template('signup.html', form=form)


@app.route('/visualizer')
def visualize():
  form = RequestVisualization()


if __name__ == '__main__':
  app.run(debug=True)






