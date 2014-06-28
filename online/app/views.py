#!/usr/bin/env python3

from flask import render_template, flash, redirect
from app import app
from app.forms import Input
from app import generator
from app import input

@app.route('/', methods = ['GET', 'POST'])
def home():
	form = Input()
	return render_template('index.html', title = 'Home', form = form)

@app.route('/result', methods = ['POST'])
def result():
	form = Input()
	if form.validate_on_submit():
		cancel = False
		if input.check(form) == False:
			return redirect('/')	
		else:
			global password_ready
			password_ready = (generator.generate(int(form.pw_length.data), int(form.pw_count.data)))
			#return redirect('/result')
			return render_template('result.html', title = 'Result', password_ready = password_ready)

@app.route('/result', methods = ['GET'])
def result2():	
	return redirect('/')

@app.route('/cancel', methods = [ 'GET', 'POST'])
def cancel():
	generator.stop()
	flash("The generation was canceled!")
	return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html', title = 'Error')