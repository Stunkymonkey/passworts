from flask.ext.wtf import Form
from wtforms import BooleanField, TextField
from wtforms.validators import Required

class Input(Form):
	pw_length = TextField('pw_length')
	pw_count = TextField('pw_count')
	#random = BooleanField('random', default = False)
	#process_data1 = pw_count
	#process_data2 = pw_length
	#process_data = random