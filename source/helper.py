# encoding: utf-8
# author: Marko Čibej
# file: helper.py
"""
Mainly stuff that needs to be loaded laterally.
"""

from database import Database
import json


APP_VERSION = '0.1'
FILES_ROOT = 'c:/Users/marko/Work-synced/Writing/'
# FILES_ROOT = 'c:/Users/mcibej/Work-synced/Writing/'
FILE_PATH = FILES_ROOT + 'test.db'
JSON_SOURCE = FILES_ROOT + 'raw-track.json'


def load_from_json(db: Database, json_file: str):
    """
    Loads the contents of a json storage file into the database.
    :param json_file: the name of the json file
    :param db: the Database object, connected to an open database
    """
    db.clear_db()
    with open(json_file, 'r') as f:
        source = json.load(f)

    for work in source['works']:
        history = [] if 'history' not in work else work['history']
        db.insert_work({'code': work['id'],
                        'name': work['name'],
                        'world': work['world'],
                        'series': work['series'],
                        'genre': work['genre'],
                        'form': work['form'],
                        'status': work['status'],
                        'word_count': work['word_count'],
                        'type': 'work',
                        'last_change': history[-1]['timestamp'] if len(history) > 0 else '',
                        'parent': None,
                        'aggregate': False},
                       commit=False)
        for entry in history:
            db.set_history(work['id'], entry['timestamp'], 'word_count', entry['count'], commit=False)

    for name, classifier in source['classifiers'].items():
        classifier['name'] = name
        db.insert_classifier(classifier, commit=False)

    for language, contexts in source['i18n'].items():
        for context, string_set in contexts.items():
            for key, value in string_set.items():
                db.set_translation(language, context, key, value, commit=False)

    db.force_commit()

