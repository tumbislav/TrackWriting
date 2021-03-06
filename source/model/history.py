# encoding: utf-8
# author: Marko Čibej
# file: history.py
"""
Objects that implement history of values over time.
"""

import datetime
from typing import List, ClassVar, Union, Any, Tuple


class WithHistory:
    """
    Provides the functionality for keeping the history and current value of an attribute.
    """
    history: List
    consistent: bool
    timezone: datetime.timezone
    latest: datetime.datetime

    def __init__(self):
        self.consistent = True
        self.history = []
        self.timezone = datetime.datetime.utcnow().astimezone().tzinfo

    def append(self, ts: Union[str, datetime.datetime, None], attribute: Any, raise_errors: bool = False):
        """
        Add an attribute value with a timestamp. It the timestamp is empty, the current time is used.
        :param attribute: the attribute value
        :param ts: the datetime object or an ISO string representing it or None for current value
        :param raise_errors: whether errors should abort the append procedure
        """
        if ts is None:
            ts = datetime.datetime.now(self.timezone)
        elif isinstance(ts, str):
            try:
                ts = datetime.datetime.fromisoformat(ts).astimezone(self.timezone)
            except ValueError:
                if raise_errors:
                    raise
                ts = datetime.datetime.now(self.timezone)

        if len(self.history) > 0:
            latest_ts, = self.history[-1]
            if latest_ts > ts:
                if raise_errors:
                    raise ValueError('Timestamp out of order {}'.format(ts.isoformat()))
                else:
                    self.consistent = False

        self.latest = ts
        self.history.append((ts, self.set_current(attribute)))

    def set_current(self, attribute: Any) -> Any:
        """
        In subclasses, this should do any value accumulation or aggregation and posibly modify the attribute,
        then return it.
        """
        raise NotImplemented('Do not call WithHistory directly')

    def reset(self):
        """
        In subclasses, this should reset the initial values of accumulated attributes.
        """
        raise NotImplemented('Do not call WithHistory directly')

    def resequence(self):
        """
        If the history is inconsistent, make it consistent.
        """
        self.history.sort(key=lambda x: x[0])
        self.reset()
        for key, attribute in self.history:
            self.set_current(attribute)
            self.latest = key


class WordCount(WithHistory):
    """
    Track the changing word counts over time for various writing artifacts.
    """
    word_count: int
    increase: int
    decrease: int

    def __init__(self):
        super().__init__()
        self.reset()

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
        for ts_string, word_count in source:
            o.append(ts_string, word_count)

        return o

    def set_current(self, counts: Tuple) -> Tuple:
        """
        Keep track of increases and decreases.
        :param counts: a trio of word count, increase and decrease; only the first is used
        :return: the tuple to be processed
        """
        word_count = counts[0]
        if word_count < self.word_count:
            self.decrease += self.word_count - word_count
        else:
            self.increase += word_count - self.word_count
        self.word_count = word_count

        return self.word_count, self.increase, self.decrease

    def reset(self):
        self.word_count = 0
        self.decrease = 0
        self.increase = 0


class Status(WithHistory):
    """
    Encapsulates status changes.
    """
    status_codes: ClassVar[List]
    default_status: ClassVar[str]

    status: str

    @classmethod
    def configure(cls, statuses: dict):
        cls.status_codes = statuses['codes']
        cls.default_status = statuses['default']

    def __init__(self):
        super().__init__()
        self.reset()

    def set_current(self, status: str) -> str:
        self.status = status
        return status

    def reset(self):
        self.status = self.default_status
