from flask import request
from riddle import app, auth
from riddle.views.teacher import teacher
from riddle.views.helpers import *
from riddle.models.Question import Question
from riddle.models.Questionnaire import Questionnaire
from riddle.models.Category import Category
from riddle.models.Option import Option
from riddle.models.Teacher import Teacher
from riddle.models.Comment import Comment
from riddle.models.Answer import Answer
from riddle.models.StudentPresence import StudentPresence

@teacher.route('/status/<qid>/')
def presentation_status(qid):
    """
    For a questionnaire, returns number of connected users and the
    question that is currently presented.
    """
    # TODO: For now we'll just return status for questionnaire
    # In the future, we'll want to check which questionnaire is being presented
    # by user, and return info for that questionnaire

    try:
        questionnaire = Questionnaire.get(Questionnaire.public_id == qid)
    except Questionnaire.DoesNotExist:
        return response_error('not_found')

    count = StudentPresence.count_active(questionnaire)
    question = questionnaire.presented_question()

    return json.dumps({'student_count': count, 'presented_question': question.as_json()})

@teacher.route('/qaires/')
@auth.login_required
def show_qaires():
    user = auth.get_logged_in_user()
    cats = Category.select().join(Teacher).where(Teacher.id == user.id)
    ret = []
    for c in cats:
        ret.append({'id': c.id, 'category': c.name, 'questionnaires': []})
        qaires = Questionnaire.select().join(Category).where(Category.id == c.id)
        for q in qaires:
            ret[-1]['questionnaires'].append({'id': q.id, 'name': q.name, 'public_id': q.public_id})

    return json.dumps(ret)

@teacher.route('/qaires/<qaire_id>/')
@auth.login_required
def show_questions(qaire_id):
    user = auth.get_logged_in_user()
    qaires = Questionnaire.select().join(Category).where(Questionnaire.public_id == qaire_id).where(Category.teacher == user)

    ret = {}

    for qaire in qaires:
        category = Category.select().join(Questionnaire).where(Questionnaire.id == qaire.id)
        questions = Question.select().join(Questionnaire).where(Questionnaire.id == qaire.id)

        catname = ''

        for cat in category:
            catname = cat.name
            break

        ret = {'id': qaire.id, 'public_id': qaire.public_id, 'name': qaire.name, 'category': catname, 'questions' : []}

        for qion in questions:
            qtype = qtype2str(qion.typ)
            ret['questions'].append({'id': qion.id, 'type': qion.typ, 'description': qion.description, 'presented': qion.presented})

            if qtype == 'single' or qtype == 'multi':
                ret['questions'][-1]['options'] = []
                options = Option.select().join(Question).where(Question.id == qion.id)

                for opt in options:
                    ret['questions'][-1]['options'].append({'id': opt.id, 'text': opt.text})

    return json.dumps(ret)

@teacher.route('/remove-comment/', methods=['POST'])
@auth.login_required
def remove_comment():
    user = auth.get_logged_in_user()

    comment_id = request.form['id']

    comments = Comment.select().join(Questionnaire).join(Category).where(Category.teacher == user).where(Comment.id == comment_id)

    for comment in comments:
        comment.delete_instance(recursive=True, delete_nullable=True)
        return response_success()

    return response_error('comment_not_found')

@teacher.route('/results-options/', methods=['POST'])
@auth.login_required
def results_options():
    user = auth.get_logged_in_user()
    question_id = request.form['question_id']

    qions = Question.select().join(Questionnaire).join(Category).where(Category.teacher == user).where(Question.id == question_id)
    for qion in qions:
        strtype = qtype2str(qion.typ)

        ret = {'question_type': strtype, 'question_answers': []}

        if strtype == 'single' or strtype == 'multi':
            opts = Option.select().where(Option.question == qion).annotate(Answer)

            for opt in opts:
                ret['question_answers'].append({'option_id': opt.id, 'option_text': opt.text, 'answers': opt.count})
        else:
            return response_error('wrong_question_type')

        return json.dumps(ret)

    return response_error('question_not_found')

@teacher.route('/results-texts/', methods=['POST'])
@auth.login_required
def results_texts():
    user = auth.get_logged_in_user()
    question_id = request.form['question_id']

    qions = Question.select().join(Questionnaire).join(Category).where(Category.teacher == user).where(Question.id == question_id)

    for qion in qions:
        strtype = qtype2str(qion.typ)

        ret = {'question_type': strtype, 'question_answers': []}

        answers = Answer.select(Answer, Student).where(Answer.question == qion)

        for answer in answers:
            ret['question_answers'].append({'text': answer.text, 'student': answer.student.name, 'id': answer.id})


        return json.dumps(ret)

    return response_error('question_not_found')


