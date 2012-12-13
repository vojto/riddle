from riddle import app, db, model_classes
from peewee import *
from riddle.models.Questionnaire import Questionnaire
from riddle.models.Student import Student
from flask_peewee.admin import ModelAdmin

class Rating(db.Model):
    like = BooleanField()
    student = ForeignKeyField(Student)
    questionnaire = ForeignKeyField(Questionnaire)

class RatingAdmin(ModelAdmin):
    columns = ('like', 'questionnaire')

model_classes.append((Rating, RatingAdmin))
