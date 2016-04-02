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

from src.classes.stance import Stance
from src.classes.relation import Relation
from src.constants import database as db_constants
from src.constants import importance
from src.constants import outcomes
from src.constants import stance_sort_key
from src.util import util

class UtilTest(unittest.TestCase):
    """ Test suite for util.py"""

    def test_intersection(self):
        """Verify only the intersection of the list is included."""
        stance = Stance()
        stance.issue = "Test"
        stance.side = outcomes.PRO

        stance2 = Stance()
        stance2.issue = "Test"
        stance2.side = outcomes.PRO

        stance3 = Stance()
        stance3.issue = "Test"
        stance3.side = outcomes.CON

        eq_fun = lambda stance1, stance2: stance1.match(stance2)
        result = util.intersection([stance, stance3], [stance2], eq_fun)
        self.assertEquals(result, [stance])

    def test_remove_duplicates(self):
        """Verify only the intersection of the list is included."""
        stance = Stance()
        stance.issue = "Test"
        stance.side = outcomes.PRO

        stance2 = Stance()
        stance2.issue = "Something different"
        stance2.side = outcomes.PRO

        data = [stance, stance, stance2, stance2, stance, stance2, stance]
        result = util.remove_duplicates(data)

        self.assertEquals(len(result), 2)
        self.assertTrue(stance in result)
        self.assertTrue(stance2 in result)

    def test_remove_less_important_stances_only_one(self):
        """ Verifies remove less importance where only one is left."""
        stance1 = Stance()
        stance1.importance = importance.A

        stance2 = Stance()
        stance2.importance = importance.B

        stance3 = Stance()
        stance3.importance = importance.C

        answer = [stance1]
        result = util.remove_less_important_stances([stance1, stance2, stance3])
        self.assertEqual(len(result), len(answer))
        for stance1, stance2 in zip(result, answer):
            self.assertEquals(stance1, stance2)

    def test_remove_less_stances_important(self):
        """ Verifies remove less importance where two are left."""
        stance1 = Stance()
        stance1.importance = importance.B

        stance2 = Stance()
        stance2.importance = importance.B

        stance3 = Stance()
        stance3.importance = importance.C

        answer = [stance1, stance2]
        result = util.remove_less_important_stances([stance1, stance2, stance3])
        self.assertEqual(len(result), len(answer))
        for stance1, stance2 in zip(result, answer):
            self.assertEquals(stance1, stance2)

    def generate_stance(self, stance_importance, relation_importance):
        """Generates stances for testing with sort keys"""
        stance = Stance()
        stance.importance = stance_importance
        relation = Relation()
        relation.importance = relation_importance
        stance.relation = relation
        stance.sort_key = stance_sort_key.LOYALTY
        return stance

    def test_remove_less_important_stances_loyalty(self):
        """ Verifies remove less importance when using a sort key."""
        stance1 = self.generate_stance(importance.C, importance.A)
        stance2 = self.generate_stance(importance.C, importance.A)
        stance3 = self.generate_stance(importance.A, importance.B)

        answer = [stance1, stance2]
        result = util.remove_less_important_stances([stance1, stance2, stance3])
        self.assertEqual(len(result), len(answer))
        for stance1, stance2 in zip(result, answer):
            self.assertEquals(stance1, stance2)

    def test_remove_less_important_stances_sorts_stances(self):
        """ Verifies function works properly when on unsorted arrays."""
        stance1 = self.generate_stance(importance.C, importance.A)
        stance2 = self.generate_stance(importance.C, importance.A)
        stance3 = self.generate_stance(importance.A, importance.B)

        answer = [stance2, stance1]
        data = [stance3, stance2, stance3, stance1]
        result = util.remove_less_important_stances(data)
        self.assertEqual(len(result), len(answer))
        for stance1, stance2 in zip(result, answer):
            self.assertEquals(stance1, stance2)

    def generate_collect_type_stance_array(self):
        """Generates the stance array for the collect_type tests"""
        stance1 = Stance()
        stance1.source_db = db_constants.MEMBERS

        stance2 = Stance()
        stance1.source_db = db_constants.BILLS

        stance3 = Stance()
        stance1.source_db = db_constants.GROUPS
        return [stance1, stance2, stance3]

    def test_collect_source_type(self):
        """ Verifies collect type return stances only with the specified source."""
        array = self.generate_collect_type_stance_array()
        result = util.collect_source_db_type(db_constants.MEMBERS, array)

        for stance in result:
            self.assertEquals(stance.source_db, db_constants.MEMBERS)

    def test_collect_groups_stances(self):
        """ Verifies the function only return stances from groups."""
        array = self.generate_collect_type_stance_array()
        result = util.collect_group_stances(array)

        for stance in result:
            self.assertEquals(stance.source_db, db_constants.GROUPS)

    def test_collect_credo_stances(self):
        """ Verifies the function only return stances from members."""
        array = self.generate_collect_type_stance_array()
        result = util.collect_credo_stances(array)

        for stance in result:
            self.assertEquals(stance.source_db, db_constants.MEMBERS)

    def test_collect_bill_stances(self):
        """ Verifies the function only return stances from bills."""
        array = self.generate_collect_type_stance_array()
        result = util.collect_bill_stances(array)

        for stance in result:
            self.assertEquals(stance.source_db, db_constants.BILLS)
