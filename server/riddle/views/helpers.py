from flask import request, make_response, g
from riddle.models.Student import Student
from riddle.models.Question import Question
from riddle.models.Questionnaire import Questionnaire
import json
import datetime
import functools
import random
import string

def response_success(json_format=True):
    ret = {'response': 'success'}

    if json_format:
        return json.dumps(ret)

    return ret

def response_error(reason=None, json_format=True):
    ret = {'response': 'error'}

    if reason:
        ret['reason'] = reason

    if json_format:
        return json.dumps(ret)

    return ret

def qtype2str(n):
    for ch in Question.typ.choices:
        if ch[0] == int(n):
            return ch[1]

    return None

def random_student_id():
    while True:
        student_id = "".join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])

        students = Student.select().where(Student.session_id == student_id)
        for student in students:
            break
        else:
            return student_id

def get_create_student():
    student_id = request.cookies.get('student_id')
    student = None

    if student_id:
        students = Student.select().where(Student.session_id == student_id)
        for s in students:
            return (s, False)

    return (Student.create(name="Anonymous", session_id=random_student_id()), True)

def get_current_student():
    return g.student

def student_session(fn):
    @functools.wraps(fn)

    def inner(*args, **kwargs):
        (student, created) = get_create_student()
        g.student = student
        response = make_response(fn(*args, **kwargs))

        if created:
            response.set_cookie('student_id', student.session_id, expires=datetime.datetime(2038, 1, 1))

        return response
    return inner

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

