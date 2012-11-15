from flask import Blueprint, request, url_for, render_template
import qrcode
import StringIO
from riddle.models.Questionnaire import Questionnaire

common = Blueprint('common', __name__, static_folder='../static', static_url_path='/static-test')

@common.route('/')
def show():
    return render_template('index.html')
#    return "Welcome to Riddle, the best page in the universe."

@common.route('/qrcode/<qaire_id>/')
def qr_code(qaire_id):
    qaires = Questionnaire.select().where(Questionnaire.public_id == qaire_id)

    qrstr = ''
    for qaire in qaires:
        qrstr = url_for('student.show', qaire_id=qaire.public_id, _external=True)
        break

    output = StringIO.StringIO()
    img = qrcode.make(qrstr)
    img.save(output)
    imgdata = output.getvalue()
    output.close()

    headers = {'Content-Type' : 'image/png'}
    return (imgdata, 200, headers);

