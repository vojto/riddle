from flask import Blueprint, request
from riddle import auth
from riddle.models.Teacher import Teacher
from riddle.models.Questionnaire import Questionnaire
from riddle.models.Category import Category 
import json

teacher = Blueprint('teacher', __name__)

@teacher.route('/qaires/')
@auth.login_required
def show():
    user = auth.get_logged_in_user()
    cats = Category.select().join(Teacher).where(Teacher.id == user.id)
    ret = "Hello %s! These are your categories: <br /><br />" % (user.username)
    for c in cats:
        ret += "Category: %s<br />" % (c.name)
        qaires = Questionnaire.select().join(Category).where(Category.id == c.id)
        for q in qaires:
            ret += "Questionnaire: %s<br />" % (q.name)

    return ret

@teacher.route('/new/', methods = ['POST'])
@auth.login_required
def add():
    return "Time to add some cool stuff."


@teacher.route('/login/', methods = ['POST', 'GET'])
def login():
    username = request.form['username']
    password = request.form['password']

    teacher = auth.authenticate(username, password)

    ret = {}

    if teacher == False:
        ret['response'] = 'error'
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

