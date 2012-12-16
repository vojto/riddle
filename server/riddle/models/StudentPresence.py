import json
from riddle import app, db, model_classes
from peewee import *
from flask_peewee.admin import ModelAdmin
from riddle.models.Student import Student
from riddle.models.Questionnaire import Questionnaire
from datetime import datetime, timedelta

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
      now = datetime.now()
      try:
        pres = cls.get(cls.student == student, cls.questionnaire == questionnaire)
        pres.last_ping = now
      except cls.DoesNotExist:
        pres = cls(student=student, questionnaire=questionnaire, last_ping=now)
      pres.save()

    @classmethod
    def count_active(cls, questionnaire):
      reference_time = datetime.now() + timedelta(seconds=-15)
      query = cls.select().where(cls.questionnaire == questionnaire, cls.last_ping > reference_time)
      return query.count()



class StudentPresenceAdmin(ModelAdmin):
    columns = ('student_id', 'questionnaire_id', 'last_ping')

model_classes.append((StudentPresence, StudentPresenceAdmin))

