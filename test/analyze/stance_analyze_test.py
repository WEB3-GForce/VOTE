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

from src.analyze import stance_analyze
from src.classes.member import Member
from src.classes.relation import Relation
from src.classes.stance import Stance
from src.classes.data import importance
from src.constants import database as db_constants
from src.constants import outcomes
from src.constants import stance_sort_key
from src.database.pymongodb import PymongoDB
from src.scripts.database import load_data

class StanceAnalyzeTest(unittest.TestCase):
    """ Test suite for util.py"""

    @classmethod
    def drop_collections(cls, DB):
        """Removes all the collections from a DB"""
        for collection_name in db_constants.DB_COLLECTIONS:
            DB.DB.drop_collection(collection_name)

    @classmethod
    def setUpClass(cls):
        # Make sure that the database is clean before this class is run.
        DB = PymongoDB()
        StanceAnalyzeTest.drop_collections(DB)

        # Ignore all output to the screen.
        sys.stdout = StringIO()

    @classmethod
    def tearDownClass(cls):
        sys.stdout = sys.__stdout__

    def setUp(self):
        self.DB = PymongoDB.get_db()
        load_data.load_data()

    def tearDown(self):
        # Delete the database each time to start fresh.
        StanceAnalyzeTest.drop_collections(self.DB)


    def test_normative_stance_not_in_db(self):
        """Verifies function returns False when the norm is not in the DB."""
        stance = Stance()
        stance.issue = "I Don't Exist"

        result = stance_analyze.normative_stance(stance)
        self.assertFalse(result)

    def test_normative_stance_no_norm(self):
        """Verifies function returns False when the Issue has no norm."""
        stance = Stance()
        stance.issue = "decision_analyze_test_no_norm"

        result = stance_analyze.normative_stance(stance)
        self.assertFalse(result)

    def test_normative_stance_norm_doesnt_match(self):
        """Verifies function returns False when the stance does not match the norm."""
        stance = Stance()
        stance.issue = "decision_analyze_test_norm"
        stance.side = outcomes.CON

        result = stance_analyze.normative_stance(stance)
        self.assertFalse(result)

    def test_normative_stance_norm_match(self):
        """Verifies function returns True when the stance matches the norm."""
        stance = Stance()
        stance.issue = "decision_analyze_test_norm"
        stance.side = outcomes.PRO

        result = stance_analyze.normative_stance(stance)
        self.assertTrue(result)

    def test_collect_normative_stances(self):
        """Verifies function returns only normative stances."""
        stance = Stance()
        stance.issue = "decision_analyze_test_norm"
        stance.side = outcomes.PRO

        agn_norm_stance = Stance()
        agn_norm_stance.issue = "decision_analyze_test_norm"
        agn_norm_stance.side = outcomes.CON

        result = stance_analyze.collect_normative_stances([stance, agn_norm_stance])
        self.assertEquals(len(result), 1)
        self.assertEquals(result[0], stance)

    def test_collect_normative_stances_no_duplicates(self):
        """Verifies function return does not contain duplicates."""
        stance = Stance()
        stance.issue = "decision_analyze_test_norm"
        stance.side = outcomes.PRO

        result = stance_analyze.collect_normative_stances([stance, stance])
        self.assertEquals(len(result), 1)
        self.assertEquals(result[0], stance)

    def test_collect_normative_stances_no_result(self):
        """Verifies function return nothing if there are no normative stances."""
        agn_norm_stance = Stance()
        agn_norm_stance.issue = "decision_analyze_test_norm"
        agn_norm_stance.side = outcomes.CON

        result = stance_analyze.collect_normative_stances([agn_norm_stance, agn_norm_stance])
        self.assertEquals(len(result), 0)

    def generate_stance_array(self):
        """Generates the stance array for the _compare_stance tests"""
        stance1 = Stance()
        stance1.importance = importance.B
        relation1 = Relation()
        relation1.importance = importance.C
        stance1.relation = relation1

        stance2 = Stance()
        stance2.importance = importance.B
        relation2 = Relation()
        relation2.importance = importance.A
        stance2.relation = relation2

        stance3 = Stance()
        stance3.importance = importance.C
        relation3 = Relation()
        relation3.importance = importance.B
        stance3.relation = relation3

        stance4 = Stance()
        stance4.importance = importance.D
        relation4 = Relation()
        relation4.importance = importance.A
        stance4.relation = relation4
        return [stance1, stance2, stance3, stance4]


    def test_sort_stances_key_given(self):
        """Verifies sort when the member key is defined."""
        stances = self.generate_stance_array()
        member = Member()
        member.stance_sort_key = stance_sort_key.LOYALTY

        stance_analyze.sort_stances(stances, member)
        for i in range(0, len(stances) - 1):
            self.assertEqual(stances[i]._sort_key, stance_sort_key.LOYALTY)
            self.assertTrue(stances[i].sort_key >= stances[i + 1].sort_key)

    def test_sort_stances_key_not_given(self):
        """Verifies sort when the member key is not defined."""
        stances = self.generate_stance_array()
        member = Member()

        stance_analyze.sort_stances(stances, member)
        for i in range(0, len(stances) - 1):
            self.assertEqual(stances[i]._sort_key, stance_sort_key.EQUITY)
            self.assertTrue(stances[i].sort_key >= stances[i + 1].sort_key)

    def test_group_stances(self):
        """Verifies stances are grouped by stance and side."""
        stance1 = Stance()
        stance1.issue = "Apples"
        stance1.side = outcomes.PRO

        stance2 = Stance()
        stance2.issue = "Oranges"
        stance2.side = outcomes.PRO

        stance3 = Stance()
        stance3.issue = "Banana"
        stance3.side = outcomes.CON

        stance4 = Stance()
        stance4.issue = "Apples"
        stance4.side = outcomes.CON

        stance5 = Stance()
        stance5.issue = "Banana"
        stance5.side = outcomes.CON

        stance6 = Stance()
        stance6.issue = "Oranges"
        stance6.side = outcomes.CON

        input_list = [stance1, stance2, stance3, stance4, stance5, stance6]
        correct_list = [stance4, stance1, stance3, stance5, stance6, stance2]

        stance_analyze.group_stances(input_list)
        self.assertEquals(input_list, correct_list)
