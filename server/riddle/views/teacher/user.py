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

    return json.dumps({
        'response': 'success',
        'user': teacher.as_json()
    })

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

@teacher.route('/get-teacher-settings/')
@auth.login_required
def get_teacher_settings():
    user = auth.get_logged_in_user()

    return json.dumps({'username': user.username, 'fullname': user.fullname, 'email': user.email})

@teacher.route('/set-teacher-settings/', methods=['POST'])
@auth.login_required
def set_teacher_settings():
    user = auth.get_logged_in_user()

    fullname = request.form.get('fullname')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    email = request.form.get('email')

    if fullname:
        user.fullname = fullname

    if email:
        user.email = email

    if old_password and new_password:
        u = auth.authenticate(user.username, old_password)
        if not u:
            return response_error('wrong_old_password')

        user.set_password(new_password)

    user.save()

    return response_success()

