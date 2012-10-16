from flask import Blueprint

student = Blueprint('student', __name__)

@student.route('/view/<qaire_id>')
def show(qaire_id):
    return "Hello, " + qaire_id + "!"
