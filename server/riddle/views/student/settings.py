from riddle.views.student import student
from riddle.views.helpers import *

@student.route('/get-settings/')
@student_session
def get_settings():
    student = get_current_student()

    return json.dumps({'name': student.name})

@student.route('/set-settings/', methods=['POST'])
@student_session
def set_settings():
    student = get_current_student()
    name = request.form['name']
    student.name = name
    student.save()

    return response_success()
