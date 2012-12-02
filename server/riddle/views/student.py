from flask import Blueprint
from riddle.views.helpers import *
from riddle.models.Questionnaire import Questionnaire
from riddle.models.Question import Question
from riddle.models.Category import Category
from riddle.models.Option import Option
from riddle.models.Answer import Answer
import json

student = Blueprint('student', __name__)

@student.route('/view/<qaire_id>/')
@student_session
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
@student_session
def settings():
    pass

# TODO: Check if this works.
@student.route('/submit-answer/', methods=['POST'])
@student_session
def submit_answer():
    question_id = request.form['question_id']

    qions = Question.select().where(Question.id == question_id)

    for qion in qions:
        qion_type = qtype2str(qion.typ)

        if qion_type == 'text':
            qion_text = request.form['text_answer']
            Answer.create(text=answer, question=qion)
        else:
            option_ids = request.form.getlist('option_ids')
            if len(option_ids) < 1:
                return response_error('missing_options')

            if qion_type == 'single':
                option_ids = option_ids[:1]

            for oid in option_ids:
                Answer.create(option=oid, question=qion)

        return response_success()

    return response_error('question_not_found')

# TODO
@student.route('/submit-comment/', methods=['POST'])
@student_session
def submit_comment():
    pass

