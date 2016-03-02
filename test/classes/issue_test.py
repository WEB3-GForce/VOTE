"""
    VOTE - A decision program for predicting votes in Congress.
    Copyright (C) 2016 William Edward Bailey, III (WEB3 or WEBIII):
      https://github.com/WEB3-GForce
    Based on Stephen Slade's Ph.D Thesis:
      zoo.cs.yale.edu/classes/cs458/materials/RealisticRationality.pdf

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import unittest

from src.classes.issue import Issue

class IssueTest(unittest.TestCase):
    """ Test suite for Issue."""

    def setUp(self):
        # This is fake data. Do not use it to make assumptions about how
        # data will look in the actual system.
        self.input_hash = {"con_stances": ["Something"],
            "number": "Plural",
            "synonyms": ["Powerful"],
            "polarity": "A meaningful description",
            "type": "A type",
            "norm": "Some norm",
            "opposite": "The opposite issue",
            "pro_english_description": "Something good",
            "pro_stances": ["Some pro stance"],
            "con_english_description": "something bad",
            "name": "A notable issue",
            "isa": ["Issue"]}

    def test_init_default(self):
        """Tests that default values are set for instance variables"""
        issue = Issue()

        self.assertEqual(issue.name, "")
        self.assertEqual(issue.number, "")
        self.assertEqual(issue.type, "")
        self.assertEqual(issue.isa, [])
        self.assertEqual(issue.synonyms, [])
        self.assertEqual(issue.opposite, [])
        self.assertEqual(issue.polarity, "")
        self.assertEqual(issue.pro_english_description, "")
        self.assertEqual(issue.con_english_description, "")

        self.assertEqual(issue.pro_stances, [])
        self.assertEqual(issue.con_stances, [])
        self.assertEqual(issue.norm, None)

    def test_init_hash(self):
        """ Verifies that input data from a hash is properly set."""
        issue = Issue(self.input_hash)
        for key, value in self.input_hash.iteritems():
            self.assertEqual(value, issue.__dict__[key])

    def test_init_hash_default(self):
        """ Verifies defaults are still defined when a hash is provided."""
        self.input_hash.pop("name")
        issue = Issue(self.input_hash)
        for key, value in self.input_hash.iteritems():
            self.assertEqual(value, issue.__dict__[key])
        self.assertEqual(issue.name, "")
