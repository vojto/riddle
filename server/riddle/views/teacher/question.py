from flask import request
from riddle import app, auth
from riddle.views.teacher import teacher
from riddle.views.helpers import *
from riddle.models.Question import Question
from riddle.models.Questionnaire import Questionnaire
from riddle.models.Category import Category

@teacher.route('/new-question/', methods=['POST'])
@auth.login_required
def new_question():
    user = auth.get_logged_in_user()

    description = request.form['description']
    typ = request.form['type']
    presented = request.form.get('presented', False)
    public_id = request.form['public_id']

    ret = {}

    qaires = Questionnaire.select().join(Category).where(Category.teacher == user).where(Questionnaire.public_id == public_id)

    for qaire in qaires:
        if qtype2str(typ) is None:
            return response_error('unknown_question_type')

        question = Question.create(description=description, typ=typ, presented=presented, questionnaire=qaire)

        ret = response_success(False)
        ret['question_id'] = question.id
        return json.dumps(ret)

    return response_error('public_id_not_found')

@teacher.route('/edit-question/', methods=['POST'])
@auth.login_required
def edit_question():
    user = auth.get_logged_in_user()

    question_id = request.form['id']
    description = request.form.get('description')
    typ = request.form.get('type')
    presented = request.form.get('presented')
    public_id = request.form.get('public_id')

    ret = {}

    qions = Question.select().join(Questionnaire).join(Category).where(Category.teacher == user).where(Question.id == question_id)

    for qion in qions:
        if description is not None:
            qion.description = description

        if typ:
            if not qtype2str(typ):
                return response_error('unknown_question_type')

            qion.typ = typ

        if presented is not None:
            qion.presented = presented

        if public_id:
            qaires = Questionnaire.select().join(Category).where(Category.teacher == user).where(Questionnaire.public_id == public_id)
            for qaire in qaires:
                qion.public_id = public_id
                break
            else:
                return response_error('public_id_not_found')


        qion.save()

        if typ and qtype2str(qion.typ) == 'text':
            # Delete options when changing type to 'text'.
            opts = Option.select().where(Option.question == qion)
            for opt in opts:
                opt.delete_instance(recursive=True, delete_nullable=True)

        return response_success()


    return response_error('question_not_found')


@teacher.route('/remove-question/', methods=['POST'])
@auth.login_required
def remove_question():
    user = auth.get_logged_in_user()
    question_id = request.form['id']

    qions = Question.select().join(Questionnaire).join(Category).where(Category.teacher == user).where(Question.id == question_id)

    for qion in qions:
        qion.delete_instance(recursive=True, delete_nullable=True)
        return response_success()

    return response_error('question_not_found')
