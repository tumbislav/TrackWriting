# encoding: utf-8
# author: Marko Čibej
# file: paths.py
"""
Temporary collection of Flask-related stuff. To be refactored.
"""

from view import app
from flask import render_template

works = [{'title': 'Moby Dick', 'count': 14122, 'change': 12, 'date_changed': 'never' },
         {'title': 'Tricky Dicky', 'count': 14122, 'change': 12, 'date_changed': 'never' },
         {'title': 'Diddly Donnie', 'count': 14122, 'change': 12, 'date_changed': 'never' },
         {'title': 'Likely Dickless', 'count': 14122, 'change': 12, 'date_changed': 'never' },
         {'title': 'Mother Hubbard', 'count': 14122, 'change': 12, 'date_changed': 'never' },
         {'title': 'Open Dock', 'count': 14122, 'change': 12, 'date_changed': 'never' },
         {'title': 'Tick Tock Clock', 'count': 14122, 'change': 12, 'date_changed': 'never' },
         {'title': '"Repent, Batman!" said Harley Quinn', 'count': 14122, 'change': 12, 'date_changed': 'never' },
         {'title': '"Good Bait, man", replied the Count', 'count': 14122, 'change': 12, 'date_changed': 'never' }
         ]


@app.route('/')
def hello_world():
    context = {'focus': 'Diary', 'tagline': 'What is happening'}
    return render_template('index.html', title='no workspace', context=context, works=works)
