from riddle import app, db, model_classes
from peewee import *
from riddle.models.Questionnaire import Questionnaire
from flask_peewee.admin import ModelAdmin

class Comment(db.Model):
    author = CharField()
    subject = CharField()
    body = TextField()
    questionnaire = ForeignKeyField(Questionnaire)
    datetime = DateTimeField()

class CommentAdmin(ModelAdmin):
    columns = ('subject', 'body', 'questionnaire')

model_classes.append((Comment, CommentAdmin))
