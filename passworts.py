#!/usr/bin/env python3
""" passworts flask webserver"""

from flask import Flask, Response, flash, redirect, render_template, stream_with_context
from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField
from wtforms.validators import InputRequired

import generator
from preprocess_type import integer_dict  # pylint: disable=unused-import


application = Flask("passworts")
application.config.from_object("config")


class Input(FlaskForm):
    """flask forms"""

    pw_length = IntegerField("pw_length")
    pw_count = IntegerField("pw_count", validators=[InputRequired()])
    random_lenght = BooleanField("random", default=False)


def input_check(form):
    """flask input validation"""
    input_correct = False
    while input_correct is False:
        if form.random_lenght.data is False:
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


@application.route("/", methods=["GET", "POST"])
def home():
    """index page"""
    form = Input()
    return render_template("index.html", title="Home", form=form)


@application.route("/result", methods=["POST"])
def result():
    """resulting page"""

    @stream_with_context
    def stream_pw():
        yield render_template("result.html", title="Result")
        yield '\n<ul class="centeredList">\n'
        for _i in range(pw_count):
            curr_pw = generator.generate(pw_length, random_lenght)
            # print(curr_pw)
            yield (
                f'<input class="result" type="text" value={curr_pw} readonly'
                ' onclick="this.select();">\n'
            )
        yield "</ul>\n"
        yield "</div>\n"

    form = Input()
    if form.validate_on_submit():
        if input_check(form):
            random_lenght = form.random_lenght.data
            if not bool(random_lenght):
                pw_length = int(form.pw_length.data)
            else:
                pw_length = 0
            pw_count = int(form.pw_count.data)
            # making sure with headers nginx does not cache anything
            return Response(stream_pw(), headers={'X-Accel-Buffering': 'no', 'Cache-Control': 'no-cache'})
        return redirect("/")
    return redirect("/")


@application.route("/result", methods=["GET"])
def result_get():
    """redirect get to results to index"""
    return redirect("/")


@application.errorhandler(404)
def page_not_found(_error):
    """error page display"""
    return render_template("404.html", title="Error")


if __name__ == "__main__":
    application.run()
