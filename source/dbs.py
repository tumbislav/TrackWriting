# encoding: utf-8
# author: Marko Čibej
# file: dbs.py
"""
Wraps a single database and exposes only those operations that we need.
"""

import json
import os
import sqlite3
from typing import List


_CREATE_TABLES = '''
    create table works (
        id integer primary key, 
        work text not null
    );
    create table history (
        id integer primary key, 
        work text not null
    );
'''


con: sqlite3.Connection


def open_db(file_name: str):
    """
    Opens or creates a database. This class only wraps a single database, so if one is already open,
    this method raises an exception.
    :param file_name: the file to use
    """
    if con is not None:
        raise Exception('Attempting to open a database when one is already open.')
    db_exists = os.path.isfile(file_name)
    con = sqlite3.connect(file_name)
    if not db_exists:
        initialize()


def close():
    """
    Flushes and closes the opened database.
    """
    global _con
    if _con is None:
        raise Exception('No database is open.')
    _con.commit()
    _con.close()
    _con = None


def initialize():
    """
    Creates the database structure.
    """
    cursor = _con.cursor()
    cursor.execute('create table works (id integer PRIMARY KEY, work text NOT NULL)')
    cursor.execute('create table history (id integer PRIMARY KEY, work text NOT NULL)')


def dump_to_sqlite():
    with open('c:/Users/mcibej/Work-synced/Writing/raw-track.json', 'r') as f:
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
