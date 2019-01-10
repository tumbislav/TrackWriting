# encoding: utf-8
# author: Marko Čibej
# file: paths.py
"""
Temporary collection of Flask-related stuff. To be refactored.
"""

from view import app
from flask import render_template


@app.route('/')
def hello_world():
    context = {'focus': 'Diary', 'tagline': 'What is happening'}
    return render_template('index.html', title='no workspace', context=context)
