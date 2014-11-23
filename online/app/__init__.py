from flask import Flask
import os

app = Flask(__name__)
app.config.from_object('config')

from app import views
