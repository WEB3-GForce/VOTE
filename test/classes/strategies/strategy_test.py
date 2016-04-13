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

from src.classes.decision import Decision
from src.classes.strategies.strategy import Strategy

class StrategyTest(unittest.TestCase):
    """ Test suite for strategy.py."""

    def setUp(self):
        self.decision = Decision()

    def test_init(self):
        """Tests whether a strategy can be constructed properly"""
        result = Strategy(self.decision)

        self.assertEqual(result._decision, self.decision)
        self.assertEqual(result._success, False)

    def test_run(self):
        """ Verifies that run throws a NotImplementedError"""
        result = Strategy(self.decision)
        self.assertRaises(NotImplementedError, result.run)

    def test_explain(self):
        """ Verifies that explain throws a NotImplementedError"""
        result = Strategy(self.decision)
        self.assertRaises(NotImplementedError, result.explain)
