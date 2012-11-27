from riddle import app, db, model_classes
from riddle.models.Questionnaire import Questionnaire
from peewee import *
from flask_peewee.admin import ModelAdmin

class Question(db.Model):
    description = TextField()
    typ = IntegerField(choices=[(1, 'single'), (2, 'multi'), (3, 'text')])
    presented = BooleanField()
    questionnaire = ForeignKeyField(Questionnaire)

    def __unicode__(self):
        return self.description

class QuestionAdmin(ModelAdmin):
    columns = ('description', 'typ', 'presented', 'questionnaire', 'id')

model_classes.append((Question, QuestionAdmin))
