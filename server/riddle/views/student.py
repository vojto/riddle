from flask import Blueprint
from riddle.views.helpers import *
from riddle.models.Questionnaire import Questionnaire
from riddle.models.Question import Question
from riddle.models.Category import Category
from riddle.models.Option import Option
from riddle.models.Answer import Answer
from riddle.models.Comment import Comment
import json
import datetime

student = Blueprint('student', __name__)

@student.route('/view/<qaire_id>/')
@student_session
def show(qaire_id):
    qaires = Questionnaire.select().where(Questionnaire.public_id == qaire_id)
    ret = {}

    for qaire in qaires:
        category = Category.select().join(Questionnaire).where(Questionnaire.id == qaire.id)
        questions = Question.select().join(Questionnaire).where(Questionnaire.id == qaire.id).where(Question.presented == True)

        catname = ''

        for cat in category:
            catname = cat.name
            break

        ret = {'id': qaire.id, 'name': qaire.name, 'category': catname, 'questions' : []}

        for qion in questions:
            qtype = qtype2str(qion.typ)
            ret['questions'].append({'id': qion.id, 'type': qtype, 'description': qion.description})

            if qtype == 'single' or qtype == 'multi':
                ret['questions'][-1]['options'] = []
                options = Option.select().join(Question).where(Question.id == qion.id)

                for opt in options:
                    ret['questions'][-1]['options'].append({'id': opt.id, 'text': opt.text})

    if not ret:
        ret = response_error('not_found', False)

    return json.dumps(ret)

@student.route('/get-settings/')
@student_session
def get_settings():
    student = get_current_student()

    return json.dumps({'name': student.name})

@student.route('/set-settings/', methods=['POST'])
@student_session
def set_settings():
    student = get_current_student()
    name = request.form['name']
    student.name = name
    student.save()

    return response_success()

@student.route('/submit-answer/', methods=['POST'])
@student_session
def submit_answer():
    student = get_current_student()
    question_id = request.form['question_id']

    qions = Question.select().where(Question.id == question_id)

    for qion in qions:
        qion_type = qtype2str(qion.typ)

        if qion_type == 'text':
            qion_text = request.form['text_answer']
            Answer.create(text=answer, question=qion, student=student)
        else:
            option_ids = request.form.getlist('option_ids')
            if len(option_ids) < 1:
                return response_error('missing_options')

            if qion_type == 'single':
                option_ids = option_ids[:1]

            for oid in option_ids:
                Answer.create(option=oid, question=qion, student=student)

        return response_success()

    return response_error('question_not_found')

@student.route('/submit-comment/', methods=['POST'])
@student_session
def submit_comment():
    student = get_current_student()
    qaire_id = request.form['qaire_id']
    subject = request.form['subject']
    body = request.form['body']

    qaires = Questionnaire.select().where(Questionnaire.id == qaire_id)

    for qaire in qaires:
        Comment.create(author=student.name, subject=subject, body=body, questionnaire=qaire, datetime=datetime.datetime.now())
        return response_success()

    return response_error('questionnaire_not_found')


@student.route('/view-comments/', methods=['POST'])
@student_session
def view_comments():
    student = get_current_student()
    qaire_id = request.form['qaire_id']
    offset = request.form.get('offset')
    limit = 10

    if not offset:
        offset = 0
    else:
        offset = int(offset)

    comments = Comment.select().where(Comment.questionnaire == qaire_id).limit(limit).offset(offset)

    ret = []

    for comment in comments:
        ret.append({'id': comment.id, 'author': comment.author, 'subject': comment.subject, 'body': comment.body, 'datetime': comment.datetime.isoformat()})

    return json.dumps(ret)
