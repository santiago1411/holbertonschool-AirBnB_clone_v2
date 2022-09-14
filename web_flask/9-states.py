#!/usr/bin/python3
"""
States and State
"""
from models import storage
from flask import Flask
from flask import render_template
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(self):
    """After each request remove current SQLAlchemy session"""
    storage.close()


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def routes(id=None):
    """Function that displays an HTML page"""
    states = storage.all(State)
    if id is not None:
        id = 'State.' + id
    return render_template('9-states.html', states=states, id=id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
