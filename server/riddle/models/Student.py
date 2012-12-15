from riddle import app, db, model_classes
from peewee import *
from flask_peewee.admin import ModelAdmin
import json

class Student(db.Model):
    name = CharField()
    session_id = CharField()

    def __unicode__(self):
        return self.name

    def to_json(self):
      data = {
        'name': self.name,
        'session_id': self.session_id
      }
      return json.dumps(data)


class StudentAdmin(ModelAdmin):
    columns = ('name', 'session_id')

model_classes.append((Student, StudentAdmin))

