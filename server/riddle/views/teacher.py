from flask import Blueprint
from riddle import auth

teacher = Blueprint('teacher', __name__)

@teacher.route('/qaires')
@auth.login_required
def show():
    return "Hello! These are your questionnaires: (none)!"

@teacher.route('/new', methods = ['POST'])
@auth.login_required
def add():
    return "Time to add some cool stuff."

