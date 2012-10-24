from riddle import app, db
from peewee import *
from riddle.models.Question import Question
from riddle.models.Option import Option

class Answer(db.Model):
    text = TextField()
    option = ForeignKeyField(Option)
    question = ForeignKeyField(Question)

app.logger.debug("Creating table for " + __name__)
Answer.create_table(fail_silently=True)

