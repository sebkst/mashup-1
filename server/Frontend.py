from flask import Flask, request, send_from_directory, redirect, url_for, render_template

#Instantiate app
#application = Flask(__name__, static_url_path='/',template_folder='../app')
application = Flask(__name__,template_folder='../app')

application.debug = True

"""
@application.route("/<path:path>")
def index(path):
    return send_from_directory('../ui/app', path)
"""

@application.route('/')
def root():
    return render_template('index.html')
