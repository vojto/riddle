from riddle import app, db
from peewee import *
from riddle.models.Teacher import Teacher
from riddle.models.Category import Category

class Questionnaire(db.Model):
    name = CharField()
    pubid = CharField()
    category = ForeignKeyField(Category)

app.logger.debug("Creating table for " + __name__)
Questionnaire.create_table(fail_silently=True)
