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
		if int(form.pw_length.data) <=3:
			flash("It is not possible to create a password unter 4 letters!")
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