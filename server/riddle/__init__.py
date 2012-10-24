from flask import Flask
from flask_peewee.db import Database
from flask_peewee.auth import Auth

DATABASE = {
    'name': 'data.db',
    'engine': 'peewee.SqliteDatabase'
}


app = Flask(__name__)
app.config.from_object(__name__)

db = Database(app)

print "Starting!"

import riddle.models
from riddle.models import Teacher

class TeacherAuth(Auth):
    def get_user_model(self):
        return Teacher

    def get_model_admin(self):
        return TeacherAdmin

auth = TeacherAuth(app, db)

import riddle.views

