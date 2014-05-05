from flask import render_template, flash, redirect, request 
import sys
from app import app
from app.forms import Input
from app import generator


@app.route('/')
def home():
	return redirect('/index')
@app.route('/index', methods = ['GET', 'POST'])
def index():
	form = Input()
	if form.validate_on_submit():
		global requested
		requested = 'Here are your '+str(form.pw_count.data)+' passwords:'

		#requested = 'You passwords are ' + str(form.pw_length.data) + ' letters long,' +'and you are getting ' + str(form.pw_count.data) + ' passwords.'
		global password_ready
		password_ready = (generator.generate(int(form.pw_length.data), int(form.pw_count.data)))
		return redirect('/result')
	return render_template('index.html', title = 'Home', form = form)

@app.route('/result', methods = ['GET', 'POST'])
def result():
	return render_template('result.html', title = 'Result', password_ready = password_ready, requested = requested)

@app.route('/impressum')
def impressum():
	return render_template('impressum.html', title = 'Impressum')