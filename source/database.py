# encoding: utf-8
# author: Marko Čibej
# file: database.py
"""
Wraps a single database and exposes the operations that we need.
"""

import json
import os
import sqlite3
import sql
from typing import Iterable, Optional


def json_list(i: Iterable) -> str:
    """
    Take an iterable that returns tuples where the first element is a json string. Such as the
    result of fetchall, to take a random example. Return a comma-separated string bracketed by [ and ]
    :param i: the iterable
    :return: the json string
    """
    return ','.join([tpl[0] for tpl in i]).join(['[', ']'])


class Database:
    """
    The database object. Opens a database on creation, but the caller should close it.
    No context handler implemented, because it's meant to remain active in its thread while the app is running.
    """
    con: sqlite3.Connection
    app_version: str

    def __init__(self, file_name: str, app_version: str, auto_upgrade: bool = True):
        """
        Open or create a database.
        :param file_name: the file to use
        :param app_version: the version of the app
        :param auto_upgrade: whether to upgrade the database automatically; overriden when the database is new
        """
        self.app_version = app_version
        new_db = not os.path.isfile(file_name)
        self.con = sqlite3.connect(file_name, check_same_thread=False)
        if auto_upgrade or new_db:
            self.upgrade_db()

    def close_db(self):
        """
        Flushe and close the opened database.
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
            cur.execute(sql.update_db_version, {'db_version': target_version, 'app_version': self.app_version})
            self.con.commit()
            current_version = target_version

    def insert_work(self, work: dict, commit: bool = True) -> int:
        """
        Parse a dict that represents a work and insert it into the table.
        :param work: the dict that represents the work
        :param commit: whether or not to commit automatically
        :return: the row ID of the inserted row
        """
        cursor = self.con.execute(sql.insert_work,
                                  {'code': work['code'],
                                   'name': work['name'],
                                   'parent': work['parent'],
                                   'json': json.dumps(work)})
        if commit:
            self.con.commit()
        return cursor.lastrowid

    def update_work(self, work: dict):
        self.con.execute(sql.update_work, {'code': work['code'], 'json': json.dumps(work)})
        self.con.commit()

    def get_works(self) -> str:
        """
        Retrieve the full list of works.
        :return: a json string with the selected works
        """
        return json_list(self.con.execute(sql.get_works).fetchall())

    def insert_classifier(self, classifier: dict, commit: bool = True) -> int:
        """
        Parse a dict that represents a classifier and insert it into the table.
        :param classifier: the classifier dict
        :param commit: whether or not to commit automatically
        :return: the relevant rowid
        """
        cursor = self.con.execute(sql.insert_classifier,
                                  {'name': classifier['name'],
                                   'json': json.dumps(classifier)})
        if commit:
            self.con.commit()
        return cursor.lastrowid

    def get_classifiers(self) -> str:
        """
        Retrieve all the classifiers.
        :return: a json string with the classifiers
        """
        return json_list(self.con.execute(sql.get_classifiers).fetchall())

    def set_translation(self, language: str, context: str, key: str, value: str, commit: bool = True) -> Optional[int]:
        """
        Insert, update or delete a translation. If the triplet language/context/key already exists,
        the value is updated. If value is None, the row is deleted. Otherwise, a new row is inserted.
        :param language: the language key
        :param context: the context key
        :param key: the key key
        :param value: the value
        :param commit: whether to commit
        :return: the relevant rowid
        """
        selector = {'language': language, 'context': context, 'key': key}
        exists = self.con.execute(sql.get_translation, selector).fetchone() is not None
        if value is None:
            if exists:
                self.con.execute(sql.delete_translation, selector)
            return None
        else:
            selector['value'] = value
            if exists:
                cursor = self.con.execute(sql.update_translation, selector)
            else:
                cursor = self.con.execute(sql.insert_translation, selector)
        if commit:
            self.con.commit()
        return cursor.lastrowid

    def get_translations_for_language(self, pattern: str = None) -> str:
        """
        Retrieve all translations for a set of languages that match the pattern, or for all languages.
        :param pattern: the pattern, in sql wildcard format, e.g. en_% for all non-default English
        :return: a json string of all the translations
        """
        cursor = self.con.execute(sql.get_translations, {'language_pattern': pattern or '%'})
        all_langs = {}
        language_name = context_name = None
        current_language = current_context = None
        for row in cursor.fetchall():
            if language_name is None or row[0] != language_name:
                current_context = None
                context_name = None
                language_name = row[0]
                current_language = {}
                all_langs[language_name] = current_language
            if context_name is None or row[1] != context_name:
                context_name = row[1]
                current_context = {}
                current_language[context_name] = current_context
            current_context[row[2]] = row[3]
        return json.dumps(all_langs)

    def set_history(self, work_code: str, timestamp: str,
                    attribute: str, value: str, commit: bool = True) -> Optional[int]:
        """
        Identical logic as set_translation.
        :param work_code: the work to which the history applies
        :param timestamp: when the value changed
        :param attribute: the attribute that changed
        :param value: the attribute's value
        :param commit: whether to commit
        :return: the relevant rowid
        """
        selector = {'work_code': work_code, 'timestamp': timestamp, 'attribute': attribute}
        exists = self.con.execute(sql.get_history, selector).fetchone() is not None
        if value is None:
            if exists:
                self.con.execute(sql.delete_history, selector)
            return None
        else:
            selector['value'] = value
            if exists:
                cursor = self.con.execute(sql.update_history, selector)
            else:
                cursor = self.con.execute(sql.insert_history, selector)
        if commit:
            self.con.commit()
        return cursor.lastrowid
