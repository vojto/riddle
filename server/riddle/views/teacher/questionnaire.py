from flask import request
from riddle import app, auth
from riddle.views.teacher import teacher
from riddle.views.helpers import *
from riddle.models.Questionnaire import Questionnaire
from riddle.models.Category import Category

@teacher.route('/new-questionnaire/', methods=['POST'])
@auth.login_required
def new_questionnaire():
    user = auth.get_logged_in_user()

    name = request.form['name']
    category_id = request.form['category_id']
    public_id = request.form.get('public_id')

    if not public_id:
        public_id = public_id_from_name(name)

    ret = {}

    cats = Category.select().where(Category.teacher == user).where(Category.id == category_id)

    category = None

    for cat in cats:
        category = cat
        break

    if not category:
        return response_error('category_not_found')

    questionnaire = Questionnaire.create(name=name, public_id=public_id, category=category)
    if not questionnaire:
        return response_error('already_exists')

    ret = response_success(False)
    ret['public_id'] = public_id
    ret['id'] = questionnaire.id
    return json.dumps(ret)


@teacher.route('/edit-questionnaire/', methods=['POST'])
@auth.login_required
def edit_questionnaire():
    user = auth.get_logged_in_user()

    questionnaire_id = request.form['id']
    name = request.form.get('name')
    category_id = request.form.get('category_id')
    public_id = request.form.get('public_id')

    qaires = Questionnaire.select().join(Category).where(Category.teacher == user).where(Questionnaire.id == questionnaire_id)

    for qaire in qaires:
        if category_id:
            categs = Category.select().where(Category.teacher == user).where(Category.id == category_id)
            for categ in categs:
                qaire.category = categ
                break
            else:
                return response_error('category_not_found')

        if public_id:
            qaires2 = Questionnaire.select().where(Questionnaire.public_id == public_id)
            for qaire2 in qaires2:
                return response_error('public_id_already_exists')

            qaire.public_id = public_id

        if name:
            qaire.name = name

        qaire.save()

        return response_success()

    return response_error('questionnaire_not_found')

@teacher.route('/remove-questionnaire/', methods=['POST'])
@auth.login_required
def remove_questionnaire():
    user = auth.get_logged_in_user()
    questionnaire_id = request.form['id']

    qaires = Questionnaire.select().join(Category).where(Category.teacher == user).where(Questionnaire.id == questionnaire_id)

    for qaire in qaires:
        qaire.delete_instance(recursive=True, delete_nullable=True)

        return response_success()

    return response_error('questionnaire_not_found')

