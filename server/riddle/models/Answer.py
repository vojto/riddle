from riddle import app, db, model_classes
from peewee import *
from riddle.models.Question import Question
from riddle.models.Option import Option
from riddle.models.Student import Student
from flask_peewee.admin import ModelAdmin

class Answer(db.Model):
    text = TextField(null=True)
    option = ForeignKeyField(Option, null=True)
    question = ForeignKeyField(Question)
    student = ForeignKeyField(Student)

class AnswerAdmin(ModelAdmin):
    columns = ('id', 'text', 'option', 'student')

model_classes.append((Answer, AnswerAdmin))
