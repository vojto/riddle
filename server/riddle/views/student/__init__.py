from flask import Blueprint

student = Blueprint('student', __name__)

from .settings import *
from .comment import *
from .misc import *
