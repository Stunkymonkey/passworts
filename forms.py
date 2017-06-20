#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import BooleanField, TextField
from wtforms.validators import Required


class Input(FlaskForm):
    pw_length = TextField('pw_length')
    pw_count = TextField('pw_count')
    random = BooleanField('random', default=False)
    # process_data = process
