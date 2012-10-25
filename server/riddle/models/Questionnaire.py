from riddle import app, db, model_classes
from peewee import *
from riddle.models.Teacher import Teacher
from riddle.models.Category import Category
from flask_peewee.admin import ModelAdmin

class Questionnaire(db.Model):
    name = CharField()
    public_id = CharField()
    category = ForeignKeyField(Category)

class QuestionnaireAdmin(ModelAdmin):
    columns = ('name', 'public_id', 'category')


model_classes.append((Questionnaire, QuestionnaireAdmin))


