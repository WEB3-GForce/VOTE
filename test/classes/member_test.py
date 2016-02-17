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

from src.classes.member import Member

class MemberTest(unittest.TestCase):
    """ Test suite for Member."""
    
    def setUp(self):
        # This is fake data. Do not use it to make assumptions about how
        # data will look in the actual system.
        self.input_hash = {"full_name": "Timothy Peter Johnson",
            "first_name": "TIMOTHY",
            "last_name": "JOHNSON",
            "gender" : "MALE",
            "district": "SD-AL",
            "term_start": 1986,
            "term_end": 1990,
            "party": "DEM",
            "voting_record": [["HR-4800", "FOR"], ["HR-3", "FOR"]],
            "credo": ["Some credos"],
            "relations": ["Some Relationships..."],
            "pro_rel_stances": ["Some Stances.."],
            "stances": ["Some more stances"],
            "stance_sort_key": None,
            "committees": ["HOUSE-AGRICULTURE", "HOUSE-VETERANS-AFFAIRS"],
            "con_rel_stances": []
            }        
    
    def test_init_default(self):
        """Tests that default values are set for instance variables"""
        member = Member()

        self.assertEqual(member.full_name, "")
        self.assertEqual(member.first_name,"")
        self.assertEqual(member.last_name, "")
        self.assertEqual(member.gender, None)
        self.assertEqual(member.district, "")
        self.assertEqual(member.term_start, None)
        self.assertEqual(member.term_end, None)
        self.assertEqual(member.party, None)

        self.assertEqual(member.voting_record, [])
        self.assertEqual(member.credo, [])
        self.assertEqual(member.relations, [])

        self.assertEqual(member.stances, [])
        self.assertEqual(member.pro_rel_stances, [])
        self.assertEqual(member.con_rel_stances, [])
        self.assertEqual(member.stance_sort_key, None)
        
    def test_init_hash(self):
        """ Verifies that input data from a hash is properly set."""
        member = Member(self.input_hash)        
        for key, value in self.input_hash.iteritems():
            self.assertEqual(value, member.__dict__[key])
        for key, value in member.__dict__.iteritems():
            self.assertEqual(value, self.input_hash[key])

    def test_init_hash_default(self):
        """ Verifies defaults are still defined when a hash is provided."""
        self.input_hash.pop("full_name")
        member = Member(self.input_hash)        
        for key, value in self.input_hash.iteritems():
            self.assertEqual(value, member.__dict__[key])
        self.assertEqual(member.full_name, "")