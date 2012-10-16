from flask import Blueprint

teacher = Blueprint('teacher', __name__)

@teacher.route('/qaires')
def show():
    return "Hello! These are your questionnaires: (none)!"

