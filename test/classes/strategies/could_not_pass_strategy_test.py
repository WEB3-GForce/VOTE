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
from src.classes.decision import Decision
from src.classes.stance import Stance
from src.classes.member import Member
from src.classes.data.vote_tally import VoteTally
from src.classes.strategies.could_not_pass_strategy import CouldNotPassStrategy
from src.constants import outcomes

class CouldNotPassStrategyTest(unittest.TestCase):
    """ Test suite for could_not_pass_strategy.py."""

    def setUp(self):
        self.decision = Decision()
        self.member = Member()
        self.bill = Bill()
        self.strategy = CouldNotPassStrategy(self.decision, self.member, self.bill)

        self.stance = Stance()
        self.stance.issue = "Some Issue"
        self.stance.side = outcomes.FOR

        self.stance1 = Stance()
        self.stance1.issue = "Some Other Issue"
        self.stance1.side = outcomes.AGN

    def test_init(self):
        """Tests whether a strategy can be constructed properly"""
        result = CouldNotPassStrategy(self.decision, self.member, self.bill)

        self.assertEqual(result._name, "Could Not Pass")
        self.assertEqual(result._decision, self.decision)
        self.assertEqual(result._member, self.member)
        self.assertEqual(result._bill, self.bill)
        self.assertEqual(result._success, False)

    def test_run_fail_no_majority(self):
        """ Verifies that run() fails if there is no majority"""
        self.bill.vote_tally = VoteTally()
        self.bill.vote_tally.agn_votes = 1 + (self.strategy._NOT_PASS_RATIO * 100)
        self.bill.vote_tally.for_votes = 100
        self.decision.for_stances = [self.stance]
        self.decision.agn_stances = [self.stance1]
        result = self.strategy.run()

        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)

    def test_run_fail_bill_could_pass(self):
        """ Verifies that run() fails if the bill could pass"""
        self.bill.vote_tally = VoteTally()
        self.bill.vote_tally.agn_votes = (self.strategy._NOT_PASS_RATIO * 100)
        self.bill.vote_tally.for_votes = 100
        self.decision.for_stances = [self.stance]
        self.decision.agn_stances = [self.stance1, self.stance1]
        result = self.strategy.run()

        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)

    def test_run_fail_no_vote_tally(self):
        """ Verifies that run() fails if there is no VoteTally object"""
        self.decision.for_stances = [self.stance]
        self.decision.agn_stances = [self.stance1, self.stance1]
        result = self.strategy.run()

        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)

    def test_run_success_FOR(self):
        """ Verifies that run() fails if there is a majority for"""
        self.bill.vote_tally = VoteTally()
        self.bill.vote_tally.agn_votes = 1 + (self.strategy._NOT_PASS_RATIO * 100)
        self.bill.vote_tally.for_votes = 100

        self.decision.for_stances = [self.stance, self.stance]
        self.decision.agn_stances = [self.stance1]
        result = self.strategy.run()

        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)

    def test_run_success(self):
        """ Verifies that run() succeeds if the bill could not pass"""
        self.bill.vote_tally = VoteTally()
        self.bill.vote_tally.agn_votes = 1 + (self.strategy._NOT_PASS_RATIO * 100)
        self.bill.vote_tally.for_votes = 100
        self.decision.for_stances = [self.stance]
        self.decision.agn_stances = [self.stance1, self.stance1]
        result = self.strategy.run()

        self.assertTrue(result)
        self.assertTrue(self.strategy._success)
        self.assertEquals(self.decision.result, outcomes.AGN)
        self.assertEquals(self.decision.reason, self.decision.agn_stances)

    def test_explain(self):
        """ Verifies explain runs if there is a success [aka _explain is implemented]."""
        self.bill.vote_tally = VoteTally()
        self.bill.vote_tally.agn_votes = 1 + (self.strategy._NOT_PASS_RATIO * 100)
        self.bill.vote_tally.for_votes = 100
        self.decision.for_stances = [self.stance]
        self.decision.agn_stances = [self.stance1, self.stance1]
        result = self.strategy.run()

        self.assertTrue(result)

        self.strategy.explain()
