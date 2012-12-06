from flask import request
from riddle import app, auth
from riddle.views.teacher import teacher
from riddle.views.teacher import captcha
from riddle.views.helpers import *
from riddle.models.Question import Question
from riddle.models.Questionnaire import Questionnaire
from riddle.models.Category import Category
from riddle.models.Option import Option

@teacher.route('/new-option/', methods=['POST'])
@auth.login_required
def new_option():
    user = auth.get_logged_in_user()
    question_id = request.form['question_id']
    text = request.form['text']

    qions = Question.select().join(Questionnaire).join(Category).where(Category.teacher == user).where(Question.id == question_id)

    for qion in qions:
        typ = qtype2str(qion.typ)
        if typ == 'single' or typ == 'multi':
            option = Option.create(text=text, question=qion)
            ret = response_success(False)
            ret['option_id'] = option.id
            return json.dumps(ret)
        else:
            return response_error('options_not_supported')

    return response_error('question_not_found')

@teacher.route('/edit-option/', methods=['POST'])
@auth.login_required
def edit_option():
    user = auth.get_logged_in_user()
    option_id = request.form['option_id']
    text = request.form['text']

    opts = Option.select().join(Question).join(Questionnaire).join(Category).where(Category.teacher == user).where(Option.id == option_id)

    for opt in opts:
        opt.text = text
        opt.save()
        return response_success()

    return response_error('option_not_found')

@teacher.route('/remove-option/', methods=['POST'])
@auth.login_required
def remove_option():
    user = auth.get_logged_in_user()
    option_id = request.form['option_id']

    opts = Option.select().join(Question).join(Questionnaire).join(Category).where(Category.teacher == user).where(Option.id == option_id)

    for opt in opts:
        opt.delete_instance(recursive=True, delete_nullable=True)
        return response_success()

    return response_error('option_not_found')

