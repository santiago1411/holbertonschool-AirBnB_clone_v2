#!/usr/bin/python3
"""script that starts a flask web application"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def web_hello():
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def web_hbnb():
    return "HBNB"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
