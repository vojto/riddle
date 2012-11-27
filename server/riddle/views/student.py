from flask import Blueprint
from riddle.views.helpers import *
from riddle.models.Questionnaire import Questionnaire
from riddle.models.Question import Question
from riddle.models.Category import Category
from riddle.models.Option import Option
import json

student = Blueprint('student', __name__)

@student.route('/view/<qaire_id>/')
def show(qaire_id):
    qaires = Questionnaire.select().where(Questionnaire.public_id == qaire_id)
    ret = {}

    def qtype2str(n):
        for ch in Question.typ.choices:
            if ch[0] == n:
                return ch[1]

        return 0

    for qaire in qaires:
        category = Category.select().join(Questionnaire).where(Questionnaire.id == qaire.id)
        questions = Question.select().join(Questionnaire).where(Questionnaire.id == qaire.id).where(Question.presented == True)

        catname = ''

        for cat in category:
            catname = cat.name
            break

        ret = {'name': qaire.name, 'category': catname, 'questions' : []}

        for qion in questions:
            qtype = qtype2str(qion.typ)
            ret['questions'].append({'type': qtype, 'description': qion.description})

            if qtype == 'single' or qtype == 'multi':
                ret['questions'][-1]['options'] = []
                options = Option.select().join(Question).where(Question.id == qion.id)

                for opt in options:
                    ret['questions'][-1]['options'].append({'text': opt.text})

    if not ret:
        ret = response_error('not_found', False)

    return json.dumps(ret)

# TODO
@student.route('/settings/', methods=['POST'])
def settings():
    pass

# TODO
@student.route('/submit-qaire/', methods=['POST'])
def submit_qaire():
    pass

# TODO
@student.route('/submit-comment/', methods=['POST'])
def submit_comment():
    pass

