from riddle import app, db, model_classes
from peewee import *
from riddle.models.Question import Question
from flask_peewee.admin import ModelAdmin

class Option(db.Model):
    text = TextField()
    question = ForeignKeyField(Question)

class OptionAdmin(ModelAdmin):
    columns = ('text', 'question')

model_classes.append((Option, OptionAdmin))

