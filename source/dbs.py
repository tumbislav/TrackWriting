# encoding: utf-8
# author: Marko Čibej
# file: dbs.py
"""
Wraps a single database and exposes only those operations that we need.
"""

import json
import os
import sqlite3
from typing import ClassVar


class Database:
    initialize_sql: ClassVar[str] = '''
        create table works (
            id integer primary key, 
            work text not null
        );
        create table history (
            id integer primary key, 
            history_work integer not null,
            foreign key(history_work) references works(id),
            value_type text,
            timestamp text,
            value text
        );
    '''
    insert_work_sql: ClassVar[str] = 'insert into works (work) values (?)'

    con: sqlite3.Connection

    def open_db(self, file_name: str):
        """
        Opens or creates a database. This class only wraps a single database, so if one is already open,
        this method raises an exception.
        :param file_name: the file to use
        """
        if self.con is not None:
            raise Exception('Attempting to open a database when one is already open.')
        db_exists = os.path.isfile(file_name)
        self.con = sqlite3.connect(file_name)
        if not db_exists:
            cursor = self.con.cursor()
            cursor.execute(self.initialize_sql)
            self.con.commit()

    def close_db(self):
        """
        Flushes and closes the opened database.
        """
        if self.con is None:
            raise Exception('No database is open.')
        self.con.commit()
        self.con.close()
        self.con = None

    def load_from_json(self, json_file: str):
        with open(json_file, 'r') as f:
            d = json.load(f)
        cursor = self.con.cursor()
        for w in d['works']:
            cursor.execute(self.insert_work_sql,
                           (json.dumps({'name': w['name'],
                                        'world': w['world'],
                                        'series': w['series'],
                                        'genre': w['genre'],
                                        'type': w['type'],
                                        'status': w['status'],
                                        'word_count': w['word_count']}),))
