# encoding: utf-8
# author: Marko Čibej
# file: database.py
"""
Wraps a single database and exposes only those operations that we need.
"""

import json
import os
import sqlite3
import sql
from helper import APP_VERSION


class Database:

    con: sqlite3.Connection

    def __init__(self, file_name: str, auto_upgrade: bool = True):
        """
        Opens or creates a database.
        :param file_name: the file to use
        :param auto_upgrade: whether to upgrade the database automatically; overriden when the database is new
        """
        new_db = not os.path.isfile(file_name)
        self.con = sqlite3.connect(file_name, check_same_thread=False)
        if auto_upgrade or new_db:
            self.upgrade_db()

    def close_db(self):
        """
        Flushes and closes the opened database.
        """
        if self.con is None:
            raise Exception('No database is open.')
        self.con.commit()
        self.con.close()
        self.con = None

    def clear_db(self):
        """
        Remove all data from the database, with the exception of the meta table.
        """
        self.con.executescript(sql.clear_database)

    def force_commit(self):
        """
        Make sure that everything is committed. Useful if we've been deferring commits for a while.
        """
        self.con.commit()

    def insert_work(self, work: dict, commit: bool = True):
        """
        Parse a dict that represents a work and insert it into the table.
        :param work: the dict that represents the work
        :param commit: whether or not to commit automatically
        """
        self.con.execute(sql.insert_work, {'name': work['name'],
                                           'type': work['work_type'],
                                           'parent': work['parent'],
                                           'last_change': work['last_change'],
                                           'aggregate': work['aggregate'],
                                           'json': json.dumps(work)})
        if commit:
            self.con.commit()

    def insert_classifier(self, classifier: dict, commit: bool = True):
        """
        Parse a dict that represents a classifier and insert it into the table.
        :param classifier: the classifier dict
        :param commit: whether or not to commit automatically
        """
        self.con.execute(sql.insert_classifier, {'name': name, 'json': json.dumps(definition)})
        pass

    def upgrade_db(self):
        """
        Bring the database version up to current.
        """
        cur = self.con.cursor()
        if cur.execute(sql.is_initialized).fetchone() is None:
            current_version = '0.0'
        else:
            current_version = cur.execute(sql.get_db_version).fetchone()[0]
        while current_version in sql.upgrade_db:
            target_version = sql.upgrade_db[current_version]['target-version']
            cur.executescript(sql.upgrade_db[current_version]['ddl'])
            cur.execute(sql.invalidate_db_version)
            cur.execute(sql.update_db_version, {'db_version': target_version, 'app_version': APP_VERSION})
            self.con.commit()
            current_version = target_version

    def get_works(self, depth: int = 0) -> str:
        """
        Retrieve a list of works, from level 0 to depth
        :param depth: the level at which to stop
        :return: a json string with the selected works
        """
        s = ','.join([_[0] for _ in self.con.execute(sql.get_works, {'level': depth}).fetchall()]).join(['[', ']'])
        return s

    def get_classifiers(self) -> str:
        """
        Retrieve all the classifiers.
        :return: a json string with the classifiers
        """
        return '[]'


def load_from_json(db: Database, json_file: str):
    """
    Loads the contents of a json storage file into the database.
    :param json_file: the name of the json file
    :param db: the Database object, connected to an open database
    """
    with open(json_file, 'r') as f:
        d = json.load(f)
    for w in d['works']:
        db.insert_work({'name': w['name'],
                        'world': w['world'],
                        'series': w['series'],
                        'genre': w['genre'],
                        'work_type': w['type'],
                        'status': w['status'],
                        'word_count': w['word_count'],
                        'entry_type': 'work',
                        'last_change': w['history'][-1]['tc'] if 'history' in w else '',
                        'parent': None,
                        'aggregate': False},
                       commit=False)
    for c in d['classifiers'].items():
        db.insert_classifier({'name': c['name'],
                              'active': c['active'],
                              'values': c['values']},
                             commit=False)
    db.force_commit()

