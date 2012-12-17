from riddle import app, db, model_classes
from peewee import *
from flask_peewee.auth import BaseUser
from flask_peewee.admin import ModelAdmin
import json

class Teacher(db.Model, BaseUser):
    username = CharField()
    fullname = CharField()
    email = CharField()
    password = CharField()
    active = BooleanField()
    superuser = BooleanField()

    def __unicode__(self):
        return '%s (%s)' % (self.username, self.fullname)

    def as_json(self):
        return {
            'username': self.username,
            'fullname': self.fullname,
            'email': self.email
        }

class TeacherAdmin(ModelAdmin):
    columns = ('username', 'fullname', 'password', 'superuser')

    def save_model(self, instance, form, adding=False):
        orig_password = instance.password

        user = super(TeacherAdmin, self).save_model(instance, form, adding)

        if orig_password != form.password.data:
            user.set_password(form.password.data)
            user.save()

        return user


model_classes.append((Teacher, TeacherAdmin))


