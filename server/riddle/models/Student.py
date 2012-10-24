from riddle import app, db
from peewee import *

class Student(db.Model):
    name = CharField()
    sessid = CharField()

app.logger.debug("Creating table for " + __name__)
Student.create_table(fail_silently=True)
