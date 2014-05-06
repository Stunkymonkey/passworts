#!/usr/bin/env python3

from flask import render_template, flash, redirect, request
from app import app
from app.forms import Input
from app import generator


@app.route('/', methods = ['GET', 'POST'])
def home():
	form = Input()
	return render_template('index.html', title = 'Home', form = form)

@app.route('/result', methods = ['GET', 'POST'])
def result():
	form = Input()
	if form.validate_on_submit():
		try:
			int(form.pw_length.data)
		except ValueError:
			flash("Please enter a real number")
			return redirect('/')
		try:
			int(form.pw_count.data)
		except ValueError:
			flash("Please enter a real number")
			return redirect('/')
		if int(form.pw_length.data) <=4:
			flash("It's not possible to create a password shorter than 5 letters!")
			return redirect('/')
		if int(form.pw_length.data) >16:
			flash("It's not possible to create a password longer than 16 letters!")
			return redirect('/')
		if int(form.pw_count.data) <=0:
			flash("Please create more than zero passwords")
			return redirect('/')
		if int(form.pw_count.data) >50:
			flash("It is not possible to create more than 50 passwords!")
			return redirect('/')
		else:
			global password_ready
			password_ready = (generator.generate(int(form.pw_length.data), int(form.pw_count.data)))
			return redirect('/result')
	return render_template('result.html', title = 'Result', password_ready = password_ready)

@app.route('/impressum')
def impressum():
	return render_template('impressum.html', title = 'Impressum')
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html', title = 'Error')