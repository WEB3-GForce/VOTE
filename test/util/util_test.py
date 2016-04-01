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
from src.constants import outcomes
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
        stance2.issue = "Test"
        stance2.side = outcomes.PRO

        data = [stance, stance, stance2, stance2, stance, stance2, stance]
        result = util.remove_duplicates(data)

        self.assertEquals(result, [stance, stance2])