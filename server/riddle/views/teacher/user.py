from flask import request
from riddle import app, auth
from riddle.views.teacher import teacher
from riddle.views.helpers import check_captcha, random_public_id
from riddle.views.helpers import *
from riddle.models.Teacher import Teacher

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

