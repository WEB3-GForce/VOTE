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
from src.classes.bill import Bill
from src.classes.member import Member
from src.classes.relation import Relation
from src.classes.stance import Stance
from src.classes.data import importance
from src.classes.data.result_data import ResultData
from src.constants import database as db_constants
from src.constants import outcomes
from src.constants import stance_sort_key
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

    def test_infer_single_relation_stances_invalid_relation(self):
        """ Verifies functionality when the group provided is invalid."""
        relation = Relation()
        relation.group = "I DON'T EXIST"
        result = member_analyze._infer_single_relation_stances(relation)
        self.assertEqual(result, [])

    def test_infer_single_relation_stances(self):
        """ Verifies a single group's stances are extracted."""
        relation = Relation()
        relation.group = self.GROUP1
        result = member_analyze._infer_single_relation_stances(relation)

        self.assertEqual(len(result), len(self.group1.stances))
        for stance1, stance2 in zip(result, self.group1.stances):
            # Ensure that the source relation is added as the source.
            self.assertEqual(stance1.relation, relation)
            self.assertTrue(stance1.total_match(stance2))

    def test_infer_relations_stances(self):
        """ Verifies all group stances are extracted."""
        member_analyze.infer_relations_stances(self.member)

        # Stances from friends of the member should be in pro_rel_stances
        self.assertEqual(len(self.member.pro_rel_stances), len(self.group1.stances))
        for stance1, stance2 in zip(self.member.pro_rel_stances, self.group1.stances):
            self.assertTrue(stance1.total_match(stance2))

        # Stances from enemies of the member should be in con_rel_stances
        self.assertEqual(len(self.member.con_rel_stances), len(self.group2.stances))
        for stance1, stance2 in zip(self.member.con_rel_stances, self.group2.stances):
            self.assertTrue(stance1.total_match(stance2))

    def generate_member_with_stances(self):
        member = Member()
        credo_stance = Stance()
        credo_stance.issue = "Credo"
        credo_stance.side = outcomes.PRO

        stances_stance = Stance()
        stances_stance.issue = "Stances"
        stances_stance.side = outcomes.CON

        pro_rel_stance = Stance()
        pro_rel_stance.issue = "Pro-Relation"
        pro_rel_stance.side = outcomes.PRO

        member.credo.append(credo_stance)
        member.stances.append(stances_stance)
        member.pro_rel_stances.append(pro_rel_stance)
        return member

    def test__match_stances_helper_match_credo(self):
        """ Verifies member.credo stances are matched."""
        member = self.generate_member_with_stances()
        stances = member.credo

        result = member_analyze._match_stances_helper(member, stances)
        self.assertEqual(result, stances)

    def test__match_stances_helper_match_stances(self):
        """ Verifies member.stances stances are matched."""
        member = self.generate_member_with_stances()
        stances = member.stances

        result = member_analyze._match_stances_helper(member, stances)
        self.assertEqual(result, stances)

    def test__match_stances_helper_match_pro_rel_stances(self):
        """ Verifies member.pro_rel_stances stances are matched."""
        member = self.generate_member_with_stances()
        stances = member.pro_rel_stances

        result = member_analyze._match_stances_helper(member, stances)
        for entry in result:
            self.assertTrue(entry in stances)

    def test__match_stances_helper_match_multiple_stances(self):
        """ Verifies member stances from multiple sources are matched."""
        member = self.generate_member_with_stances()
        stances = member.credo + member.pro_rel_stances

        result = member_analyze._match_stances_helper(member, stances)
        for entry in result:
            self.assertTrue(entry in stances)

    def test__match_stances_helper_extra_stances(self):
        """ Verifies that extra stances in the filter stances list are not added."""
        member = self.generate_member_with_stances()
        stances = member.credo + member.pro_rel_stances

        stance = Stance()
        stance.issue = "Not Found"
        stance.side = outcomes.PRO
        stances.append(stance)

        result = member_analyze._match_stances_helper(member, stances)
        answer = member.credo + member.pro_rel_stances
        for entry in result:
            self.assertTrue(entry in answer)

    def test_match_stances_for(self):
        """ Verifies stances are matched by the bill FOR stances."""
        member = self.generate_member_with_stances()

        bill = Bill()
        bill.stances_for = member.credo
        bill.stances_agn = member.pro_rel_stances

        result = member_analyze.match_stances(member, bill, outcomes.FOR)
        for entry in result:
            self.assertTrue(entry in bill.stances_for)

    def test_match_stances_agn(self):
        """ Verifies the returned stances are sorted by importance."""
        member = Member()
        member.stance_sort_key = stance_sort_key.EQUITY
        credo_stance = Stance()
        credo_stance.issue = "Credo"
        credo_stance.side = outcomes.PRO
        credo_stance.importance = importance.B

        stances_stance1 = Stance()
        stances_stance1.issue = "Stances"
        stances_stance1.side = outcomes.CON
        stances_stance1.importance = importance.D

        stances_stance2 = Stance()
        stances_stance2.issue = "An Outcomes"
        stances_stance2.side = outcomes.PRO
        stances_stance2.importance = importance.A

        pro_rel_stance = Stance()
        pro_rel_stance.issue = "Pro-Relation"
        pro_rel_stance.side = outcomes.PRO
        pro_rel_stance.importance = importance.C

        member.credo.append(credo_stance)
        member.stances.append(stances_stance1)
        member.stances.append(stances_stance2)
        member.pro_rel_stances.append(pro_rel_stance)

        bill = Bill()
        bill.stances_for = member.credo + member.stances
        bill.stances_agn = member.pro_rel_stances

        result = member_analyze.match_stances(member, bill, outcomes.FOR)
        sorted_answer = [stances_stance2, credo_stance, stances_stance1]
        self.assertEqual(result, sorted_answer)