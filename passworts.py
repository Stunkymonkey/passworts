#!/usr/bin/env python3

from flask import Flask, render_template, flash, redirect
from flask import Response, stream_with_context
from forms import Input
import generator
import input

"""
these lines are required, because pickle does not store the data type
https://stackoverflow.com/questions/27732354/unable-to-load-files-using-pickle-and-multipile-modules
"""
from collections import defaultdict


def dd():
    return defaultdict(int)


app = Flask('passworts')
app.config.from_object('config')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = Input()
    return render_template('index.html', title='Home', form=form)


@app.route('/result', methods=['POST'])
def result():
    def stream_pw():
        yield (render_template('result.html', title='Result'))
        yield ('\n<ul class="centeredList">\n')
        for i in range(pw_count):
            curr_pw = generator.generate(pw_length, random, "text.txt")
            # print (curr_pw)
            yield ('  <input class="result" type="text" value=%s readonly onclick="this.select();">\n' % curr_pw)
        yield ('</ul>\n')
        yield ('</div>\n')
        # print ("Finished")
    form = Input()
    if form.validate_on_submit():
        if input.check(form):
            random = form.random.data
            if not bool(random):
                pw_length = int(form.pw_length.data)
            else:
                pw_length = 0
            pw_count = int(form.pw_count.data)
            return Response(stream_with_context(stream_pw()))
        else:
            return redirect('/')
    else:
        return redirect('/')


@app.route('/result', methods=['GET'])
def result2():
    return redirect('/')


@app.route('/cancel', methods=['GET', 'POST'])
def cancel():
    flash("The generation sould be canceled (unsure)!")
    return redirect('/')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='Error')

if __name__ == '__main__':
    app.run()
