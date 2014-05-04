from flask.ext.wtf import Form
from wtforms import IntegerField, BooleanField
from wtforms.validators import Required

class Input(Form):
	pw_length = IntegerField('pw_length', validators = [Required()])
	pw_count = IntegerField('pw_count', validators = [Required()])
	#random = BooleanField('random', default = False)
	#process_data1 = pw_count
	#process_data2 = pw_length
	#process_data = random