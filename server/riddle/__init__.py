from flask import Flask
from flask_peewee.db import Database
from flask_peewee.auth import Auth
from flask_peewee.admin import Admin

DATABASE = {
    'name': 'data.db',
    'engine': 'peewee.SqliteDatabase'
}


app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'this_is_too_secret'

db = Database(app)

print "Starting!"

model_classes = []

import riddle.models

for mdl in model_classes:
    app.logger.debug("Creating table for " + mdl[0].__name__)
    mdl[0].create_table(fail_silently=True)

from riddle.models.Teacher import Teacher, TeacherAdmin

class TeacherAuth(Auth):
    def get_user_model(self):
        return Teacher

    def get_model_admin(self):
        return TeacherAdmin

class CustomAdmin(Admin):
    def check_user_permission(self, user):
        return user.superuser

auth = TeacherAuth(app, db)
admin = CustomAdmin(app, auth)

admin.register(Teacher, TeacherAdmin)

for mdl in model_classes:
    admin.register(mdl[0], mdl[1])

admin.setup()

import riddle.views

