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
import os
import unittest

from src.constants import outcomes
from src.config import config
from src.scripts import configure_logging
from src.scripts.database import load_data
from src.vote import vote

class StagingTest(unittest.TestCase):
    """ Test suite for not_constitutional_strategy.py."""

    @classmethod
    def setUpClass(cls):
        # Make sure that the database is clean before this class is run.
        cls.old_config = config.CONFIG
        config.load_config(os.path.dirname(__file__) + "/../../src/config/staging.json")
        configure_logging.configure_logging()
        load_data.load_data()

    @classmethod
    def tearDownClass(cls):
        # Delete the database each time to start fresh.
        config.CONFIG = cls.old_config
        configure_logging.configure_logging()

    def test_popular_decision_FOR(self):
        """Tests that VOTE can decide FOR with a popular decision."""
        decision = vote.vote("SMITH", "HR-4800")

        self.assertEqual(decision.strategy, "Popular Decision")
        self.assertEqual(decision.result, outcomes.FOR)
        self.assertTrue(len(decision.reason) > 0)
        self.assertEqual(len(decision.downside + decision.downside_record), 0)

    def test_popular_decision_AGN(self):
        """Tests that VOTE can decide AGN with a popular decision."""
        decision = vote.vote("DOE", "HR-4800")

        self.assertEqual(decision.result, outcomes.AGN)
        self.assertEqual(decision.strategy, "Popular Decision")
        self.assertTrue(len(decision.reason) > 0)
        self.assertEqual(len(decision.downside + decision.downside_record), 0)

    def test_inconsistent_constituency_FOR(self):
        """Tests that VOTE can decide FOR with Inconsistent Constituency."""
        decision = vote.vote("SMITH", "AMD")
        self.assertEqual(decision.strategy, "Inconsistent Constituency")
        self.assertEqual(decision.result, outcomes.FOR)
        self.assertTrue(len(decision.reason) > 0)
        self.assertTrue(len(decision.downside + decision.downside_record) > 0)

    def test_inconsistent_constituency_AGN(self):
        """Tests that VOTE can decide AGN with Inconsistent Constituency."""
        decision = vote.vote("DOE", "HR-4264")
        self.assertEqual(decision.strategy, "Inconsistent Constituency")
        self.assertEqual(decision.result, outcomes.AGN)
        self.assertTrue(len(decision.reason) > 0)
        self.assertTrue(len(decision.downside + decision.downside_record) > 0)

    def test_non_partisan_decision_FOR(self):
        """Tests that VOTE can decide FOR with Non-partisan Decision."""
        decision = vote.vote("DOE", "AMD")
        self.assertEqual(decision.strategy, "Non-partisan Decision")
        self.assertEqual(decision.result, outcomes.FOR)
        self.assertTrue(len(decision.reason) > 0)
        self.assertTrue(len(decision.downside + decision.downside_record) > 0)

    def test_non_partisan_decision_AGN(self):
        """Tests that VOTE can decide AGN with Non-partisan Decision."""
        decision = vote.vote("SMITH", "HR-4264")
        self.assertEqual(decision.strategy, "Non-partisan Decision")
        self.assertEqual(decision.result, outcomes.AGN)
        self.assertTrue(len(decision.reason) > 0)
        self.assertTrue(len(decision.downside + decision.downside_record) > 0)

    def test_non_constitutional_AGN(self):
        """Tests that VOTE can decide AGN with Not Constitutional."""
        decision = vote.vote("DOE", "HR-0")
        self.assertEqual(decision.strategy, "Not Constitutional")
        self.assertEqual(decision.result, outcomes.AGN)
        self.assertTrue(len(decision.reason) > 0)
        self.assertTrue(len(decision.downside + decision.downside_record) > 0)

    def test_unimportant_bill_FOR(self):
        """Tests that VOTE can decide FOR with Unimportant Bill."""
        decision = vote.vote("JORDAN", "HR-4800")
        self.assertEqual(decision.strategy, "Unimportant Bill")
        self.assertEqual(decision.result, outcomes.FOR)
        self.assertTrue(len(decision.reason) > 0)
        self.assertTrue(len(decision.downside + decision.downside_record) > 0)

    def test_unimportant_bill_AGN(self):
        """Tests that VOTE can decide AGN with Unimportant Bill."""
        decision = vote.vote("WILLIAMS", "HR-4800")
        self.assertEqual(decision.strategy, "Unimportant Bill")
        self.assertEqual(decision.result, outcomes.AGN)
        self.assertTrue(len(decision.reason) > 0)
        self.assertTrue(len(decision.downside + decision.downside_record) > 0)

    def test_balance_the_books_FOR(self):
        """Tests that VOTE can decide FOR with Balance the Books."""
        decision = vote.vote("JORDAN", "HR-4264")
        self.assertEqual(decision.strategy, "Balance the Books")
        self.assertEqual(decision.result, outcomes.FOR)
        self.assertTrue(len(decision.reason) > 0)
        self.assertTrue(len(decision.downside + decision.downside_record) > 0)

    def test_balance_the_books_AGN(self):
        """Tests that VOTE can decide AGN with Balance the Books."""
        decision = vote.vote("WILLIAMS", "HR-4264")
        self.assertEqual(decision.strategy, "Balance the Books")
        self.assertEqual(decision.result, outcomes.AGN)
        self.assertTrue(len(decision.reason) > 0)
        self.assertTrue(len(decision.downside + decision.downside_record) > 0)

    def test_best_for_the_country_FOR(self):
        """Tests that VOTE can decide FOR with Best for the Country."""
        decision = vote.vote("JORDAN", "HR-777")
        self.assertEqual(decision.strategy, "Best for the Country")
        self.assertEqual(decision.result, outcomes.FOR)
        self.assertTrue(len(decision.reason) > 0)
        self.assertTrue(len(decision.downside + decision.downside_record) > 0)

    def test_best_for_the_country_AGN(self):
        """Tests that VOTE can decide AGN with Best for the Country."""
        decision = vote.vote("JORDAN", "HR-778")
        self.assertEqual(decision.strategy, "Best for the Country")
        self.assertEqual(decision.result, outcomes.AGN)
        self.assertTrue(len(decision.reason) > 0)
        self.assertTrue(len(decision.downside + decision.downside_record) > 0)

    def test_change_of_heart_FOR(self):
        """Tests that VOTE can decide FOR with Change of Heart."""
        decision = vote.vote("JORDAN", "HR-780")
        self.assertEqual(decision.strategy, "Change of Heart")
        self.assertEqual(decision.result, outcomes.FOR)
        self.assertTrue(len(decision.reason) > 0)
        self.assertTrue(len(decision.downside + decision.downside_record) > 0)

    def test_change_of_heart_AGN(self):
        """Tests that VOTE can decide AGN with Change of Heart."""
        decision = vote.vote("JORDAN", "HR-779")
        self.assertEqual(decision.strategy, "Change of Heart")
        self.assertEqual(decision.result, outcomes.AGN)
        self.assertTrue(len(decision.reason) > 0)
        self.assertTrue(len(decision.downside + decision.downside_record) > 0)

    def test_innoculation_FOR(self):
        """Tests that VOTE can decide FOR with Inoculation."""
        decision = vote.vote("YANG", "HR-4800")
        self.assertEqual(decision.strategy, "Inoculation")
        self.assertEqual(decision.result, outcomes.FOR)
        self.assertTrue(len(decision.reason) > 0)
        self.assertTrue(len(decision.downside + decision.downside_record) > 0)

    def test_innoculation_AGN(self):
        """Tests that VOTE can decide AGN with Inoculation."""
        decision = vote.vote("YANG", "ANTI-HR-4800")
        self.assertEqual(decision.strategy, "Inoculation")
        self.assertEqual(decision.result, outcomes.AGN)
        self.assertTrue(len(decision.reason) > 0)
        self.assertTrue(len(decision.downside + decision.downside_record) > 0)

    def test_could_not_pass(self):
        """Tests that VOTE can decide with Could Not Pass."""
        decision = vote.vote("YIN", "HR-900")
        self.assertEqual(decision.strategy, "Could Not Pass")
        self.assertEqual(decision.result, outcomes.AGN)
        self.assertTrue(len(decision.reason) > 0)
        self.assertTrue(len(decision.downside + decision.downside_record) > 0)

    def test_not_good_enough(self):
        """Tests that VOTE can decide with Not Good Enough."""
        decision = vote.vote("YIN", "HR-4264")
        self.assertEqual(decision.strategy, "Not Good Enough")
        self.assertEqual(decision.result, outcomes.AGN)
        self.assertTrue(len(decision.reason) > 0)
        self.assertTrue(len(decision.downside + decision.downside_record) > 0)

    def test_simple_consensus_FOR(self):
        """Tests that VOTE can decide FOR with Simple Consensus."""
        decision = vote.vote("YIN", "AMD-IMP")
        self.assertEqual(decision.strategy, "Simple Consensus")
        self.assertEqual(decision.result, outcomes.FOR)
        self.assertTrue(len(decision.reason) > 0)
        self.assertTrue(len(decision.downside + decision.downside_record) > 0)

    def test_simple_consensus_AGN(self):
        """Tests that VOTE can decide AGN with Simple Consensus."""
        decision = vote.vote("YANG", "AMD-IMP")
        self.assertEqual(decision.strategy, "Simple Consensus")
        self.assertEqual(decision.result, outcomes.AGN)
        self.assertTrue(len(decision.reason) > 0)
        self.assertTrue(len(decision.downside + decision.downside_record) > 0)

    def test_normative_decision_FOR(self):
        """Tests that VOTE can decide FOR with Normative Decision."""
        decision = vote.vote("WILLIAMS", "HR-780")
        self.assertEqual(decision.strategy, "Normative Decision")
        self.assertEqual(decision.result, outcomes.FOR)
        self.assertTrue(len(decision.reason) > 0)
        self.assertTrue(len(decision.downside + decision.downside_record) == 0)

    def test_normative_decision_AGN(self):
        """Tests that VOTE can decide AGN with Normative Decision."""
        decision = vote.vote("WILLIAMS", "HR-779")
        self.assertEqual(decision.strategy, "Normative Decision")
        self.assertEqual(decision.result, outcomes.AGN)
        self.assertTrue(len(decision.reason) > 0)
        self.assertTrue(len(decision.downside + decision.downside_record) == 0)