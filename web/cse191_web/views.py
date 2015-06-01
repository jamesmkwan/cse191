import flask

from . import app
from . import util
from . import problems

default_code = 'print("Hello world!")'
@app.route('/')
def list_problems():
    return flask.render_template('problems.html', problems=problems.list_problems())

@app.route('/s', methods=['GET', 'POST'])
def free_run():
    if flask.request.method == 'POST':
        _, result = util.run_code(flask.request.form['code'])
    else:
        result = None
    return flask.render_template('free.html', result=result, code=flask.request.form.get('code', default_code))

@app.route('/q/<question>', methods=['GET', 'POST'])
def test_run(question):
    try:
        problem = problems.find_problem(question)
    except KeyError:
        flask.abort(404)

    code = flask.request.form.get('code', problem.starter_code)

    if flask.request.form.get('action', 'grade') == 'reset_grade':
        grader = problem.grader_code
    else:
        grader = flask.request.form.get('grader', problem.grader_code)

    if flask.request.method == 'POST':
        grade, debug = util.grade_code(code, grader)
    else:
        grade = None
        debug = None
    return flask.render_template('grade.html', instructions=problem.prompt, grade=grade, debug_=debug, code=code, grader=grader, name=problem.name)
