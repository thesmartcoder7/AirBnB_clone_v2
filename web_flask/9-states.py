#!/usr/bin/python3
"""This script starts a Flask web application."""

# Import necessary modules and classes
from flask import Flask, render_template
from models import storage
from models.state import State
import subprocess

# Create a Flask web application instance
app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    """Render a list of states.

    This function is executed when a request to
    0.0.0.0:/5000/states is made.

    Returns:
        str: HTML template rendered with a list of states.
    """
    state_list = storage.all(State)
    states = []
    for value in state_list.values():
        states.append(value)
    return render_template('9-states.html', states=states, id=None)


@app.route('/states/<id>', strict_slashes=False)
def single_state(id):
    """Render information about a single state.

    This function is executed when a request to
    0.0.0.0:/5000/states/<id> is made.

    Args:
        id (str): The ID of the state to display information about.

    Returns:
        str: HTML template rendered with information about
        the specified state.
    """
    state_list = storage.all(State)
    state = {}
    for key, value in state_list.items():
        if value.id == id:
            state = state_list[key]
    return render_template('9-states.html', id=id, state=state)


@app.teardown_appcontext
def tear_down_context(exception):
    """Remove the current SQLAlchemy Session when the app
    context is torn down."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    subprocess.run(["export", "FLASK_APP=9-states.py"])
    subprocess.run(["flask", "run"])
