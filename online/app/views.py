from flask import render_template, flash, redirect, request
from app import app
from app.forms import Input
from app import generator


@app.route('/index')
def index():
	return redirect('/')
@app.route('/', methods = ['GET', 'POST'])
def home():
	form = Input()
	if form.validate_on_submit():
		try:
			int(form.pw_length.data)
		except ValueError:
			flash("You have to enter a number")
			return redirect('/')
		try:
			int(form.pw_count.data)
		except ValueError:
			flash("You have to enter a number")
			return redirect('/')
		if int(form.pw_length.data) <=4:
			flash("It is not possible to create a password unter 5 letters!")
			return redirect('/')
		if int(form.pw_length.data) >16:
			flash("It is not possible to create a password over 16 letters!")
			return redirect('/')
		if int(form.pw_count.data) <=0:
			flash("It is not possible to create no passwords!")
			return redirect('/')
		if int(form.pw_count.data) >50:
			flash("It is not possible to create more than 50 passwords!")
			return redirect('/')
		else:
			global requested
			requested = 'Here are your '+str(form.pw_count.data)+' passwords:'
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
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html', title = 'Error')