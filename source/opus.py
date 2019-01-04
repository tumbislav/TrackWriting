# encoding: utf-8
# author: Marko Čibej
"""
Main writing entities for the TrackWriting package.
"""

import datetime
from typing import List, ClassVar


class OpusVersion:
    """
    Abstracts a version of a work that can be distributed across a number of files.
    """
    version_types: ClassVar[List] = ['working', 'publication']

    description: str
    name: str
    work_files: List
    opened: datetime.date
    closed: datetime.date
    version_type: str
    word_count: int
    language: str

    def __init__(self, json_source: dict=None):
        pass

class Status:
    """
    Encapsulates a status change.
    """
    status_code: str
    valid_from: datetime.date
    valid_to: datetime.date

    def __init__(self, code: str, start: datetime.date, end: datetime.date):
        self.status_code = code
        self.valid_from = start
        self.valid_to = end


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


class Classifier:
    pass

class Genre(Classifier):
    pass


class Opida:
    """
    A collection of opuses. Not a collection of opi.
    """
    name: str
    parts: List[Opus]

