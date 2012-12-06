from flask import request
from riddle import app, auth
from riddle.views.teacher import teacher
from riddle.views.helpers import *
from riddle.models.Question import Question
from riddle.models.Questionnaire import Questionnaire
from riddle.models.Category import Category
from riddle.models.Option import Option
from riddle.models.Teacher import Teacher

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

        ret = {'id': qaire.id, 'name': qaire.name, 'category': catname, 'questions' : []}

        for qion in questions:
            qtype = qtype2str(qion.typ)
            ret['questions'].append({'id': qion.id, 'type': qtype, 'description': qion.description, 'presented': qion.presented})

            if qtype == 'single' or qtype == 'multi':
                ret['questions'][-1]['options'] = []
                options = Option.select().join(Question).where(Question.id == qion.id)

                for opt in options:
                    ret['questions'][-1]['options'].append({'id': opt.id, 'text': opt.text})

    return json.dumps(ret)

