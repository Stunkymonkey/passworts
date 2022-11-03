#!/usr/bin/env python3

from flask import flash

"""
top: -((8)/(40-1))x+(16+(8)/(40-1))
bottom: ((8-5)/40)x+(5-((8-5)/40))
"""


def input_check(form):
    input_correct = False
    while input_correct is False:
        if form.random.data is False:
            try:
                int(form.pw_length.data)
            except ValueError:
                flash("You have to enter a number")
                break
            if int(form.pw_length.data) <= 4:
                flash("It is not possible to create a password unter 5 letters!")
                break
            if int(form.pw_length.data) > 16:
                flash("It is not possible to create a password over 16 letters!")
                break
        try:
            int(form.pw_count.data)
        except ValueError:
            flash("You have to enter a number")
            break
        if int(form.pw_count.data) <= 0:
            flash("It is not possible to create no passwords!")
            break
        if int(form.pw_count.data) > 50:
            flash("It is not possible to create more than 50 passwords!")
            break
        input_correct = True
    return input_correct
