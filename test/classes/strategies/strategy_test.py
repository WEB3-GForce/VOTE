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
from src.classes.strategies.strategy import Strategy
from src.classes.data.result_data import ResultData
from src.constants import outcomes

from test.test_helpers.always_fail_strategy import AlwaysFailStrategy
from test.test_helpers.always_succeed_strategy import AlwaysSucceedStrategy

class StrategyTest(unittest.TestCase):
    """ Test suite for strategy.py."""

    def setUp(self):
        self.decision = Decision()
        self.member = Member()
        self.bill = Bill()

    def test_init(self):
        """Tests whether a strategy can be constructed properly"""
        result = Strategy(self.decision, self.member, self.bill)

        self.assertEqual(result._name, "Strategy")
        self.assertEqual(result._decision, self.decision)
        self.assertEqual(result._member, self.member)
        self.assertEqual(result._bill, self.bill)
        self.assertEqual(result._success, False)

    def test_run_success(self):
        """ Verifies that run() works properly on a success. A child class is
        used to implement _run()"""
        strategy = AlwaysSucceedStrategy(self.decision, self.member, self.bill)
        result = strategy.run()
        self.assertTrue(result)

    def test_run_fail(self):
        """ Verifies that run() works properly on a failure. A child class is
        used to implement _run()"""
        strategy = AlwaysFailStrategy(self.decision, self.member, self.bill)
        result = strategy.run()
        self.assertFalse(result)

    def test_explain_when_not_successful(self):
        """ Verifies explain() exits gracefully when strategy._succeed == F"""
        result = Strategy(self.decision, self.member, self.bill)
        result.explain()

    def test_explain_when_successful(self):
        """ Verifies explain() calls _explain() when strategy._succeed == T"""
        result = Strategy(self.decision, self.member, self.bill)
        result._success = True
        self.assertRaises(NotImplementedError, result.explain)

    def test__run(self):
        """ Verifies that _run() throws a NotImplementedError"""
        result = Strategy(self.decision, self.member, self.bill)
        self.assertRaises(NotImplementedError, result._run)

    def test__explain(self):
        """ Verifies that _explain() throws a NotImplementedError"""
        result = Strategy(self.decision, self.member, self.bill)
        self.assertRaises(NotImplementedError, result._explain)

    def test__finalize_decision(self):
        """ Verifies a decision can properly be updated with the result"""
        strategy = Strategy(self.decision, self.member, self.bill)

        stance = Stance()
        stance.issue = "Something good"
        stance.side = "FOR"

        stance1 = Stance()
        stance1.issue = "Fire"
        stance1.side = "AGN"

        stance2 = Stance()
        stance2.issue = "Ice"
        stance2.side = "FOR"

        reason = [stance, stance1]
        downside = [stance2]

        strategy._finalize_decision(outcomes.FOR, reason, downside)

        self.assertEqual(self.decision.strategy, strategy._name)
        self.assertEqual(self.decision.result, outcomes.FOR)
        self.assertEqual(self.decision.reason, reason)
        self.assertEqual(self.decision.downside, downside)
        self.assertEqual(self.decision.downside_record, [])

    def test__finalize_decision_with_record_stances(self):
        """ Verifies downside_record is properly set"""
        strategy = Strategy(self.decision, self.member, self.bill)

        stance = Stance()
        stance.issue = "Something good"
        stance.side = "FOR"

        stance1 = Stance()
        stance1.issue = "Fire"
        stance1.side = "AGN"
        stance1.source_db = "bills"

        stance2 = Stance()
        stance2.issue = "Ice"
        stance2.side = "FOR"

        reason = [stance2]
        downside = [stance, stance1]

        strategy._finalize_decision(outcomes.FOR, reason, downside)

        self.assertEqual(self.decision.strategy, strategy._name)
        self.assertEqual(self.decision.result, outcomes.FOR)
        self.assertEqual(self.decision.reason, reason)
        self.assertEqual(self.decision.downside, [stance])
        self.assertEqual(self.decision.downside_record, [stance1])

    def test__set_decision_FOR(self):
        """ Verifies the decision is properly set FOR the bill"""
        strategy = Strategy(self.decision, self.member, self.bill)

        stance = Stance()
        stance.issue = "Something good"
        stance.side = "FOR"

        stance1 = Stance()
        stance1.issue = "Something Bad"
        stance1.side = "AGN"

        self.decision.for_stances = [stance]
        self.decision.agn_stances = [stance1]

        strategy._set_decision(outcomes.FOR)

        self.assertEqual(self.decision.strategy, strategy._name)
        self.assertEqual(self.decision.result, outcomes.FOR)
        self.assertEqual(self.decision.reason, self.decision.for_stances)
        self.assertEqual(self.decision.downside, self.decision.agn_stances)

    def test__set_decision_AGN(self):
        """ Verifies the decision is properly set AGN the bill"""
        strategy = Strategy(self.decision, self.member, self.bill)

        stance = Stance()
        stance.issue = "Something good"
        stance.side = "FOR"

        stance1 = Stance()
        stance1.issue = "Something Bad"
        stance1.side = "AGN"
        stance1.source_db = "bills"

        self.decision.for_stances = [stance]
        self.decision.agn_stances = [stance1]

        strategy._set_decision(outcomes.AGN)

        self.assertEqual(self.decision.strategy, strategy._name)
        self.assertEqual(self.decision.result, outcomes.AGN)
        self.assertEqual(self.decision.reason, self.decision.agn_stances)
        self.assertEqual(self.decision.downside, self.decision.for_stances)

    def test__set_decision_neither(self):
        """ Verifies no result is set for an invalid result"""
        strategy = Strategy(self.decision, self.member, self.bill)

        strategy._set_decision("Invalid result")
        self.assertEqual(self.decision.strategy, None)

    def test__majority_FOR(self):
        """ Verifies when there is a majority for the bill"""
        strategy = Strategy(self.decision, self.member, self.bill)

        stance = Stance()
        stance.issue = "Something good"
        stance.side = "FOR"

        self.decision.for_stances = [stance]
        self.decision.agn_stances = []
        result = strategy._majority()
        self.assertEqual(result, outcomes.FOR)

    def test__majority_AGN(self):
        """ Verifies when there is a majority against the bill"""
        strategy = Strategy(self.decision, self.member, self.bill)

        stance1 = Stance()
        stance1.issue = "Something Bad"
        stance1.side = "AGN"

        self.decision.for_stances = []
        self.decision.agn_stances = [stance1]
        result = strategy._majority()
        self.assertEqual(result, outcomes.AGN)

    def test__majority_neither(self):
        """ Verifies when both sides are equally supported"""
        strategy = Strategy(self.decision, self.member, self.bill)

        stance = Stance()
        stance.issue = "Something good"
        stance.side = "FOR"

        stance1 = Stance()
        stance1.issue = "Something Bad"
        stance1.side = "AGN"

        self.decision.for_stances = [stance]
        self.decision.agn_stances = [stance1]
        result = strategy._majority()
        self.assertEqual(result, None)

    def test__consensus_FOR(self):
        """ Verifies when there is a consensus FOR the bill"""
        strategy = Strategy(self.decision, self.member, self.bill)

        strategy._decision.MI_stance = ResultData({"outcome": outcomes.FOR, "data": []})
        strategy._decision.MI_group = ResultData({"outcome": outcomes.FOR, "data": []})
        strategy._decision.MI_credo = ResultData({"outcome": outcomes.FOR, "data": []})
        strategy._decision.MI_record = ResultData({"outcome": outcomes.FOR, "data": []})
        strategy._decision.MI_norm = ResultData({"outcome": outcomes.FOR, "data": []})

        result = strategy._consensus()
        self.assertEqual(result, outcomes.FOR)

    def test__consensus_AGN(self):
        """ Verifies when there is a consensus AGN the bill"""
        strategy = Strategy(self.decision, self.member, self.bill)

        strategy._decision.MI_stance = ResultData({"outcome": outcomes.AGN, "data": []})
        strategy._decision.MI_group = ResultData({"outcome": outcomes.AGN, "data": []})
        strategy._decision.MI_credo = ResultData({"outcome": outcomes.AGN, "data": []})
        strategy._decision.MI_record = ResultData({"outcome": outcomes.AGN, "data": []})
        strategy._decision.MI_norm = ResultData({"outcome": outcomes.AGN, "data": []})

        result = strategy._consensus()
        self.assertEqual(result, outcomes.AGN)

    def test__consensus_neither(self):
        """ Verifies when there is no consensus"""
        strategy = Strategy(self.decision, self.member, self.bill)

        strategy._decision.MI_stance = ResultData({"outcome": outcomes.AGN, "data": []})
        strategy._decision.MI_group = ResultData({"outcome": outcomes.AGN, "data": []})
        strategy._decision.MI_credo = ResultData({"outcome": outcomes.AGN, "data": []})
        strategy._decision.MI_record = ResultData({"outcome": outcomes.AGN, "data": []})
        strategy._decision.MI_norm = ResultData({"outcome": outcomes.FOR, "data": []})

        result = strategy._consensus()
        self.assertEqual(result, None)

    def test__consensus_ignore_none(self):
        """ Verifies that MI sources that are None are ignored"""
        strategy = Strategy(self.decision, self.member, self.bill)

        strategy._decision.MI_stance = ResultData({"outcome": outcomes.AGN, "data": []})

        result = strategy._consensus()
        self.assertEqual(result, outcomes.AGN)

    def test__explain_simple_consensus(self):
        """ Verifies the function works without raising an error"""
        stance = Stance()
        stance.issue = "Some Issue"
        stance.side = outcomes.FOR

        group_result = ResultData()
        group_result.outcome = outcomes.FOR
        group_result.data = [stance]

        self.decision.result = outcomes.FOR
        self.decision.MI_group = group_result

        strategy = Strategy(self.decision, self.member, self.bill)
        strategy._explain_simple_consensus()
