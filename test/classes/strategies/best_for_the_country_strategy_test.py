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
from src.classes.group import Group
from src.classes.member import Member
from src.classes.stance import Stance
from src.classes.data.result_data import ResultData
from src.classes.strategies.best_for_the_country_strategy import BestForTheCountryStrategy
from src.constants import outcomes
from src.constants import database as db_constants
from src.database.pymongodb import PymongoDB

class BestForTheCountryStrategyTest(unittest.TestCase):
    """ Test suite for best_for_the_country_strategy.py."""

    @classmethod
    def drop_collections(cls, DB):
        """Removes all the collections from a DB"""
        for collection_name in db_constants.DB_COLLECTIONS:
            DB.DB.drop_collection(collection_name)

    @classmethod
    def setUpClass(cls):
        # Make sure that the database is clean before this class is run.
        DB = PymongoDB()
        BestForTheCountryStrategyTest.drop_collections(DB)

    def setUp(self):
        self.DB = PymongoDB.get_db()
        self.decision = Decision()
        self.member = Member()
        self.bill = Bill()
        self.strategy = BestForTheCountryStrategy(self.decision, self.member, self.bill)

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

        self.stance_country = Stance()
        self.stance_country.issue = "Very important"
        self.stance_country.source = self.strategy._COUNTRY
        self.stance_country.side = outcomes.FOR

        self.decision.for_stances = [self.stance]
        self.decision.agn_stances = [self.stance1]


    def tearDown(self):
        # Delete the database each time to start fresh.
        BestForTheCountryStrategyTest.drop_collections(self.DB)

    def test_init(self):
        """Tests whether a strategy can be constructed properly"""
        result = BestForTheCountryStrategy(self.decision, self.member, self.bill)

        self.assertEqual(result._name, "Best for the Country")
        self.assertEqual(result._decision, self.decision)
        self.assertEqual(result._member, self.member)
        self.assertEqual(result._bill, self.bill)
        self.assertEqual(result._success, False)

    def test_run_fail_no_country_group_in_db(self):
        """ Verifies the function fails if there is no Country group."""
        self.group_result.outcome = outcomes.FOR
        self.credo_result.outcome = outcomes.FOR

        self.decision.groups_for = [self.stance_country]
        self.decision.groups_agn = [self.stance1]

        result = self.strategy.run()
        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)

    def test_run_fail_no_consensus(self):
        """ Verifies the function fails if there is no consensus."""
        country = Group()
        country.name = self.strategy._COUNTRY
        self.DB.insert_one(db_constants.GROUPS, country)

        self.group_result.outcome = outcomes.FOR
        self.credo_result.outcome = outcomes.AGN

        self.decision.groups_for = [self.stance_country]
        self.decision.groups_agn = [self.stance1]

        result = self.strategy.run()

        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)

    def test_run_fail_no_country_stance_in_groups_for(self):
        """ Verifies the function fails if the country has no FOR stances."""
        country = Group()
        country.name = self.strategy._COUNTRY
        self.DB.insert_one(db_constants.GROUPS, country)

        self.group_result.outcome = outcomes.FOR
        self.credo_result.outcome = outcomes.FOR

        self.decision.groups_for = [self.stance]
        self.decision.groups_agn = [self.stance1]

        result = self.strategy.run()

        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)

    def test_run_fail_no_country_stance_in_groups_agn(self):
        """ Verifies the function fails if the country has no AGN stances."""
        country = Group()
        country.name = self.strategy._COUNTRY
        self.DB.insert_one(db_constants.GROUPS, country)

        self.group_result.outcome = outcomes.AGN
        self.credo_result.outcome = outcomes.AGN

        self.decision.groups_for = [self.stance]
        self.decision.groups_agn = [self.stance1]

        result = self.strategy.run()

        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)

    def test_run_fail_country_split_FOR(self):
        """ Verifies a FOR consensus fails if the country is split."""
        country = Group()
        country.name = self.strategy._COUNTRY
        self.DB.insert_one(db_constants.GROUPS, country)

        self.group_result.outcome = outcomes.FOR
        self.credo_result.outcome = outcomes.FOR

        self.decision.groups_for = [self.stance_country]
        self.decision.groups_agn = [self.stance_country]

        result = self.strategy.run()

        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)

    def test_run_fail_country_split_AGN(self):
        """ Verifies an AGN consensus fails if the country is split."""
        country = Group()
        country.name = self.strategy._COUNTRY
        self.DB.insert_one(db_constants.GROUPS, country)

        self.group_result.outcome = outcomes.AGN
        self.credo_result.outcome = outcomes.AGN

        self.decision.groups_for = [self.stance_country]
        self.decision.groups_agn = [self.stance_country]

        result = self.strategy.run()

        self.assertFalse(result)
        self.assertFalse(self.strategy._success)
        self.assertEquals(self.decision.result, None)
        self.assertEquals(self.decision.reason, None)

    def test_run_success_FOR(self):
        """ Verifies that run() successfully makes a FOR decision"""
        country = Group()
        country.name = self.strategy._COUNTRY
        self.DB.insert_one(db_constants.GROUPS, country)

        self.group_result.outcome = outcomes.FOR
        self.credo_result.outcome = outcomes.FOR

        self.decision.groups_for = [self.stance_country, self.stance]
        self.decision.groups_agn = [self.stance1]

        result = self.strategy.run()

        self.assertTrue(result)
        self.assertTrue(self.strategy._success)
        self.assertEquals(self.strategy._country_stances, [self.stance_country])
        self.assertEquals(self.decision.result, outcomes.FOR)
        self.assertEquals(self.decision.reason, self.decision.for_stances)
        self.assertEquals(self.decision.downside, self.decision.agn_stances)

    def test_run_success_AGN(self):
        """ Verifies that run() successfully makes a AGN decision"""
        country = Group()
        country.name = self.strategy._COUNTRY
        self.DB.insert_one(db_constants.GROUPS, country)

        self.group_result.outcome = outcomes.AGN
        self.credo_result.outcome = outcomes.AGN

        self.decision.groups_for = [self.stance]
        self.decision.groups_agn = [self.stance_country, self.stance1]

        result = self.strategy.run()

        self.assertTrue(result)
        self.assertTrue(self.strategy._success)
        self.assertEquals(self.strategy._country_stances, [self.stance_country])
        self.assertEquals(self.decision.result, outcomes.AGN)
        self.assertEquals(self.decision.reason, self.decision.agn_stances)
        self.assertEquals(self.decision.downside, self.decision.for_stances)


    def test_explain(self):
        """ Verifies explain runs if there is a success [aka _explain is implemented]."""
        country = Group()
        country.name = self.strategy._COUNTRY
        self.DB.insert_one(db_constants.GROUPS, country)

        self.group_result.outcome = outcomes.AGN
        self.credo_result.outcome = outcomes.AGN

        self.decision.groups_for = [self.stance]
        self.decision.groups_agn = [self.stance_country]

        result = self.strategy.run()

        self.assertTrue(result)
        self.strategy.explain()
