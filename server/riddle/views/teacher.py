from flask import Blueprint, request
from riddle import app, auth
from riddle.models.Teacher import Teacher
from riddle.models.Questionnaire import Questionnaire
from riddle.models.Category import Category 
import json
import recaptcha

IS_CAPTCHA_ENABLED = False

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
    email    = request.form['email']
    ret = {}

    captcha_result = check_captcha(request)
    if captcha_result[0] == False:
        return json.dumps({'response': 'error', 'reason': captcha_result[1]})

    teachers = Teacher.select().where(Teacher.username == username)
    for teacher in teachers:
        ret['response'] = 'error'
        ret['reason'] = 'already_exists'
        return json.dumps(ret)

    teacher = Teacher(username=username, fullname=fullname, email=email, active=True, superuser=False)
    teacher.set_password(password)
    teacher.save()

    ret['response'] = 'success'
    return json.dumps(ret)

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

# TODO
@teacher.route('/new-questionnaire/', methods=['POST'])
@auth.login_required
def new_questionnaire():
    pass

# TODO
@teacher.route('/new-question/', methods=['POST'])
@auth.login_required
def new_question():
    pass

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

