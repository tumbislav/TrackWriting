# encoding: utf-8
# author: Marko Čibej
# file: model.py
"""
Main writing entities for the TrackWriting package.
"""

import datetime
from typing import List, ClassVar
from model.history import WordCount, Status


class ManuscriptFile:
    """
    A file in which a part is (being) written.
    """
    name: str
    description: str
    primary_location: str
    other_locations: List[str]
    status: Status
    word_count: WordCount

    def __init__(self, name: str, location: str = None):
        self.name = name
        self.primary_location = location


class OpusVersion:
    """
    Abstracts a version of a work that can be distributed across a number of files.
    """
    version_intents: ClassVar[List] = ['working', 'publication']

    description: str
    name: str
    work_files: List
    opened: datetime.date
    closed: datetime.date
    version_intent: str
    word_count: int
    language: str

    def __init__(self, json_source: dict=None):
        pass

    def add_file(self, file_name):
        pass


class Opus:
    """
    Abstracts a work that can have several versions.
    """
    name: str
    word_count: int
    begun_on: datetime.date
    status: str
    status_changes: List
    versions: List[OpusVersion]
    is_new: bool

    def __init__(self, json_source: dict=None):
        if json_source is not None:
            self.name = json_source['name']
            self.word_count = json_source['word-count']
            self.begun = json_source['begun-on']
            self.status_changes = [Status(stat['status'], stat['valid-from'], stat['valid-to'])
                                   for stat in json_source['status-changes']]
            self.status = self.status_changes[-1].status_code
            self.versions = [OpusVersion(ver) for ver in json_source['versions']]
            self.is_new = False
        else:
            self.name = None
            self.word_count = 0
            self.begun = datetime.date.today()
            self.status_changes = []
            self.status = None
            self.versions = []
            self.is_new = True


class Opera:
    """
    Neither a collection of opuses nor a collection of opi.
    """
    name: str
    parts: List[Opus]

