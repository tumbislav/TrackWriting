# encoding: utf-8
# author: Marko Čibej
# file: dbs.py
"""
Database abstraction.
"""

import json
import os
import sqlite3
from typing import List


class Database:
    """
    Wraps a single database and exposes only those operations that we need.
    """
    file_name: str
    con: sqlite3.Connection

    def __init__(self):
        """
        Store the file name if given.
        """
        self.con = None

    def open(self, file_name: str) -> 'Database':
        """
        Opens or creates a database. This class only wraps a single database, so if one is already open,
        this method raises an exception.
        :param file_name: the file to use
        :return: self
        """
        if self.con is not None:
            raise Exception('Attempting to open a database when one is already open.')
        self.file_name = file_name
        db_exists = os.path.isfile(file_name)
        self.con = sqlite3.connect(self.file_name)
        if not db_exists:
            self.initialize()
        return self

    def close(self):
        """
        Flushes and closes the opened database.
        """
        if self.con is None:
            raise Exception('No database is open.')
        self.con.commit()
        self.con.close()
        self.con = None

    def initialize(self):
        """
        Creates the database structure.
        """
        cursor = self.con.cursor()
        cursor.execute('create table works (id integer PRIMARY KEY, work text NOT NULL)')
        cursor.execute('create table history (id integer PRIMARY KEY, work text NOT NULL)')


def dump_to_sqlite():
    with open(r'c:\Users\mcibej\Work-synced\Writing\raw-track.json', 'r') as f:
        d = json.load(f)
    con = sqlite3.connect(r'c:\Users\mcibej\Work-synced\Writing\db.sqlite3')
    cursor = con.cursor()
    cursor.execute('create table works (id integer PRIMARY KEY, work text NOT NULL)')
    insert_sql = 'INSERT INTO works (work) VALUES (?)'
    for w in d['works']:
        cursor.execute(insert_sql, (json.dumps({'name': w['name'],
                                                'world': w['world'],
                                                'series': w['series'],
                                                'genre': w['genre'],
                                                'type': w['type'],
                                                'status': w['status'],
                                                'word_count': w['word_count']}),))
    con.commit()
