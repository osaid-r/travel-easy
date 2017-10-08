from flask import Flask, request, render_template, redirect, session, flash
from flask_mysqldb import MySQL
from helpers import *
import MySQLdb

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'temp'
app.config['MYSQL_PASSWORD'] = 'temporary'
app.config['MYSQL_DB'] = 'Company'
mysql = MySQL(app)

@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
	if session.get('logged'):
		return redirect('/profile')

	if request.method == 'GET':
		return render_template('index.html')

	else:
		if not all(request.form.values()):
			return apologize('Please enter all the details')

		cur = mysql.connection.cursor()
		try:
			query = '''SELECT * FROM Users WHERE username = "{0}"'''.format(request.form['username'])
			cur.execute(query)
			l = cur.fetchall()

			if len(l) != 1:
				return apologize('Incorrect login details')

			#not a good idea to keep the authentication like this
			if request.form['username'] == l[0][0] and request.form['password'] == l[0][2]:
				session['username'] = request.form['username']
				session['logged'] = True
				return redirect('/profile')

			else:
				return apologize('Incorrect login details')

		except (MySQLdb.Error, MySQLdb.Warning) as e:
			return apologize('Incorrect login details')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if session.get('logged'):
		return redirect('/profile')

	if request.method == 'GET':
		return render_template('reg_form.html')

	else:
		if not all(request.form.values()):
			return apologize('Please enter all the details')

		elif request.form['password'] != request.form['confirmation']:
			return apologize('Passwords do not match')

		else:
			cur = mysql.connection.cursor()

			#not a good idea to store passwords like this
			query = '''INSERT IGNORE INTO Users (username, name, password, credit) VALUES("{0}", "{1}", "{2}", 0)'''.format(request.form['username'], request.form['name'] ,request.form['password'])
			cur.execute(query)
			mysql.connection.commit()
			session['username'] = request.form['username']
			session['logged'] = True
			return redirect('/profile')


@app.route('/profile', methods=['GET'])
def profile():
	if not session.get('logged'):
		return redirect('/register')

	cur = mysql.connection.cursor()
	query = '''SELECT * FROM Users WHERE username = "{0}"'''.format(session.get('username'))

	cur.execute(query)
	l = cur.fetchall()

	return render_template('profile.html', l=l[0])

@app.route('/shop', methods=['GET', 'POST'])
def shop():
	return render_template('shop.html')

@app.route('/list')
def list():
	return render_template('list.html')

@app.route('/items/<category>')
def items(category):
	cur = mysql.connection.cursor()
	query = '''SELECT * FROM Items WHERE category = "{0}"'''.format(category)

	cur.execute(query)
	l = cur.fetchall()
	return render_template('items.html', l=l)

@app.route('/logout')
def logout():
	session.pop('username', None)
	session.pop('logged', None)
	return redirect('/index')

if __name__ == '__main__':
	app.secret_key = 'somerandomkey'
	app.run(debug=True)