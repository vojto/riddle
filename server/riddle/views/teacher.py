from flask import Blueprint, request
from riddle import app, auth
from riddle.views.helpers import *
from riddle.models.Teacher import Teacher
from riddle.models.Questionnaire import Questionnaire
from riddle.models.Category import Category
from riddle.models.Question import Question
from riddle.models.Option import Option
import json
import recaptcha
import string
import random

IS_CAPTCHA_ENABLED = False

teacher = Blueprint('teacher', __name__)
captcha = recaptcha.RecaptchaClient(app.config['RECAPTCHA_PRIVATE_KEY'], app.config['RECAPTCHA_PUBLIC_KEY'])


@teacher.route('/qaires/')
@auth.login_required
def show_qaires():
    user = auth.get_logged_in_user()
    cats = Category.select().join(Teacher).where(Teacher.id == user.id)
    ret = []
    for c in cats:
        ret.append({'id': c.id, 'category': c.name, 'questionnaires': []})
        qaires = Questionnaire.select().join(Category).where(Category.id == c.id)
        for q in qaires:
            ret[-1]['questionnaires'].append({'id': q.id, 'name': q.name, 'public_id': q.public_id})

    return json.dumps(ret)

@teacher.route('/qaires/<qaire_id>/')
@auth.login_required
def show_questions(qaire_id):
    user = auth.get_logged_in_user()
    qaires = Questionnaire.select().join(Category).where(Questionnaire.public_id == qaire_id).where(Category.teacher == user)

    ret = {}

    for qaire in qaires:
        category = Category.select().join(Questionnaire).where(Questionnaire.id == qaire.id)
        questions = Question.select().join(Questionnaire).where(Questionnaire.id == qaire.id)

        catname = ''

        for cat in category:
            catname = cat.name
            break

        ret = {'id': qaire.id, 'name': qaire.name, 'category': catname, 'questions' : []}

        for qion in questions:
            qtype = qtype2str(qion.typ)
            ret['questions'].append({'id': qion.id, 'type': qtype, 'description': qion.description, 'presented': qion.presented})

            if qtype == 'single' or qtype == 'multi':
                ret['questions'][-1]['options'] = []
                options = Option.select().join(Question).where(Question.id == qion.id)

                for opt in options:
                    ret['questions'][-1]['options'].append({'id': opt.id, 'text': opt.text})

    return json.dumps(ret)

@teacher.route('/categories/')
@auth.login_required
def show_categories():
    user = auth.get_logged_in_user()
    cats = Category.select().where(Category.teacher == user)
    ret = []
    for c in cats:
        ret.append({'name': c.name, 'id': c.id})

    return json.dumps(ret)

@teacher.route('/new-category/', methods = ['POST'])
@auth.login_required
def add():
    user = auth.get_logged_in_user()
    name = request.form['name']
    cats = Category.select().join(Teacher).where(Teacher.id == user.id).where(Category.name == name);

    for c in cats:
        return response_error('already_exists')

    Category.insert(name=name, teacher=user).execute()

    return response_success()

@teacher.route('/login/', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    teacher = auth.authenticate(username, password)

    if teacher == False:
        return response_error('wrong_password')

    auth.login_user(teacher)

    return response_success()

@teacher.route('/logout/')
@auth.login_required
def logout():
    auth.logout_user(auth.get_logged_in_user())

    return response_success()

@teacher.route('/registration/', methods=['POST'])
def registration():
    username = request.form['username']
    fullname = request.form['fullname']
    password = request.form['password']
    email    = request.form['email']
    ret = {}

    captcha_result = check_captcha(request)
    if captcha_result[0] == False:
        return response_error(captcha_result[1])

    teachers = Teacher.select().where(Teacher.username == username)
    for teacher in teachers:
        return response_error('already_exists')

    teacher = Teacher(username=username, fullname=fullname, email=email, active=True, superuser=False)
    teacher.set_password(password)
    teacher.save()

    return response_success()

def check_captcha(request):
    """Checks captcha from request. Returns (result:Boolean, error:String)."""
    
    if not IS_CAPTCHA_ENABLED:
        return (True, None)
    
    captcha_challenge = request.form.get('recaptcha_challenge_field', None)
    captcha_solution = request.form.get('recaptcha_response_field', None)
    try:
        is_correct = captcha.is_solution_correct(captcha_solution, captcha_challenge, request.remote_addr)
    except recaptcha.RecaptchaException as ex:
        return (False, 'internal_error')
    
    if is_correct:
        return (True, None)
    else:
        return (False, 'captcha_incorrect')

def random_public_id():
    while True:
        pubid = "".join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)])

        qions = Questionnaire.select().where(Questionnaire.public_id == pubid)
        for qion in qions:
            break
        else:
            return pubid

@teacher.route('/new-questionnaire/', methods=['POST'])
@auth.login_required
def new_questionnaire():
    user = auth.get_logged_in_user()

    name = request.form['name']
    category_id = request.form['category_id']
    public_id = request.form.get('public_id')

    if not public_id:
        public_id = random_public_id()

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
        qions = Question.select().where(Question.questionnaire == qaire)

        for qion in qions:
            Question.delete().where(Question.id == qion.id).execute()

        if Questionnaire.delete().where(Questionnaire.id == qaire.id).execute():
            return response_success()
        else:
            return response_error('questionnaire_not_found')

        break

    return response_error('questionnaire_not_found')


# TODO
@teacher.route('/new-question/', methods=['POST'])
@auth.login_required
def new_question():
    user = auth.get_logged_in_user()

    description = request.form['description']
    typ = request.form['type']
    presented = request.form['presented']
    public_id = request.form['public_id']

    ret = {}

    qaires = Questionnaire.select().join(Category).where(Category.teacher == user).where(Questionnaire.public_id == public_id)

    for qaire in qaires:
        if Question.create(description=description, typ=typ, presented=presented, questionnaire=qaire):
            return response_success()
        else:
            return response_error('internal_error')

        break


    return response_error('questionnaire_not_found')

@teacher.route('/remove-question/', methods=['POST'])
@auth.login_required
def remove_question():
    user = auth.get_logged_in_user()
    question_id = request.form['question_id']

    qions = Question.select().join(Questionnaire).join(Category).where(Category.teacher == user).where(Question.id == question_id)

    for qion in qions:
        qion.delete_instance()
        return response_success()

    return response_error('question_not_found')

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
        opt.delete_instance()
        return response_success()

    return response_error('option_not_found')


# TODO
@teacher.route('/settings/', methods=['POST'])
@auth.login_required
def settings():
    pass

# TODO
@teacher.route('/results/<qaire_id>/', methods=['POST'])
@auth.login_required
def results(qaire_id):
    pass

