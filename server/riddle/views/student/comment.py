from riddle.views.student import student
from riddle.views.helpers import *
from riddle.models.Questionnaire import Questionnaire
from riddle.models.Comment import Comment
import json
import datetime

@student.route('/submit-comment/', methods=['POST'])
@student_session
def submit_comment():
    student = get_current_student()
    qaire_id = request.form['qaire_id']
    body = request.form['body']

    qaires = Questionnaire.select().where(Questionnaire.id == qaire_id)

    for qaire in qaires:
        Comment.create(author=student.name, body=body, questionnaire=qaire, datetime=datetime.datetime.now())
        return response_success()

    return response_error('questionnaire_not_found')


@student.route('/view-comments/', methods=['POST'])
@student_session
def view_comments():
    student = get_current_student()
    qaire_id = request.form['qaire_id']
    offset = request.form.get('offset')
    limit = 10

    if not offset:
        offset = 0
    else:
        offset = int(offset)

    comments = Comment.select().where(Comment.questionnaire == qaire_id).limit(limit).offset(offset)

    ret = []

    for comment in comments:
        ret.append({'id': comment.id, 'author': comment.author, 'body': comment.body, 'datetime': comment.datetime.isoformat()})

    return json.dumps(ret)
