#!/usr/bin/env python3

from app.forms import Input

#form = Input()

def check():
	try:
		int(form.pw_length.data)
	except ValueError:
		flash("You have to enter a number")
		input_correct = False
	try:
		int(form.pw_count.data)
	except ValueError:
		flash("You have to enter a number")
		input_correct = False
	print (input_correct)
	if input_correct == False:
		return input_correct
	else:
		if int(form.pw_length.data) <=4:
			flash("It is not possible to create a password unter 5 letters!")
			input_correct = False
		if int(form.pw_length.data) >16:
			flash("It is not possible to create a password over 16 letters!")
			input_correct = False
		if int(form.pw_count.data) <=0:
			flash("It is not possible to create no passwords!")
			input_correct = False
		if int(form.pw_count.data) >50:
			flash("It is not possible to create more than 50 passwords!")
			input_correct = False
		return input_correct