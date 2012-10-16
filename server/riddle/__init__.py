from flask import Flask

from riddle.views.common import common
from riddle.views.student import student
from riddle.views.teacher import teacher

app = Flask(__name__)
app.register_blueprint(common)
app.register_blueprint(student)
app.register_blueprint(teacher)
