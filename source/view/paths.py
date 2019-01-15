# encoding: utf-8
# author: Marko Čibej
# file: paths.py
"""
Temporary collection of Flask-related stuff. To be refactored.
"""

import json
from view import app
from flask import render_template, request

works = [{'title': 'Moby Dick', 'count': 14122, 'change': 12, 'date_changed': 'never'},
         {'title': 'Tricky Dicky', 'count': 14122, 'change': 12, 'date_changed': 'never'},
         {'title': 'Diddly Donnie', 'count': 14122, 'change': 12, 'date_changed': 'never'},
         {'title': 'Likely Dickless', 'count': 14122, 'change': 12, 'date_changed': 'never'},
         {'title': 'Mother Hubbard', 'count': 14122, 'change': 12, 'date_changed': 'never'},
         {'title': 'Open Dock', 'count': 14122, 'change': 12, 'date_changed': 'never'},
         {'title': 'Tick Tock Clock', 'count': 14122, 'change': 12, 'date_changed': 'never'},
         {'title': '"Repent, Batman!" said Harley Quinn', 'count': 14122, 'change': 12, 'date_changed': 'never'},
         {'title': '"Good Bait, man", replied the Count', 'count': 14122, 'change': 12, 'date_changed': 'never'}
         ]


@app.route('/')
def start_page():
    context = {'focus': 'Diary', 'tagline': 'What is happening'}
    return render_template('index.html', title='no workspace', context=context, works=works)


# API
#


@app.route('/diary', methods=['POST'])
def update_diary():
    retval = request.json
    return json.dumps({'change': retval['count']}), 200, {'ContentType': 'application/json'}
