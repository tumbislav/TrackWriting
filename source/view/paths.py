# encoding: utf-8
# author: Marko Čibej
# file: paths.py
"""
Temporary collection of Flask-related stuff. To be refactored.
"""

import json
from view import app
from flask import render_template, request

with open('c:\\Users\\mcibej\\Work-synced\\Writing\\raw-track.json', encoding='utf-8') as f:
    works = json.load(f)

@app.route('/')
def start_page():
    return render_template('index.html', works=works)


@app.route('/diary', methods=['GET', 'POST'])
def update_diary():
    if request.method == 'GET':
        return json.dumps([{'title': w['name'], 'count': w['word-count'], 'new-count': 0} for w in works]), 200, \
                {'ContentType': 'application/json'}
    elif request.method == 'POST':
        return json.dumps(works), 200, {'ContentType': 'application/json'}


@app.route('/cards', methods=['GET'])
def get_cards():
    return json.dumps(works), 200, {'ContentType': 'application/json'}

@app.route('/all', methods=['GET'])
def get_all():
    return json.dumps(works), 200, {'ContentType': 'application/json'}

