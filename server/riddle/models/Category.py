from riddle import app, db
from peewee import *
from riddle.models.Teacher import Teacher

class Category(db.Model):
    name = CharField()
    teacher = ForeignKeyField(Teacher)

app.logger.debug("Creating table for " + __name__)
Category.create_table(fail_silently=True)
