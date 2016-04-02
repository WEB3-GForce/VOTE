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
from src.classes.stance import Stance
from src.constants import database as db_constants
from src.constants import outcomes
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
