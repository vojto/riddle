from riddle import app, db, model_classes
from peewee import *
from flask_peewee.auth import BaseUser
from flask_peewee.admin import ModelAdmin

class Teacher(db.Model, BaseUser):
    username = CharField()
    fullname = CharField()
    password = CharField()
    active = BooleanField()
    superuser = BooleanField()

    def __unicode__(self):
        return '%s (%s)' % (self.username, self.fullname)

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


