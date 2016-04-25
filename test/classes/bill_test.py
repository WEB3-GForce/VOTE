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

from src.classes.bill import Bill

class BillTest(unittest.TestCase):
    """ Test suite for Bill."""

    def setUp(self):
        # This is fake data. Do not use it to make assumptions about how
        # data will look in the actual system.
        self.input_hash = {"synonyms": ["DEFENSE-AUTHORIZATION"],
            "session": "100",
            "vote_tally": "Vote Tally Object",
            "stance_agn": ["Some Stances"],
            "issues": ["DEFENSE", "CHEMICAL-WEAPONS"],
            "bill_number": "AMD",
            "date_of_vote": "Monday, May 18, 1987",
            "sort_key": None,
            "inferred_stance_agn": ["Some I stances"],
            "importance": "C",
            "stance_for": ["Some For stances"],
            "inferred_stance_for": ["Some I for stances"],
            "majority_factor": None,
            "name": "Defense Authorization, Fiscal 1988 / Chemical Weapons",
            "president_position": "AGN",
            "notes": ["Note 1"]}

    def test_init_default(self):
        """Tests that default values are set for instance variables"""
        bill = Bill()

        self.assertEqual(bill.bill_number, "")
        self.assertEqual(bill.name, "")
        self.assertEqual(bill.synonyms, [])
        self.assertEqual(bill.importance, None)
        self.assertEqual(bill.session, "")
        self.assertEqual(bill.majority_factor, None)
        self.assertEqual(bill.date_of_vote, None)

        self.assertEqual(bill.vote_tally, None)
        self.assertEqual(bill.president_position, None)
        self.assertEqual(bill.sort_key, None)

        self.assertEqual(bill.issues, [])
        self.assertEqual(bill.stances_for, [])
        self.assertEqual(bill.stances_agn, [])
        self.assertEqual(bill.inferred_stances_for, [])
        self.assertEqual(bill.inferred_stances_agn, [])

    def test_init_hash(self):
        """ Verifies that input data from a hash is properly set."""
        bill = Bill(self.input_hash)
        for key, value in self.input_hash.iteritems():
            self.assertEqual(value, bill.__dict__[key])

    def test_init_hash_default(self):
        """ Verifies defaults are still defined when a hash is provided."""
        self.input_hash.pop("bill_number")
        bill = Bill(self.input_hash)
        for key, value in self.input_hash.iteritems():
            self.assertEqual(value, bill.__dict__[key])
        self.assertEqual(bill.bill_number, "")
