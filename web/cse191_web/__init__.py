import flask
app = flask.Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

from . import views
