from riddle import app, db, model_classes
from peewee import *
from riddle.models.Teacher import Teacher
from flask_peewee.admin import ModelAdmin

class Category(db.Model):
    name = CharField()
    teacher = ForeignKeyField(Teacher)

    def __unicode__(self):
        return self.name

class CategoryAdmin(ModelAdmin):
    columns = ('name', 'teacher')

model_classes.append((Category, CategoryAdmin))

