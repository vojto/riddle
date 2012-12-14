from flask import Blueprint
from riddle.views.helpers import *
from riddle.models.Questionnaire import Questionnaire
from riddle.models.Question import Question
from riddle.models.Category import Category
from riddle.models.Option import Option
from riddle.models.Answer import Answer
from riddle.models.Comment import Comment

student = Blueprint('student', __name__)

