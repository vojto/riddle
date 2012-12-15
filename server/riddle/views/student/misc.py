from riddle.views.student import student
from riddle.views.helpers import *
from riddle.models.Question import Question
from riddle.models.Questionnaire import Questionnaire
from riddle.models.Category import Category
from riddle.models.Option import Option
from riddle.models.Answer import Answer
from riddle.models.Rating import Rating
import json

@student.route('/student/status')
def status():
    student = get_student()
    if student:
        return student.to_json()
    else:
        return json.dumps(None)

@student.route('/student/login')
def login():
    name = request.args.get('name')
    get_current_student(name)
    return response_success()

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

@student.route('/submit-answer/', methods=['POST'])
@student_session
def submit_answer():
    student = get_current_student()
    question_id = request.form['question_id']

    qions = Question.select().where(Question.id == question_id)

    for qion in qions:
        qion_type = qtype2str(qion.typ)

        if qion_type == 'text':
            text_answer = request.form['text_answer']
            Answer.create(text=text_answer, question=qion, student=student)
        else:
            option_ids = request.form.getlist('option_ids')
            if len(option_ids) < 1:
                return response_error('missing_options')

            if qion_type == 'single':
                option_ids = option_ids[:1]

            final_opts = []

            for oid in option_ids:
                opts = Option.select().where(Option.question == qion).where(Option.id == oid)
                for opt in opts:
                    final_opts.append(opt)
                    break
                else:
                    return response_error('wrong_option')

            for opt in final_opts:
                    Answer.create(option=opt, question=qion, student=student)

        return response_success()

    return response_error('question_not_found')

@student.route('/submit-rating/', methods=['POST'])
@student_session
def submit_rating():
    student = get_current_student()
    qaire_id = request.form['qaire_id']
    like = request.form['like']

    qaires = Questionnaire.select().where(Questionnaire.id == qaire_id)

    for qaire in qaires:
        ratings = Rating.select().where(Rating.student == student).where(Rating.questionnaire == qaire)
        for rating in ratings:
            return response_error('already_rated')

        if like == "1" or like == "true":
            like = True
        else:
            like = False

        Rating.create(like=like, student=student, questionnaire=qaire)

        return response_success()

    return response_error('questionnaire_not_found')


