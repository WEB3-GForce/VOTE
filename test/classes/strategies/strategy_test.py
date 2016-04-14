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
from src.classes.member import Member
from src.classes.strategies.strategy import Strategy

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

    def test__run(self):
        """ Verifies that _run() throws a NotImplementedError"""
        result = Strategy(self.decision, self.member, self.bill)
        self.assertRaises(NotImplementedError, result._run)

    def test_explain_when_not_successful(self):
        """ Verifies explain() exits gracefully when strategy._succeed == F"""
        result = Strategy(self.decision, self.member, self.bill)
        result.explain()

    def test_explain_when_successful(self):
        """ Verifies explain() calls _explain() when strategy._succeed == T"""
        result = Strategy(self.decision, self.member, self.bill)
        result._success = True
        self.assertRaises(NotImplementedError, result.explain)

    def test__explain(self):
        """ Verifies that _explain() throws a NotImplementedError"""
        result = Strategy(self.decision, self.member, self.bill)
        self.assertRaises(NotImplementedError, result._explain)
