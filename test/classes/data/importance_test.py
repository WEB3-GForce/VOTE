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

from src.classes.data import importance

class ImportanceTest(unittest.TestCase):
    """ Test suite for importance."""

    def test_eq(self):
        """Test the equality function for importance"""
        self.assertEqual(importance.A, importance.A)
        self.assertEqual(importance.B, importance.B)
        self.assertEqual(importance.C, importance.C)
        self.assertEqual(importance.D, importance.D)

    def test_ne(self):
        """Test the non-equality function for importance"""
        self.assertNotEqual(importance.A, importance.B)
        self.assertNotEqual(importance.A, importance.C)
        self.assertNotEqual(importance.A, importance.D)
        self.assertNotEqual(importance.A, importance.Z)

    def test_lt(self):
        """Test the less than function for importance"""
        self.assertLess(importance.B, importance.A)
        self.assertLess(importance.C, importance.B)
        self.assertLess(importance.D, importance.C)
        self.assertLess(importance.Z, importance.D)
        self.assertLess(importance.Z, importance.A)

    def test_gt(self):
        """Test the greater than function for importance"""
        self.assertGreater(importance.A, importance.B)
        self.assertGreater(importance.B, importance.C)
        self.assertGreater(importance.C, importance.D)
        self.assertGreater(importance.D, importance.Z)
        self.assertGreater(importance.A, importance.Z)

    def test_le(self):
        """Test the less than or equal to function for importance"""
        self.assertLessEqual(importance.B, importance.A)
        self.assertLessEqual(importance.B, importance.B)

    def test_ge(self):
        """Test the greater than or equal to function for importance"""
        self.assertGreaterEqual(importance.A, importance.B)
        self.assertGreaterEqual(importance.A, importance.A)
