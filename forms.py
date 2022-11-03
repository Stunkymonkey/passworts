#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField
from wtforms.validators import InputRequired


class Input(FlaskForm):
    pw_length = IntegerField("pw_length", validators=[InputRequired()])
    pw_count = IntegerField("pw_count", validators=[InputRequired()])
    random = BooleanField("random", default=False)
