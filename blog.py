# blog.py - controller

# imports
from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3
from functools import wraps

# config
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = '\xf3\xde\xa6\xa9\x85\x07\x06\x0f\x03\xea\xad;ZOu\xf0\xbd\x96c\xc9\xa7\nT\xc5'


app = Flask(__name__)

# pulls in app config by looking for UPPERCASE variables
app.config.from_object(__name__)

#function used for connecting to the db
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap

@app.route('/', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['usename']!=app.config['USERNAME'] or\
			request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid Credentials. Please try again.'
		else:
			session['logged_in'] = True
			return redirect(url_for('main'))
	return render_template('login.html', error=error)

@app.route('/main')
@login_required
def main():
	g.db = connect_db()
	cur = g.db.execute('select * from posts')
	posts = [dict(title=row[0], posts=row[1]) for row in cur.fetchall()]
	g.db.close()

	return render_template('main.html', posts=posts)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug=True)