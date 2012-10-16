from flask import Blueprint, request
import qrcode
import StringIO


common = Blueprint('common', __name__)

@common.route('/')
def show():
    return "Welcome to Riddle, the best page in the universe."

@common.route('/qrcode')
def qr_code():
    output = StringIO.StringIO()
    qrstr = request.args.get('str', '')
    img = qrcode.make(qrstr)
    img.save(output)
    imgdata = output.getvalue()
    output.close()

    headers = {'Content-Type' : 'image/png'}
    return (imgdata, 200, headers);

