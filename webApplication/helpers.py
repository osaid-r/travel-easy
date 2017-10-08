from flask import render_template

def apologize(message):
	return render_template('apology.html', message=message)