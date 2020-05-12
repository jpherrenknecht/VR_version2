""" flask_example.py

    Required packages:
    - flask
    - folium

    Usage:

    Start the flask server by running:

        $ python flask_example.py

    And then head to http://127.0.0.1:5000/ in your browser to see the map displayed

"""


from flask import Flask
app = Flask(__name__)

@app.route('/')

def hello_world():
    return 'Hello, World!'