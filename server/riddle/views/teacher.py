from flask import Blueprint, request
from riddle import app, auth
from riddle.models.Teacher import Teacher
from riddle.models.Questionnaire import Questionnaire
from riddle.models.Category import Category 
import json
import recaptcha

teacher = Blueprint('teacher', __name__)
captcha = recaptcha.RecaptchaClient(app.config['RECAPTCHA_PRIVATE_KEY'], app.config['RECAPTCHA_PUBLIC_KEY'])

@teacher.route('/qaires/')
@auth.login_required
def show():
    user = auth.get_logged_in_user()
    cats = Category.select().join(Teacher).where(Teacher.id == user.id)
    ret = []
    for c in cats:
        ret.append({'category': c.name, 'questionnaires': []})
        qaires = Questionnaire.select().join(Category).where(Category.id == c.id)
        for q in qaires:
            ret[-1]['questionnaires'].append({'name': q.name, 'public_id': q.public_id})

    return json.dumps(ret)

@teacher.route('/new-category/', methods = ['POST'])
@auth.login_required
def add():
    user = auth.get_logged_in_user()
    name = request.form['name']
    cats = Category.select().join(Teacher).where(Teacher.id == user.id).where(Category.name == name);
    ret = {}

    for c in cats:
        ret['response'] = 'error'
        ret['reason'] = 'already_exists'
        return json.dumps(ret)


    Category.insert(name=name, teacher=user).execute()

    ret['response'] = 'success'

    return json.dumps(ret)


@teacher.route('/login/', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    teacher = auth.authenticate(username, password)

    ret = {}

    if teacher == False:
        ret['response'] = 'error'
        ret['reason'] = 'wrong_password'
    else:
        auth.login_user(teacher)
        ret['response'] = 'success'

    return json.dumps(ret)

@teacher.route('/logout/')
@auth.login_required
def logout():
    auth.logout_user(auth.get_logged_in_user())

    ret = {}
    ret['response'] = 'success'

    return json.dumps(ret)

@teacher.route('/registration/', methods=['POST'])
def registration():
    username = request.form['username']
    fullname = request.form['fullname']
    password = request.form['password']
    captcha_challenge = request.form['recaptcha_challenge_field']
    captcha_solution = request.form['recaptcha_response_field']

    teachers = Teacher.select().where(Teacher.username == username)

    ret = {}

    try:
        if not captcha.is_solution_correct(captcha_solution, captcha_challenge, request.remote_addr):
            ret['response'] = 'error'
            ret['reason'] = 'captcha_incorrect'
            return json.dumps(ret)
    except recaptcha.RecaptchaException as ex:
        ret['response'] = 'error'
        ret['reason'] = 'internal_error'
        return json.dumps(ret)

    for teacher in teachers:
        ret['response'] = 'error'
        ret['reason'] = 'already_exists'
        return json.dumps(ret)

    teacher = Teacher(username=username, fullname=fullname, active=True, superuser=False)
    teacher.set_password(password)
    teacher.save()

    ret['response'] = 'success'
    return json.dumps(ret)

