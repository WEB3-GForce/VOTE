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

from src.classes.data.vote_tally import VoteTally
from src.constants import outcomes

class VoteTallyaTest(unittest.TestCase):
    """ Test suite for vote_tally.py."""

    def setUp(self):
        # This is fake data. Do not use it to make assumptions about how
        # data will look in the actual system.
        self.input_hash = {"outcome": "some outcome",
            "for_votes" : 20,
            "agn_votes" : 30,
            "party_votes" : {"Party A" :
                                {outcomes.FOR_VOTES : 15,
                                 outcomes.AGN_VOTES : 15},
                             "Party B" :
                                {outcomes.FOR_VOTES : 5,
                                 outcomes.AGN_VOTES : 15}}
            }

    def test_init_default(self):
        """Tests that default values are set for instance variables"""
        result = VoteTally()

        self.assertEqual(result.outcome, None)
        self.assertEqual(result.for_votes, 0)
        self.assertEqual(result.agn_votes, 0)
        self.assertEqual(result.party_votes, {})

    def test_init_hash(self):
        """ Verifies that input data from a hash is properly set."""
        result = VoteTally(self.input_hash)
        for key, value in self.input_hash.iteritems():
            self.assertEqual(value, result.__dict__[key])
        for key, value in result.__dict__.iteritems():
            self.assertEqual(value, self.input_hash[key])

    def test_init_hash_default(self):
        """ Verifies defaults are still defined when a hash is provided."""
        self.input_hash.pop("party_votes")
        result = VoteTally(self.input_hash)
        for key, value in self.input_hash.iteritems():
            self.assertEqual(value, result.__dict__[key])
        self.assertEqual(result.party_votes, {})

    def test_vote_ratio(self):
        """ Verifies the proper ratio is computed. """
        vote_tally = VoteTally()
        vote_tally.for_votes = 27
        vote_tally.agn_votes = 52

        result = vote_tally.vote_ratio()
        self.assertEqual(result, 27.0 / 52.0)
