from riddle import app, db
from peewee import *
from riddle.models.Questionnaire import Questionnaire

class Rating(db.Model):
    like = BooleanField()
    questionnaire = ForeignKeyField(Questionnaire)

app.logger.debug("Creating table for " + __name__)
Rating.create_table(fail_silently=True)
