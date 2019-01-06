# encoding: utf-8
# author: Marko Čibej
# file: model.py
"""
Main writing entities for the TrackWriting package.
"""

import datetime
from typing import List, ClassVar


class Status:
    """
    Encapsulates a status change.
    """
    codes: ClassVar[List] = ['idea', 'outlining', ' researching', 'writing', 'on hold',
                             'needs review' 'reviewing', 'done', 'abandoned']

    status_code: str
    valid_from: datetime.date
    valid_to: datetime.date

    def __init__(self, code: str, start: datetime.date, end: datetime.date):
        self.status_code = code
        self.valid_from = start
        self.valid_to = end


class WordCount:
    """
    Track the changing word counts over time for various writing artifacts.
    """
    word_count: int
    increase: int
    decrease: int
    history: List
    consistent: bool
    timezone: datetime.timezone

    def __init__(self):
        self.word_count = 0
        self.decrease = 0
        self.increase = 0
        self.consistent = True
        self.history = []
        self.timezone = datetime.datetime.utcnow().astimezone().tzinfo

    @classmethod
    def from_dict(cls, source: List):
        """
        We should receive a list of tuples containing the history of word counts.
        Timestamps should be in ISO 8601 format. Incoming times must be ordered, and all the times must be
        earlier than current.
        :param source: the list of historical values
        :return: whether the load produced any errors
        """
        o = WordCount()
        last_ts = None
        now = datetime.datetime.now(o.timezone)
        for ts_string, word_count in source:
            ts = datetime.datetime.fromisoformat(ts_string)
            if last_ts is not None and ts < last_ts or ts > now:  # take note of errors, but keep going
                o.consistent = False
            last_ts = ts
            if word_count < o.word_count:
                o.decrease += o.word_count - word_count
            else:
                o.increase += word_count - o.word_count
            o.word_count = word_count
            o.history.append((ts, o.word_count, o.increase, o.decrease))

        return o

    def append(self, word_count: int, ts_string: str=None, ts: datetime.datetime=None):
        """
        Add a word count with an optional timestamp. It the timestamp is empty, the current time is used.
        :param word_count: the current word count
        :param ts_string: string containing the timestamp
        :param ts: the datetime object
        :return:
        """
        if ts is None:
            if ts_string is None:
                ts = datetime.datetime.now(self.timezone)
            else:
                ts = datetime.datetime.fromisoformat(ts_string)

        if word_count < self.word_count:
            self.decrease += self.word_count - word_count
        else:
            self.increase += word_count - self.word_count
        self.word_count = word_count
        self.history.append((ts, self.word_count, self.increase, self.decrease))


class TextFile:
    """
    A file in which a part is (being) written.
    """
    name: str
    description: str
    primary_location: str
    other_locations: List[str]
    status: Status
    word_count: WordCount

    def __init__(self, name: str, location: str=None):
        self.name = name
        self.primary_location = location
        self.word_counts = []

    def set_word_count(self, word_count: int, valid_from: datetime.datetime=None):
        """
        Set the current word count
        :param count: the active number of words
        :param valid_from: the timestamp for the time of validity; if none is given, use the system time
        """
        if valid_from is None:
            valid_from = datetime.datetime.now()
        if len(self.word_counts) > 0 and self.word_counts[-1][0] > valid_from:
            raise Exception('Cannot insert a word count with an earlier date')

        self.word_counts.append(valid_from, word_count)
        self.word_count = word_count


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

