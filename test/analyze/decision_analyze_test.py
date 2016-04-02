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

from src.analyze import decision_analyze
from src.classes.decision import Decision
from src.classes.relation import Relation
from src.classes.stance import Stance
from src.classes.data import importance
from src.constants import database as db_constants
from src.constants import outcomes
from src.constants import stance_sort_key
from src.database.pymongodb import PymongoDB
from src.scripts.database import load_data

class DecisionAnalyzeTest(unittest.TestCase):
    """ Test suite for decision_analyze.py."""

    @classmethod
    def drop_collections(cls, DB):
        """Removes all the collections from a DB"""
        for collection_name in db_constants.DB_COLLECTIONS:
            DB.DB.drop_collection(collection_name)


    @classmethod
    def setUpClass(cls):
        # Make sure that the database is clean before this class is run.
        DB = PymongoDB()
        DecisionAnalyzeTest.drop_collections(DB)

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
        DecisionAnalyzeTest.drop_collections(self.DB)

    def generate_stance_array(self):
        """Generates the stance array for the _compare_stance tests"""
        stance1 = Stance()
        stance1.importance = importance.B
        relation1 = Relation()
        relation1.importance = importance.A
        stance1.relation = relation1
        stance1.sort_key = stance_sort_key.LOYALTY

        stance2 = Stance()
        stance2.importance = importance.C
        relation2 = Relation()
        relation2.importance = importance.A
        stance2.relation = relation2
        stance2.sort_key = stance_sort_key.LOYALTY

        stance3 = Stance()
        stance3.importance = importance.D
        relation3 = Relation()
        relation3.importance = importance.A
        stance3.relation = relation3
        stance3.sort_key = stance_sort_key.LOYALTY
        return [stance1, stance2, stance3]

    def test_compare_stances_neither(self):
        """ Verifies compare stances returns the empty list when both
        sides are equal."""
        fors = self.generate_stance_array()
        agns = self.generate_stance_array()

        result = decision_analyze._compare_stances(fors, agns)
        self.assertEqual(result, [])

    def test_compare_stances_sort(self):
        """ Verifies compare stances sorts arrays it gets by sort_key."""
        fors = self.generate_stance_array()
        agns = self.generate_stance_array()

        # Swap the order so that agns will win if the list is not sorted properly
        # beforhand
        temp = fors[0]
        fors[0] = fors[2]
        fors[2] = temp

        result = decision_analyze._compare_stances(fors, agns)
        self.assertEqual(result, [])

    def test_compare_stances_fors(self):
        """ Verifies compare stances returns properly when FORS win."""
        fors = self.generate_stance_array()
        agns = self.generate_stance_array()

        stance2 = fors[1]
        stance2.importance = importance.B
        stance2.relation.importance = importance.A

        result = decision_analyze._compare_stances(fors, agns)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], outcomes.FOR)
        self.assertEqual(len(result[1]), 1)
        self.assertEquals(result[1][0], stance2)

    def test_compare_stances_agns(self):
        """ Verifies compare stances returns properly when AGNS win."""
        fors = self.generate_stance_array()
        agns = self.generate_stance_array()

        agns[1].importance = importance.B
        agns[1].relation.importance = importance.A
        agns[2].importance = importance.B
        agns[2].relation.importance = importance.A

        result = decision_analyze._compare_stances(fors, agns)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], outcomes.AGN)
        self.assertEqual(len(result[1]), 2)
        for stance1, stance2 in zip(result[1], agns[1:]):
            self.assertEquals(stance1, stance2)

    def test_compare_stances_longer_wins(self):
        """ Verifies compare stances returns properly when both arrays are the
        same except one is longer.."""
        fors = self.generate_stance_array()
        agns = self.generate_stance_array()

        stance4 = Stance()
        stance4.importance = importance.D
        stance4.sort_key = stance_sort_key.LOYALTY
        agns.append(stance4)

        result = decision_analyze._compare_stances(fors, agns)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], outcomes.AGN)
        self.assertEqual(len(result[1]), 1)
        self.assertEquals(result[1][0], stance4)

    def test_compare_stances_fors_empty(self):
        """ Verifies that the base_stance is created properly when FORS are
        empty."""
        fors = []
        agns = self.generate_stance_array()

        result = decision_analyze._compare_stances(fors, agns)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], outcomes.AGN)

    def test_compare_stances_agns_empty(self):
        """ Verifies that the base_stance is created properly when AGNS are
        empty."""
        fors = self.generate_stance_array()
        agns = []

        result = decision_analyze._compare_stances(fors, agns)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], outcomes.FOR)

    def test_MI_stances(self):
        """Verifies MI_stances properly compares all for and agn stances."""
        decision = Decision()
        decision.for_stances = self.generate_stance_array()
        decision.agn_stances = self.generate_stance_array()

        decision.for_stances[1].importance = importance.B
        result = decision_analyze._MI_stances(decision)

        self.assertEqual(result[0], outcomes.FOR)
        self.assertGreater(len(result[1]), 0)

    def test_MI_stance_with_source(self):
        """Verifies MI_stance properly compares stances from the given source."""
        decision = Decision()
        decision.for_stances = self.generate_stance_array()
        decision.agn_stances = self.generate_stance_array()

        decision.agn_stances[2].source_db = db_constants.MEMBERS
        result = decision_analyze._MI_stances(decision, db_constants.MEMBERS)

        self.assertEqual(result[0], outcomes.AGN)
        self.assertGreater(len(result[1]), 0)

    def test_update_MI_stances(self):
        """Verifies _update_MI_stance properly updates all MI stances."""
        decision = Decision()
        decision.for_stances = self.generate_stance_array()
        decision.agn_stances = self.generate_stance_array()

        decision.agn_stances[0].importance = importance.A
        decision.for_stances[0].source_db = db_constants.MEMBERS
        decision.agn_stances[0].source_db = db_constants.BILLS
        decision.for_stances[1].source_db = db_constants.GROUPS

        decision.for_norms = self.generate_stance_array()
        decision.agn_norms = self.generate_stance_array()
        decision.for_norms[0].importance = importance.A

        decision_analyze._update_MI_stances(decision)
        self.assertEqual(decision.MI_stance[0], outcomes.AGN)
        self.assertEqual(decision.MI_credo[0], outcomes.FOR)
        self.assertEqual(decision.MI_record[0], outcomes.AGN)
        self.assertEqual(decision.MI_group[0], outcomes.FOR)
        self.assertEqual(decision.MI_norm[0], outcomes.FOR)

    def test_update_regular_stances_norms(self):
        """Verifies function properly updates for and agn norms."""
        stance = Stance()
        stance.issue = "decision_analyze_test_norm"
        stance.side = outcomes.PRO

        stance2 = Stance()
        stance2.issue = "decision_analyze_test_norm"
        stance2.side = outcomes.PRO
        stance2.importance = importance.C

        decision = Decision()
        decision.for_stances = [stance]
        decision.agn_stances = [stance2]

        decision_analyze._update_regular_stances(decision)
        self.assertEquals(decision.for_norms, decision.for_stances)
        self.assertEquals(decision.agn_norms, decision.agn_stances)

    def test_update_regular_stances_bill_not_found(self):
        """Verifies function does not update bill norms when bill not found."""
        decision = Decision()
        decision.bill = "I don't exist"

        decision_analyze._update_regular_stances(decision)
        self.assertEquals(decision.for_bill_norms, [])
        self.assertEquals(decision.agn_bill_norms, [])

    def test_update_regular_stances_bill_found(self):
        """Verifies function updates bill norms when the bill is found."""
        decision = Decision()
        decision.bill = "decision_analyze_test"

        decision_analyze._update_regular_stances(decision)
        self.assertEquals(len(decision.for_bill_norms), 1)
        self.assertEquals(len(decision.agn_bill_norms), 1)

    def test_update_regular_stances_groups(self):
        """Verifies function updates group stances"""
        stance = Stance()
        stance.source_db = db_constants.GROUPS

        stance2 = Stance()
        stance2.importance = importance.C
        stance2.source_db = db_constants.GROUPS

        decision = Decision()
        decision.for_stances = [stance]
        decision.agn_stances = [stance2]

        decision_analyze._update_regular_stances(decision)
        self.assertEquals(decision.groups_for, decision.for_stances)
        self.assertEquals(decision.groups_agn, decision.agn_stances)

    def test_update_regular_stances_split_groups(self):
        """Verifies function detects split groups"""
        stance = Stance()
        stance.source = "Split Group"
        stance.source_db = db_constants.GROUPS

        stance2 = Stance()
        stance2.importance = importance.C
        stance2.source = "Split Group"
        stance2.source_db = db_constants.GROUPS

        different_stance = Stance()
        different_stance.source = "Different Group"
        different_stance.source_db = db_constants.GROUPS


        decision = Decision()
        decision.for_stances = [stance, different_stance]
        decision.agn_stances = [stance2]

        decision_analyze._update_regular_stances(decision)
        self.assertTrue(stance in decision.split_group)
        self.assertTrue(stance2 in decision.split_group)
        self.assertTrue(different_stance not in decision.split_group)

    def test_update_regular_stances_split_groups_no_match(self):
        """Verifies function detects split groups"""
        stance = Stance()
        stance.source = "Split Group"
        stance.source_db = db_constants.GROUPS

        different_stance = Stance()
        different_stance.source = "Different Group"
        different_stance.source_db = db_constants.GROUPS


        decision = Decision()
        decision.for_stances = [stance]
        decision.agn_stances = [different_stance]

        decision_analyze._update_regular_stances(decision)
        self.assertEquals(decision.split_group, [])


    def test_update_regular_stances_split_bills(self):
        """Verifies function recognizes split bills"""
        stance = Stance()
        stance.source = "decision_analyze_test"
        stance.source_db = db_constants.BILLS

        stance2 = Stance()
        stance2.importance = importance.C
        stance2.source = "decision_analyze_test"
        stance2.source_db = db_constants.BILLS

        decision = Decision()
        decision.for_stances = [stance]
        decision.agn_stances = [stance2]

        decision_analyze._update_regular_stances(decision)
        self.assertTrue(stance in decision.split_record)
        self.assertTrue(stance2 in decision.split_record)

    def test_update_regular_stances_split_bills_no_fors(self):
        """Verifies there is no split record when there are no for stances"""

        stance2 = Stance()
        stance2.importance = importance.C
        stance2.source = "decision_analyze_test"
        stance2.source_db = db_constants.BILLS

        decision = Decision()
        decision.for_stances = []
        decision.agn_stances = [stance2]

        decision_analyze._update_regular_stances(decision)
        self.assertEquals(decision.split_record, [])

    def test_update_regular_stances_split_bills_no_agns(self):
        """Verifies there is no split record when there are no agn stances"""

        stance = Stance()
        stance.source = "decision_analyze_test"
        stance.source_db = db_constants.BILLS

        decision = Decision()
        decision.for_stances = [stance]
        decision.agn_stances = []

        decision_analyze._update_regular_stances(decision)
        self.assertEquals(decision.split_record, [])

    def test_update_regular_stances_split_credo(self):
        """Verifies function recognizes a split credo"""
        stance = Stance()
        stance.source = "A Member"
        stance.source_db = db_constants.MEMBERS

        stance2 = Stance()
        stance2.importance = importance.C
        stance2.source = "A Member"
        stance2.source_db = db_constants.MEMBERS

        decision = Decision()
        decision.for_stances = [stance]
        decision.agn_stances = [stance2]

        decision_analyze._update_regular_stances(decision)
        self.assertTrue(stance in decision.split_credo)
        self.assertTrue(stance2 in decision.split_credo)

    def test_update_regular_stances_split_credo_no_fors(self):
        """Verifies there is no split credo when there are no for stances"""

        stance2 = Stance()
        stance2.importance = importance.C
        stance2.source = "A Member"
        stance2.source_db = db_constants.MEMBERS

        decision = Decision()
        decision.for_stances = []
        decision.agn_stances = [stance2]

        decision_analyze._update_regular_stances(decision)
        self.assertEquals(decision.split_credo, [])

    def test_update_regular_stances_split_credo_no_ags(self):
        """Verifies there is no split credo when there are no agn stances"""

        stance = Stance()
        stance.source = "A Member"
        stance.source_db = db_constants.MEMBERS

        decision = Decision()
        decision.for_stances = [stance]
        decision.agn_stances = []

        decision_analyze._update_regular_stances(decision)
        self.assertEquals(decision.split_credo, [])

    def test_update_decision_metrics(self):
        """Verifies all decision metrics are updated properly."""
        decision = Decision()
        decision.bill = "decision_analyze_test"
        decision.for_stances = self.generate_stance_array()
        decision.agn_stances = self.generate_stance_array()

        decision.agn_stances[0].importance = importance.A
        decision.for_stances[0].source_db = db_constants.MEMBERS
        decision.agn_stances[0].source_db = db_constants.BILLS

        decision.for_stances[1].source_db = db_constants.GROUPS
        decision.for_stances[1].issue = "decision_analyze_test_norm"
        decision.for_stances[1].side = outcomes.PRO
        decision.for_stances[1].importance = importance.C

        decision_analyze.update_decision_metrics(decision)

        self.assertGreater(len(decision.for_stances), 0)
        self.assertGreater(len(decision.agn_stances), 0)
        self.assertGreater(len(decision.agn_stances), 0)
        self.assertGreater(len(decision.groups_for), 0)
        self.assertEqual(len(decision.groups_agn), 0)
        self.assertGreater(len(decision.for_norms), 0)
        self.assertEqual(len(decision.agn_norms), 0)
        self.assertGreater(len(decision.for_bill_norms), 0)
        self.assertGreater(len(decision.agn_bill_norms), 0)
        self.assertEqual(decision.split_credo, [])
        self.assertEqual(decision.split_group, [])
        self.assertEqual(decision.split_record, [])
        self.assertEqual(decision.MI_stance[0], outcomes.AGN)
        self.assertEqual(decision.MI_credo[0], outcomes.FOR)
        self.assertEqual(decision.MI_record[0], outcomes.AGN)
        self.assertEqual(decision.MI_group[0], outcomes.FOR)
        self.assertEqual(decision.MI_norm[0], outcomes.FOR)
