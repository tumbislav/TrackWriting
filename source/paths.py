# encoding: utf-8
# author: Marko Čibej
# file: paths.py
"""
Temporary collection of Flask-related stuff. To be refactored.
"""

import json
from flask import Flask, render_template, request
from database import Database
from helper import FILE_PATH, APP_VERSION, JSON_SOURCE, load_from_json


db = Database(FILE_PATH, APP_VERSION)

app = Flask(__name__)


@app.route('/')
def start_page():
    return render_template('index.html')


@app.route('/diary', methods=['GET', 'POST'])
def update_diary():
    if request.method == 'GET':
        return json.dumps([{'title': w['name'], 'count': w['word-count'], 'new-count': 0} for w in works]), 200, \
                {'ContentType': 'application/json'}
    elif request.method == 'POST':
        return json.dumps(works), 200, {'ContentType': 'application/json'}


@app.route('/import', methods=['GET'])
def import_from_json():
    """
    Reload the model from a new or old file.
    """
    load_from_json(db, JSON_SOURCE)
    return ''


@app.route('/works', methods=['GET'])
def get_works():
    return db.get_works(), 200, {'ContentType': 'application/json'}


@app.route('/classifiers', methods=['GET'])
def get_classifiers():
    return db.get_classifiers(), 200, {'ContentType': 'application/json'}


@app.route('/translations', methods=['GET'])
def get_translations():
    return db.get_translations_for_language(), 200, {'ContentType': 'application/json'}
