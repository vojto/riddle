from riddle import app, db
from riddle.models.Questionnaire import Questionnaire
from peewee import *

class Question(db.Model):
    description = TextField()
    typ = IntegerField(choices=[(1, 'single'), (2, 'multi'), ('3', 'text')])
    presented = BooleanField()
    questionnaire = ForeignKeyField(Questionnaire)

app.logger.debug("Creating table for " + __name__)
Question.create_table(fail_silently=True)
