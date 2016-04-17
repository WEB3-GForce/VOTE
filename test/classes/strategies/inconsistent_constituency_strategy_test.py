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
from src.classes.data.result_data import ResultData
from src.classes.strategies.inconsistent_constituency_strategy import InconsistentConstituencyStrategy
from src.constants import outcomes

class InconsistentConstituencyStrategyTest(unittest.TestCase):
    """ Test suite for inconsistent_constituency.py."""

    def setUp(self):
        self.decision = Decision()
        self.member = Member()
        self.bill = Bill()
        self.strategy = InconsistentConstituencyStrategy(self.decision, self.member, self.bill)

        self.stance = Stance()
        self.stance.issue = "Some Issue"
        self.stance.side = outcomes.FOR

        self.stance1 = Stance()
        self.stance1.issue = "Some Other Issue"
        self.stance1.side = outcomes.AGN

    def test_init(self):
        """Tests whether a strategy can be constructed properly"""
        result = InconsistentConstituencyStrategy(self.decision, self.member, self.bill)

        self.assertEqual(result._name, "Inconsistent Constituency")
        self.assertEqual(result._decision, self.decision)
        self.assertEqual(result._member, self.member)
        self.assertEqual(result._bill, self.bill)
        self.assertEqual(result._success, False)

    def test_run_success_FOR(self):
        """ Verifies that run() successfully sets a FOR decision"""
        group_result = ResultData()
        group_result.outcome = outcomes.FOR
        group_result.data = [self.stance]

        credo_result = ResultData()
        credo_result.outcome = outcomes.FOR
        credo_result.data = [self.stance]

        self.decision.MI_group = group_result
        self.decision.MI_credo = credo_result
        self.decision.split_group = [self.stance, self.stance1]

        self.decision.for_stances = [self.stance, self.stance]
        result = self.strategy.run()

        self.assertTrue(result)
        self.assertTrue(self.strategy._success)
        self.assertEquals(self.decision.result, outcomes.FOR)
        self.assertEquals(self.decision.reason, self.decision.for_stances)

    def test_run_success_AGN(self):
        """ Verifies that run() successfully sets an AGN decision"""
        group_result = ResultData()
        group_result.outcome = outcomes.AGN
        group_result.data = [self.stance]

        credo_result = ResultData()
        credo_result.outcome = outcomes.AGN
        credo_result.data = [self.stance]

        self.decision.MI_group = group_result
        self.decision.MI_credo = credo_result
        self.decision.split_group = [self.stance, self.stance1]

        self.decision.agn_stances = [self.stance, self.stance]
        result = self.strategy.run()

        self.assertTrue(result)
        self.assertTrue(self.strategy._success)
        self.assertEquals(self.decision.result, outcomes.AGN)
        self.assertEquals(self.decision.reason, self.decision.agn_stances)

    def test_run_fail_no_consensus(self):
        """ Verifies that the strategy fails when no consensus is reached."""
        group_result = ResultData()
        group_result.outcome = outcomes.FOR
        group_result.data = [self.stance]

        credo_result = ResultData()
        credo_result.outcome = outcomes.AGN
        credo_result.data = [self.stance1]

        self.decision.MI_group = group_result
        self.decision.MI_credo = credo_result
        self.decision.split_group = [self.stance, self.stance1]

        self.decision.for_stances = [self.stance]
        result = self.strategy.run()

        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)

    def test_run_fail_no_split_group(self):
        """ Verifies that the strategy fails when there is no split constituency."""
        group_result = ResultData()
        group_result.outcome = outcomes.FOR
        group_result.data = [self.stance]

        credo_result = ResultData()
        credo_result.outcome = outcomes.FOR
        credo_result.data = [self.stance]

        self.decision.MI_group = group_result
        self.decision.MI_credo = credo_result

        self.decision.for_stances = [self.stance]
        result = self.strategy.run()

        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)

    def test_explain(self):
        """ Verifies explain runs if there is a success [aka _explain is implemented]."""
        group_result = ResultData()
        group_result.outcome = outcomes.FOR
        group_result.data = [self.stance]

        self.decision.MI_group = group_result
        self.decision.split_group = [self.stance, self.stance1]

        result = self.strategy.run()
        self.assertTrue(result)

        self.strategy.explain()