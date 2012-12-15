from flask import Blueprint, request, url_for, render_template
from peewee import fn
import qrcode
import StringIO
from riddle.views.helpers import *
from riddle.models.Questionnaire import Questionnaire
from riddle.models.Rating import Rating

common = Blueprint('common', __name__, static_folder='../static', static_url_path='/static-test')

@common.route('/')
def show():
    return render_template('index.html')
#    return "Welcome to Riddle, the best page in the universe."

@common.route('/qrcode/')
def qr_code():
    url = request.args.get('url')
    output = StringIO.StringIO()
    img = qrcode.make(url)
    img.save(output)
    imgdata = output.getvalue()
    output.close()

    headers = {'Content-Type' : 'image/png'}
    return (imgdata, 200, headers);

@common.route('/get-ratings/', methods=['POST'])
def get_rating():
    qaire_id = request.form['qaire_id']

    qaires = Questionnaire.select().where(Questionnaire.id == qaire_id)
    for qaire in qaires:
        ratings = Rating.select(Rating, fn.Count(Rating.id).alias('count')).where(Rating.questionnaire == qaire).group_by(Rating.like)
        ret = {'likes': 0, 'dislikes': 0}

        for rating in ratings:
            if rating.like:
                ret['likes'] = rating.count
            else:
                ret['dislikes'] = rating.count

        return json.dumps(ret)

    return response_error('questionnaire_not_found')

