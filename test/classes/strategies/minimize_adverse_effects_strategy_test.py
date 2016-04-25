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
from src.classes.data import importance
from src.classes.strategies.minimize_adverse_effects_strategy import MinimizeAdverseEffectsStrategy
from src.constants import outcomes

class MinimizeAdverseEffectsStrategyTest(unittest.TestCase):
    """ Test suite for minimize_adverse_effects_strategy.py."""

    def setUp(self):
        self.decision = Decision()
        self.member = Member()
        self.bill = Bill()
        self.strategy = MinimizeAdverseEffectsStrategy(self.decision, self.member, self.bill)

        self.stance = Stance()
        self.stance.issue = "Some Issue"
        self.stance.side = outcomes.FOR

        self.stance1 = Stance()
        self.stance1.issue = "Some Other Issue"
        self.stance1.side = outcomes.AGN

        self.stance2 = Stance()
        self.stance2.issue = "Golden Issue"
        self.stance2.side = outcomes.AGN

        self.stance.importance = importance.B
        self.stance1.importance = importance.B
        self.stance2.importance = importance.A

    def test_init(self):
        """Tests whether a strategy can be constructed properly"""
        result = MinimizeAdverseEffectsStrategy(self.decision, self.member, self.bill)

        self.assertEqual(result._name, "Minimize Adverse Effects")
        self.assertEqual(result._decision, self.decision)
        self.assertEqual(result._member, self.member)
        self.assertEqual(result._bill, self.bill)
        self.assertEqual(result._success, False)

    def test_run_fail_no_majority(self):
        """ Verifies that run() fails if there is no majority"""
        self.decision.for_stances = [self.stance2]
        self.decision.agn_stances = [self.stance1]
        result = self.strategy.run()

        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)

    def test_run_fail_majority_stances_not_most_important(self):
        """ Verifies that run() fails if both sides are equally important"""
        self.decision.for_stances = [self.stance, self.stance]
        self.decision.agn_stances = [self.stance1]
        result = self.strategy.run()

        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)

    def test_run_success_FOR(self):
        """ Verifies that run() successfully sets a FOR decision"""
        self.decision.for_stances = [self.stance, self.stance2, self.stance]
        self.decision.agn_stances = [self.stance1]
        result = self.strategy.run()

        self.assertTrue(result)
        self.assertTrue(self.strategy._success)
        self.assertEquals(self.decision.result, outcomes.FOR)
        self.assertEquals(self.decision.reason, self.decision.for_stances)

    def test_run_success_AGN(self):
        """ Verifies that run() successfully sets a FOR decision"""
        self.decision.for_stances = [self.stance]
        self.decision.agn_stances = [self.stance1, self.stance2, self.stance]
        result = self.strategy.run()

        self.assertTrue(result)
        self.assertTrue(self.strategy._success)
        self.assertEquals(self.decision.result, outcomes.AGN)
        self.assertEquals(self.decision.reason, self.decision.agn_stances)

    def test_run_success_FOR_empty(self):
        """ Verifies that run() successfully when no for stances"""
        self.decision.for_stances = []
        self.decision.agn_stances = [self.stance1, self.stance2, self.stance]
        result = self.strategy.run()

        self.assertTrue(result)
        self.assertTrue(self.strategy._success)
        self.assertEquals(self.decision.result, outcomes.AGN)
        self.assertEquals(self.decision.reason, self.decision.agn_stances)

    def test_run_success_AGN_empty(self):
        """ Verifies that run() successfully when no agn stances"""
        self.decision.for_stances = [self.stance, self.stance2, self.stance]
        self.decision.agn_stances = []
        result = self.strategy.run()

        self.assertTrue(result)
        self.assertTrue(self.strategy._success)
        self.assertEquals(self.decision.result, outcomes.FOR)
        self.assertEquals(self.decision.reason, self.decision.for_stances)


    def test_explain(self):
        """ Verifies explain runs if there is a success [aka _explain is implemented]."""
        self.decision.for_stances = [self.stance, self.stance2, self.stance]
        self.decision.agn_stances = [self.stance1]
        result = self.strategy.run()

        self.assertTrue(result)

        self.strategy.explain()

    def test_explain_empty_FOR_stances(self):
        """ Verifies explain runs if for stances empty."""
        self.decision.for_stances = []
        self.decision.agn_stances = [self.stance1, self.stance2, self.stance]
        result = self.strategy.run()
        self.assertTrue(result)
        self.strategy.explain()

    def test_explain_empty_AGN_stances(self):
        """ Verifies explain runs if agn stances empty."""
        self.decision.for_stances = [self.stance, self.stance2, self.stance]
        self.decision.agn_stances = []
        result = self.strategy.run()
        self.assertTrue(result)
        self.strategy.explain()