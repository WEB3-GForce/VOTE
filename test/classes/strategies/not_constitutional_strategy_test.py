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
from src.classes.issue import Issue
from src.classes.member import Member
from src.classes.stance import Stance
from src.classes.data.result_data import ResultData
from src.classes.strategies.not_constitutional_strategy import NotConstitutionalStrategy
from src.constants import outcomes
from src.constants import database as db_constants
from src.database.pymongodb import PymongoDB

class NotConstitutionalStrategyTest(unittest.TestCase):
    """ Test suite for not_constitutional_strategy.py."""

    @classmethod
    def drop_collections(cls, DB):
        """Removes all the collections from a DB"""
        for collection_name in db_constants.DB_COLLECTIONS:
            DB.DB.drop_collection(collection_name)

    @classmethod
    def setUpClass(cls):
        # Make sure that the database is clean before this class is run.
        DB = PymongoDB()
        NotConstitutionalStrategyTest.drop_collections(DB)

    def setUp(self):
        self.DB = PymongoDB.get_db()
        self.decision = Decision()
        self.member = Member()
        self.bill = Bill()
        self.strategy = NotConstitutionalStrategy(self.decision, self.member, self.bill)

        self.stance = Stance()
        self.stance.issue = "Some Issue"
        self.stance.side = outcomes.FOR

        self.stance1 = Stance()
        self.stance1.issue = "Some Other Issue"
        self.stance1.side = outcomes.AGN

        self.group_result = ResultData()
        self.group_result.outcome = outcomes.AGN
        self.group_result.data = [self.stance]

        self.credo_result = ResultData()
        self.credo_result.outcome = outcomes.AGN
        self.credo_result.data = [self.stance]

        self.decision.MI_group = self.group_result
        self.decision.MI_credo = self.credo_result

        self.stance_con = Stance()
        self.stance_con.issue = self.strategy._CONSTITUTION
        self.stance_con.side = outcomes.FOR

        self.decision.for_stances = [self.stance]
        self.decision.agn_stances = [self.stance_con]


    def tearDown(self):
        # Delete the database each time to start fresh.
        NotConstitutionalStrategyTest.drop_collections(self.DB)

    def test_init(self):
        """Tests whether a strategy can be constructed properly"""
        result = NotConstitutionalStrategy(self.decision, self.member, self.bill)

        self.assertEqual(result._name, "Not Constitutional")
        self.assertEqual(result._decision, self.decision)
        self.assertEqual(result._member, self.member)
        self.assertEqual(result._bill, self.bill)
        self.assertEqual(result._success, False)

    def test_run_fail_no_constitutional_issue_in_db(self):
        """ Verifies the function fails if there is no Constitution issue."""
        result = self.strategy.run()
        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)

    def test_run_fail_no_consensus(self):
        """ Verifies the function fails if there is no consensus."""
        constitution = Issue()
        constitution.name = self.strategy._CONSTITUTION
        self.DB.insert_one(db_constants.ISSUES, constitution)

        self.group_result.outcome = outcomes.FOR
        self.credo_result.outcome = outcomes.AGN

        result = self.strategy.run()
        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)


    def test_run_fail_consensus_for(self):
        """ Verifies the function fails if there is a consensus FOR the bill."""
        constitution = Issue()
        constitution.name = self.strategy._CONSTITUTION
        self.DB.insert_one(db_constants.ISSUES, constitution)

        self.group_result.outcome = outcomes.FOR
        self.credo_result.outcome = outcomes.FOR

        result = self.strategy.run()
        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)


    def test_run_fail_no_constitutional_stance_in_agn_stances(self):
        """ Verifies the function fails if the bill isn't unconstitutional."""
        constitution = Issue()
        constitution.name = self.strategy._CONSTITUTION
        self.DB.insert_one(db_constants.ISSUES, constitution)

        self.decision.agn_stances = [self.stance1]

        result = self.strategy.run()
        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)

    def test_run_success(self):
        """ Verifies that run() successfully makes a decision"""
        constitution = Issue()
        constitution.name = self.strategy._CONSTITUTION
        self.DB.insert_one(db_constants.ISSUES, constitution)

        result = self.strategy.run()

        self.assertTrue(result)
        self.assertTrue(self.strategy._success)
        self.assertEquals(self.decision.result, outcomes.AGN)
        self.assertEquals(self.decision.reason, self.decision.agn_stances)
        self.assertEquals(self.decision.downside, self.decision.for_stances)

    def test_explain(self):
        """ Verifies explain runs if there is a success [aka _explain is implemented]."""
        constitution = Issue()
        constitution.name = self.strategy._CONSTITUTION
        self.DB.insert_one(db_constants.ISSUES, constitution)

        result = self.strategy.run()

        self.assertTrue(result)
        self.strategy.explain()