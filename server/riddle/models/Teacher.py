from riddle import app, db
from peewee import *
from flask_peewee.auth import BaseUser
from flask_peewee.admin import ModelAdmin

class Teacher(db.Model, BaseUser):
    username = CharField()
    fullname = CharField()
    password = CharField()
    superuser = BooleanField()

class TeacherAdmin(ModelAdmin):
    columns = ('username', 'fullname', 'password', 'superuser')

app.logger.debug("Creating table for " + __name__)
Teacher.create_table(fail_silently=True)
