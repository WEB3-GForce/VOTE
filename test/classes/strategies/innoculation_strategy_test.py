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
from src.classes.strategies.inoculation_strategy import InoculationStrategy
from src.constants import outcomes

class InoculationStrategyTest(unittest.TestCase):
    """ Test suite for inoculation_strategy.py."""

    def setUp(self):
        self.decision = Decision()
        self.member = Member()
        self.bill = Bill()
        self.strategy = InoculationStrategy(self.decision, self.member, self.bill)

        self.stance = Stance()
        self.stance.issue = "Some Issue"
        self.stance.side = outcomes.FOR

        self.stance1 = Stance()
        self.stance1.issue = "Some Other Issue"
        self.stance1.side = outcomes.AGN

        self.stance2 = Stance()
        self.stance2.issue = "Something else"
        self.stance2.side = outcomes.FOR

    def test_init(self):
        """Tests whether a strategy can be constructed properly"""
        result = InoculationStrategy(self.decision, self.member, self.bill)

        self.assertEqual(result._name, "Inoculation")
        self.assertEqual(result._decision, self.decision)
        self.assertEqual(result._member, self.member)
        self.assertEqual(result._bill, self.bill)
        self.assertEqual(result._success, False)

    def test_run_fail_no_divided_groups_FOR(self):
        """ Verifies that run() fails if no groups FOR the bill"""
        self.stance.importance = importance.C
        self.stance1.importance = importance.C

        self.decision.groups_for = []
        self.decision.groups_agn = [self.stance1]

        self.decision.for_stances = [self.stance, self.stance]
        self.decision.agn_stances = [self.stance1]

        result = self.strategy.run()

        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)

    def test_run_fail_no_divided_groups_AGN(self):
        """ Verifies that run() fails if no groups AGN the bill"""
        self.stance.importance = importance.C
        self.stance1.importance = importance.C

        self.decision.groups_for = [self.stance]
        self.decision.groups_agn = []

        self.decision.for_stances = [self.stance, self.stance]
        self.decision.agn_stances = [self.stance1]

        result = self.strategy.run()

        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)

    def test_run_fail_no_majority(self):
        """ Verifies that run() fails if there is no majority"""
        self.stance.importance = importance.C
        self.stance1.importance = importance.C

        self.decision.groups_for = [self.stance]
        self.decision.groups_agn = [self.stance1]

        self.decision.for_stances = [self.stance]
        self.decision.agn_stances = [self.stance1]

        result = self.strategy.run()

        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)

    def test_run_fail_stances_important(self):
        """ Verifies that run() fails if a group really cares about the bill."""
        self.stance.importance = importance.C
        self.stance1.importance = importance.C
        self.stance2.importance = importance.B

        self.decision.groups_for = [self.stance, self.stance]
        self.decision.groups_agn = [self.stance1, self.stance2, self.stance1]

        self.decision.for_stances = [self.stance, self.stance]
        self.decision.agn_stances = [self.stance1]

        result = self.strategy.run()

        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)


    def test_run_success_FOR(self):
        """ Verifies that run() successfully sets a FOR decision"""
        self.stance.importance = importance.C
        self.stance1.importance = importance.C

        self.decision.groups_for = [self.stance]
        self.decision.groups_agn = [self.stance1]

        self.decision.for_stances = [self.stance, self.stance]
        self.decision.agn_stances = [self.stance1]

        result = self.strategy.run()

        self.assertTrue(result)
        self.assertTrue(self.strategy._success)
        self.assertEquals(self.decision.result, outcomes.FOR)
        self.assertEquals(self.decision.reason, self.decision.for_stances)

    def test_run_success_AGN(self):
        """ Verifies that run() successfully sets a FOR decision"""
        self.stance.importance = importance.C
        self.stance1.importance = importance.C

        self.decision.groups_for = [self.stance]
        self.decision.groups_agn = [self.stance1]

        self.decision.for_stances = [self.stance]
        self.decision.agn_stances = [self.stance1, self.stance1]

        result = self.strategy.run()

        self.assertTrue(result)
        self.assertTrue(self.strategy._success)
        self.assertEquals(self.decision.result, outcomes.AGN)
        self.assertEquals(self.decision.reason, self.decision.agn_stances)

    def test_explain(self):
        """ Verifies explain runs if there is a success [aka _explain is implemented]."""
        self.stance.importance = importance.C
        self.stance1.importance = importance.C

        self.decision.groups_for = [self.stance]
        self.decision.groups_agn = [self.stance1]

        self.decision.for_stances = [self.stance, self.stance]
        self.decision.agn_stances = [self.stance1]

        result = self.strategy.run()

        self.assertTrue(result)

        self.strategy.explain()