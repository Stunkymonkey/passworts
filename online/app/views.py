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
		wrong_input = False
		numbers = True
		try:
			int(form.pw_length.data)
		except ValueError:
			flash("You have to enter a number")
			numbers = False
		try:
			int(form.pw_count.data)
		except ValueError:
			flash("You have to enter a number")
			numbers = False
		if numbers == False:
			return redirect('/')
		if int(form.pw_length.data) <=4:
			flash("It is not possible to create a password unter 5 letters!")
			wrong_input = True
		if int(form.pw_length.data) >20:
			flash("It is not possible to create a password over 20 letters!")
			wrong_input = True
		if int(form.pw_count.data) <=0:
			flash("It is not possible to create no passwords!")
			wrong_input = True
		if int(form.pw_count.data) >100:
			flash("It is not possible to create more than 100 passwords!")
			wrong_input = True
		if wrong_input == True:
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