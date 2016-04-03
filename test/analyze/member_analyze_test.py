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

import sys
import unittest

from StringIO import StringIO

from src.analyze import member_analyze
from src.classes.relation import Relation
from src.classes.data.result_data import ResultData
from src.constants import database as db_constants
from src.constants import outcomes
from src.database import queries
from src.database.pymongodb import PymongoDB
from src.scripts.database import load_data

class MemberAnalyzeTest(unittest.TestCase):
    """ Test suite for member_analyze.py."""

    @classmethod
    def drop_collections(cls, DB):
        """Removes all the collections from a DB"""
        for collection_name in db_constants.DB_COLLECTIONS:
            DB.DB.drop_collection(collection_name)


    @classmethod
    def setUpClass(cls):
        # Make sure that the database is clean before this class is run.
        DB = PymongoDB()
        MemberAnalyzeTest.drop_collections(DB)

        # Ignore all output to the screen.
        sys.stdout = StringIO()

    @classmethod
    def tearDownClass(cls):
        sys.stdout = sys.__stdout__

    def setUp(self):
        self.DB = PymongoDB.get_db()
        load_data.load_data()
        self.member = self.DB.find_one(db_constants.MEMBERS,
            {"full_name" : "member_analyze_test"})

        self.BILL1 = "BILL1"
        self.BILL2 = "BILL2"
        self.BILL3 = "BILL3"

        self.GROUP1 = "GROUP1"
        self.GROUP2 = "GROUP2"

        self.bill1 = self.DB.find_one(db_constants.BILLS,
            queries.bill_query(self.BILL1))
        self.bill2 = self.DB.find_one(db_constants.BILLS,
            queries.bill_query(self.BILL2))
        self.bill3 = self.DB.find_one(db_constants.BILLS,
            queries.bill_query(self.BILL3))

        self.group1 = self.DB.find_one(db_constants.GROUPS,
            queries.bill_query(self.GROUP1))
        self.group2 = self.DB.find_one(db_constants.GROUPS,
            queries.bill_query(self.GROUP2))


    def tearDown(self):
        # Delete the database each time to start fresh.
        MemberAnalyzeTest.drop_collections(self.DB)

    def test_extract_single_voting_stance_invalid_bill(self):
        """ Verifies functionality when the specified bill doesn't exist."""
        vote = ResultData({"data" : "DOES NOT EXIST", "outcome" : outcomes.FOR})
        result = member_analyze._extract_single_voting_stance(vote)
        self.assertEquals(result, [])

    def test_extract_single_voting_stance_invalid_side(self):
        """ Verifies functionality when the side on the bill is invalid."""
        vote = ResultData({"data" : self.BILL1, "outcome" : "Random Value"})
        result = member_analyze._extract_single_voting_stance(vote)
        self.assertEquals(result, [])

    def test_extract_single_voting_stance_for(self):
        """ Verifies stances for a single bill FOR are extracted."""
        vote = ResultData({"data" : self.BILL1, "outcome" : outcomes.FOR})
        result = member_analyze._extract_single_voting_stance(vote)
        self.assertEqual(len(result), len(self.bill1.stances_for))
        for stance1, stance2 in zip(result, self.bill1.stances_for):
            self.assertTrue(stance1.total_match(stance2))

    def test_extract_single_voting_stance_agn(self):
        """ Verifies stances for a single bill AGN are extracted."""
        vote = ResultData({"data" : self.BILL1, "outcome" : outcomes.AGN})
        result = member_analyze._extract_single_voting_stance(vote)
        self.assertEqual(len(result), len(self.bill1.stances_agn))
        for stance1, stance2 in zip(result, self.bill1.stances_agn):
            self.assertTrue(stance1.total_match(stance2))

    def test_extract_voting_stances(self):
        """ Verifies stances for all bill are extracted."""
        member_analyze.extract_voting_stances(self.member)

        answer = (self.bill1.stances_for + self.bill2.stances_agn +
            self.bill3.stances_for)

        self.assertEqual(len(self.member.stances), len(answer))
        for stance1, stance2 in zip(self.member.stances, answer):
            self.assertTrue(stance1.total_match(stance2))

    def test_extract_single_relation_stances_invalid_relation(self):
        """ Verifies functionality when the group provided is invalid."""
        relation = Relation()
        relation.group = "I DON'T EXIST"
        result = member_analyze._extract_single_relation_stances(relation)
        self.assertEqual(result, [])

    def test_extract_single_relation_stances(self):
        """ Verifies a single group's stances are extracted."""
        relation = Relation()
        relation.group = self.GROUP1
        result = member_analyze._extract_single_relation_stances(relation)

        self.assertEqual(len(result), len(self.group1.stances))
        for stance1, stance2 in zip(result, self.group1.stances):
            # Ensure that the source relation is addded as the source.
            self.assertEqual(stance1.relation, relation)
            self.assertTrue(stance1.total_match(stance2))

    def test_extract_relations_stances(self):
        """ Verifies all group stances are extracted."""
        member_analyze.extract_relations_stances(self.member)

        # Stances from friends of the member should be in pro_rel_stances
        self.assertEqual(len(self.member.pro_rel_stances), len(self.group1.stances))
        for stance1, stance2 in zip(self.member.pro_rel_stances, self.group1.stances):
            self.assertTrue(stance1.total_match(stance2))

        # Stances from enemies of the member should be in con_rel_stances
        self.assertEqual(len(self.member.con_rel_stances), len(self.group2.stances))
        for stance1, stance2 in zip(self.member.con_rel_stances, self.group2.stances):
            self.assertTrue(stance1.total_match(stance2))