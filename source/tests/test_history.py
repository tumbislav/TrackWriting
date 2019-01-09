# encoding: utf-8
# author: Marko Čibej
# file: all_tests.py
"""
Collects all the test files.
"""

import unittest
from model.history import WordCount


class TestWordCount(unittest.TestCase):
    """
    Test the word counter object
    """

    def test_create_from_dict(self):
        history = [('2018-01-01T03:03', 100), ('2018-01-01T03:04', 200), ('2018-01-01T03:05', 150)]
        o = WordCount.from_dict(history)
        self.assertEqual(o.word_count, 150)
        self.assertEqual(o.increase, 200)
        self.assertEqual(o.decrease, 50)
        self.assertTrue(o.consistent)

        o.append(None, 500)
        self.assertEqual(o.word_count, 500)
        self.assertEqual(o.increase, 550)
        o.append('2018-01-01T03:02', 1000)
        self.assertFalse(o.consistent)
        self.assertRaises(ValueError, o.append, *('2018-01-01T03:01', 1000, True))
