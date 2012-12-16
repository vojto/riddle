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

    def options(self):
      from riddle.models.Option import Option
      return [o for o in Option.select().where(Option.question == self)]

    def as_json(self):
      return {
        'description': self.description,
        'type': self.typ,
        'presented': self.presented,
        'options': [o.as_json() for o in self.options()]
      }


class QuestionAdmin(ModelAdmin):
    columns = ('description', 'typ', 'presented', 'questionnaire', 'id')

model_classes.append((Question, QuestionAdmin))
