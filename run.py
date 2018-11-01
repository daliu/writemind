#!flask/bin/python

from app import app, db, cli
from app.models import *

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Entry': Entry, 'SurveyResponse': SurveyResponse},
