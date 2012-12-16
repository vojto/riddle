from riddle import app, db, model_classes
from riddle.models.Questionnaire import Questionnaire
from peewee import *
from flask_peewee.admin import ModelAdmin
import json

class Question(db.Model):
    description = TextField()
    typ = IntegerField(choices=[(1, 'single'), (2, 'multi'), (3, 'text')])
    presented = BooleanField()
    questionnaire = ForeignKeyField(Questionnaire)

    def __unicode__(self):
        return self.description


    def present(self):
      """Presents question while un-presenting all other questions in questionnaire"""
      Question.update(presented=False).where(Question.questionnaire==self.questionnaire).execute()
      self.presented = True
      self.save()


    def as_json(self):
      return {
        'description': self.description,
        'typ': self.typ,
        'presented': self.presented
      }


class QuestionAdmin(ModelAdmin):
    columns = ('description', 'typ', 'presented', 'questionnaire', 'id')

model_classes.append((Question, QuestionAdmin))
