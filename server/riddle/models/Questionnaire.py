from riddle import app, db, model_classes
from peewee import *
from riddle.models.Teacher import Teacher
from riddle.models.Category import Category
import riddle.models.Question
from flask_peewee.admin import ModelAdmin

class Questionnaire(db.Model):
    name = CharField()
    public_id = CharField()
    category = ForeignKeyField(Category)

    def __unicode__(self):
        return "%s (ID: %s)" % (self.name, self.public_id)

    def presented_question(self):
        Question = riddle.models.Question.Question
        try:
            return Question.select().where(Question.questionnaire == self, Question.presented == True).get()
        except Question.DoesNotExist:
            return None

    class Meta:
        indexes = (
            (('public_id',), True),
            (('name', 'category'), False)
        )

class QuestionnaireAdmin(ModelAdmin):
    columns = ('name', 'public_id', 'category')


model_classes.append((Questionnaire, QuestionnaireAdmin))


