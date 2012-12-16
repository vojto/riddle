import json
from riddle import app, db, model_classes
from peewee import *
from flask_peewee.admin import ModelAdmin
from riddle.models.Student import Student
from riddle.models.Questionnaire import Questionnaire

class StudentPresence(db.Model):
    student = ForeignKeyField(Student)
    questionnaire = ForeignKeyField(Questionnaire)
    last_ping = DateTimeField()

    def to_json(self):
      return json.dumps({
        'student_id': self.student.id,
        'questionnaire_id': self.questionnaire.id,
        'last_ping': self.last_ping
      })

    @classmethod
    def update_latest(cls, student, questionnaire):
      # Try to find the last presence record
      print 'updating', student, questionnaire
      pres = cls.select().where((cls.student == student) & (cls.questionnaire == questionnaire)).get()
      print 'found pres', pres


class StudentPresenceAdmin(ModelAdmin):
    columns = ('student_id', 'questionnaire_id', 'last_ping')

model_classes.append((StudentPresence, StudentPresenceAdmin))

