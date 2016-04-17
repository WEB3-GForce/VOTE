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
from src.classes.data.result_data import ResultData
from src.classes.strategies.nonpartisan_decision_strategy import NonPartisanDecisionStrategy
from src.constants import outcomes

class NonPartisanDecisionStrategyTest(unittest.TestCase):
    """ Test suite for nonpartisan_decision_strategy.py."""

    def setUp(self):
        self.decision = Decision()
        self.member = Member()
        self.bill = Bill()
        self.strategy = NonPartisanDecisionStrategy(self.decision, self.member, self.bill)

        self.stance = Stance()
        self.stance.issue = "Some Issue"
        self.stance.side = outcomes.FOR

        self.stance1 = Stance()
        self.stance1.issue = "Some Other Issue"
        self.stance1.side = outcomes.AGN

        self.INDEPENDENT = "INDEPENDENT"

    def test_init(self):
        """Tests whether a strategy can be constructed properly"""
        result = NonPartisanDecisionStrategy(self.decision, self.member, self.bill)

        self.assertEqual(result._name, "Non-partisan Decision")
        self.assertEqual(result._decision, self.decision)
        self.assertEqual(result._member, self.member)
        self.assertEqual(result._bill, self.bill)
        self.assertEqual(result._success, False)

    def test_run_fail_no_credo(self):
        """ Verifies that run() fails if there is no MI_credo."""
        self.member.party = self.INDEPENDENT

        self.stance1.source = self.INDEPENDENT
        self.decision.groups_agn = [self.stance1]

        result = self.strategy.run()
        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)

    def test_run_fail_no_party(self):
        """ Verifies that run() fails if there is no party."""

        self.stance.importance = importance.A

        credo_result = ResultData()
        credo_result.outcome = outcomes.FOR
        credo_result.data = [self.stance]

        self.decision.MI_credo = credo_result

        self.stance1.source = self.INDEPENDENT
        self.decision.groups_agn = [self.stance1]

        result = self.strategy.run()
        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)

    def test_run_fail_no_opposing_groups(self):
        """ Verifies that run() fails if there is no groups opposing the member's credo."""

        self.stance.importance = importance.A

        credo_result = ResultData()
        credo_result.outcome = outcomes.FOR
        credo_result.data = [self.stance]

        self.decision.MI_credo = credo_result
        self.member.party = self.INDEPENDENT

        result = self.strategy.run()
        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)

    def test_run_fail_party_not_in_opposing_groups(self):
        """ Verifies that run() fails if the member's party does not have a
        stance in the groups opposing the member's credo."""

        self.stance.importance = importance.A

        credo_result = ResultData()
        credo_result.outcome = outcomes.FOR
        credo_result.data = [self.stance]

        self.decision.MI_credo = credo_result
        self.member.party = self.INDEPENDENT

        self.decision.groups_agn = [self.stance1]

        result = self.strategy.run()
        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)

    def test_run_fail_credo_stance_not_most_importance(self):
        """ Verifies that run() fails if the member doesn't care too strongly
        about the credo stances."""

        self.stance.importance = importance.B

        credo_result = ResultData()
        credo_result.outcome = outcomes.FOR
        credo_result.data = [self.stance]

        self.decision.MI_credo = credo_result
        self.member.party = self.INDEPENDENT

        self.stance1.source = self.INDEPENDENT
        self.decision.groups_agn = [self.stance1]

        result = self.strategy.run()
        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)


    def test_run_success_FOR(self):
        """ Verifies that run() successfully sets a FOR decision"""
        self.stance.importance = importance.A

        credo_result = ResultData()
        credo_result.outcome = outcomes.FOR
        credo_result.data = [self.stance]

        self.decision.MI_credo = credo_result
        self.member.party = self.INDEPENDENT

        self.stance1.source = self.INDEPENDENT
        self.decision.groups_agn = [self.stance1]

        result = self.strategy.run()
        self.assertTrue(result)
        self.assertTrue(self.strategy._success)
        self.assertEquals(self.decision.result, outcomes.FOR)

    def test_run_success_AGN(self):
        """ Verifies that run() successfully sets an AGN decision"""
        self.stance.importance = importance.A

        credo_result = ResultData()
        credo_result.outcome = outcomes.AGN
        credo_result.data = [self.stance]

        self.decision.MI_credo = credo_result
        self.member.party = self.INDEPENDENT

        self.stance1.source = self.INDEPENDENT
        self.decision.groups_for = [self.stance1]

        result = self.strategy.run()
        self.assertTrue(result)
        self.assertTrue(self.strategy._success)
        self.assertEquals(self.decision.result, outcomes.AGN)

    def test_explain(self):
        """ Verifies explain runs if there is a success [aka _explain is implemented]."""
        self.stance.importance = importance.A

        credo_result = ResultData()
        credo_result.outcome = outcomes.AGN
        credo_result.data = [self.stance]

        self.decision.MI_credo = credo_result
        self.member.party = self.INDEPENDENT

        self.stance1.source = self.INDEPENDENT
        self.decision.groups_for = [self.stance1]

        result = self.strategy.run()
        self.assertTrue(result)
        self.strategy.explain()
