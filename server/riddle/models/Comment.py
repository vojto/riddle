from riddle import app, db, model_classes
from peewee import *
from riddle.models.Questionnaire import Questionnaire
from flask_peewee.admin import ModelAdmin

class Comment(db.Model):
    subject = CharField()
    body = TextField()
    questionnaire = ForeignKeyField(Questionnaire)

class CommentAdmin(ModelAdmin):
    columns = ('response', 'questionnaire')

model_classes.append((Comment, CommentAdmin))
