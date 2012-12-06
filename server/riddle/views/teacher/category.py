from flask import request
from riddle import app, auth
from riddle.views.teacher import teacher
from riddle.views.helpers import *
from riddle.models.Category import Category

@teacher.route('/categories/')
@auth.login_required
def show_categories():
    user = auth.get_logged_in_user()
    cats = Category.select().where(Category.teacher == user)
    ret = []
    for c in cats:
        ret.append({'name': c.name, 'id': c.id})

    return json.dumps(ret)

@teacher.route('/new-category/', methods = ['POST'])
@auth.login_required
def add_category():
    user = auth.get_logged_in_user()
    name = request.form['name']
    cats = Category.select().where(Category.teacher == user).where(Category.name == name);

    for c in cats:
        return response_error('already_exists')

    Category.insert(name=name, teacher=user).execute()

    return response_success()

@teacher.route('/edit-category/', methods = ['POST'])
@auth.login_required
def edit_category():
    user = auth.get_logged_in_user()
    category_id = request.form['id']
    name = request.form['name']

    cats = Category.select().where(Category.teacher == user).where(Category.id == category_id);

    for cat in cats:
        cat.name = name
        cat.save()
        return response_success()

    return response_error('category_not_found')

@teacher.route('/remove-category/', methods = ['POST'])
@auth.login_required
def remove_category():
    user = auth.get_logged_in_user()
    category_id = request.form['id']
    name = request.form['name']

    cats = Category.select().where(Category.teacher == user).where(Category.id == category_id);

    for cat in cats:
        cat.delete_instance(recursive=True, delete_nullable=True)
        return response_success()

    return response_error('category_not_found')

