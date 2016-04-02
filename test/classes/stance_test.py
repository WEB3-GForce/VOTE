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
from src.classes.data import importance
from src.constants import stance_sort_key

class StanceTest(unittest.TestCase):
    """ Test suite for Stance."""

    def setUp(self):
        # This is fake data. Do not use it to make assumptions about how
        # data will look in the actual system.
        self.relation = Relation()
        self.relation.importance = importance.D
        self.input_hash = {"importance": importance.A,
            "issue": "CONSTITUTION",
            "relation": self.relation,
            "siblings": ["Sib1", "Sib2"],
            "side": "PRO",
            "_sort_key": "Some initial random value",
            "source": "PARRIS",
            "source_db": "member"}
        self.input_hash2 = {"importance": importance.A,
            "issue": "CONSTITUTION",
            "relation": self.relation,
            "siblings": ["Sib1", "Sib2"],
            "side": "PRO",
            "_sort_key": "Some initial random value",
            "source": "PARRIS",
            "source_db": "member"}
        self.stance = Stance(self.input_hash)
        self.stance2 = Stance(self.input_hash2)

    def test_init_default(self):
        """Tests that default values are set for instance variables"""
        stance = Stance()

        self.assertEqual(stance.source, None)
        self.assertEqual(stance.source_db, None)
        self.assertEqual(stance.issue, None)
        self.assertEqual(stance.importance, None)
        self.assertEqual(stance.side, None)
        self.assertEqual(stance.relation, None)
        self.assertEqual(stance.siblings, [])
        self.assertEqual(stance._sort_key, None)


    def test_init_hash(self):
        """ Verifies that input data from a hash is properly set."""
        stance = Stance(self.input_hash)
        for key, value in self.input_hash.iteritems():
            self.assertEqual(value, stance.__dict__[key])

    def test_init_hash_default(self):
        """ Verifies defaults are still defined when a hash is provided."""
        self.input_hash.pop("source")
        stance = Stance(self.input_hash)
        for key, value in self.input_hash.iteritems():
            self.assertEqual(value, stance.__dict__[key])
        self.assertEqual(stance.source, None)

    def test_sort_key_undefined(self):
        """When sort_key is undefined, verifies the stance's importance is
        returned."""
        self.stance._sort_key = None
        self.assertEqual(self.stance.sort_key,
            self.stance.importance)

    def test_sort_key_equity(self):
        """Verifies that the EQUITY sort key is set properly."""
        self.stance.sort_key = stance_sort_key.EQUITY
        self.assertEqual(self.stance.sort_key,
            [self.stance.importance, self.relation.importance])

    def test_sort_key_loyalty(self):
        """Verifies that the LOYALTY sort key is set properly."""
        self.stance.sort_key = stance_sort_key.LOYALTY
        self.assertEqual(self.stance.sort_key,
            [self.relation.importance, self.stance.importance])

    def test_sort_key_no_relation(self):
        """Verifies relation_import is set to B if no relation provided."""
        self.stance.relation = None
        self.stance.sort_key = stance_sort_key.LOYALTY
        self.assertEqual(self.stance.sort_key,
            [importance.B, self.stance.importance])

    def test_sort_key_no_relation_importance(self):
        """Verifies relation_import is set to B if there is no relation
        importance."""
        self.relation.importance = None
        self.stance.sort_key = stance_sort_key.LOYALTY
        self.assertEqual(self.stance.sort_key,
            [importance.B, self.stance.importance])

    def test_sort_key_unknown(self):
        """Verifies sort_key can gracefully handle an unknown option."""
        self.stance._sort_key = None
        self.stance.sort_key = "I am an unknown sort key"
        self.assertEqual(self.stance.sort_key,
            self.stance.importance)

    def test_match_true(self):
        """Verifies that match returns true properly."""
        self.stance2.importance = importance.Z
        self.assertTrue(self.stance.match(self.stance2))

    def test_total_match_bad_side(self):
        """Verifies that match returns false when the sides differ."""
        self.stance2.side = "Something else"
        self.assertFalse(self.stance.total_match(self.stance2))

    def test_total_match_bad_issue(self):
        """Verifies that match returns false when the issues differ."""
        self.stance2.issue = "Something else"
        self.assertFalse(self.stance.total_match(self.stance2))

    def test_total_match_true(self):
        """Verifies that total match returns true properly."""
        self.assertTrue(self.stance.total_match(self.stance2))

    def test_total_match_false(self):
        """Verifies that total match returns false properly."""
        self.stance2.importance = importance.Z
        self.assertFalse(self.stance.total_match(self.stance2))
