import random
import string

CSRF_ENABLED = True
SECRET_KEY = str(''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)]))
APPNAME = "Passworts"
DEBUG = True
