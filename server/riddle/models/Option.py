from riddle import app, db
from peewee import *
from riddle.models.Question import Question

class Option(db.Model):
    text = TextField()
    question = ForeignKeyField(Question)

app.logger.debug("Creating table for " + __name__)
Option.create_table(fail_silently=True)

