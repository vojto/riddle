from flask import Flask
from flask_peewee.db import Database
from flask_peewee.auth import Auth
from flask_peewee.admin import Admin
import functools
import json
from werkzeug import SharedDataMiddleware
import os

DATABASE = {
    'name': 'data.db',
    'engine': 'peewee.SqliteDatabase'
}

SECRET_KEY = 'this_is_too_secret'

RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''

app = Flask(__name__, static_folder='../../client/public', static_url_path='/static')
app.config.from_object(__name__)
app.config.from_pyfile("settings.cfg", silent=True)

db = Database(app)

@app.before_request
def sleep_app():
    import time
    # time.sleep(1)

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

    def login_required(self, fn):
        @functools.wraps(fn)

        def inner(*args, **kwargs):
            user = self.get_logged_in_user()

            if not user:
                return json.dumps({'response': 'error', 'reason': 'logged_out'}), 401
            return fn(*args, **kwargs)
        return inner

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

# Static files

app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
  '/': os.path.join(os.path.dirname(__file__), '../../client/public')
})
