from flask import Blueprint
from riddle import app
import recaptcha

teacher = Blueprint('teacher', __name__)
captcha = recaptcha.RecaptchaClient(app.config['RECAPTCHA_PRIVATE_KEY'], app.config['RECAPTCHA_PUBLIC_KEY'])

from .user import *
from .category import *
from .questionnaire import *
from .question import *
from .option import *
from .misc import *
