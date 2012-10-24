from riddle import app
from .common import common
from .student import student
from .teacher import teacher

app.register_blueprint(common)
app.register_blueprint(student)
app.register_blueprint(teacher)
