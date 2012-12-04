from riddle import app, db, model_classes
from peewee import *
from flask_peewee.admin import ModelAdmin

class Student(db.Model):
    name = CharField()
    session_id = CharField()

    def __unicode__(self):
        return self.name

class StudentAdmin(ModelAdmin):
    columns = ('name', 'session_id')

model_classes.append((Student, StudentAdmin))

