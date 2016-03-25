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

from src.classes.decision import Decision

class DecisionTest(unittest.TestCase):
    """ Test suite for decision.py"""

    def setUp(self):
        # This is fake data. Do not use it to make assumptions about how
        # data will look in the actual system.
        self.input_hash = { "bill" : "some_bill",
            "member" : "some_member",
            "for_stances" : ["Some_stances_for"],
            "agn_stances" : ["Some_stances_agn"],
            "con_rel_for_stances" : ["Some_more_stances_for"],
            "con_rel_agn_stances" : ["Some_more_stances_agn"],
            "groups_for" : ["group_stances_for"],
            "groups_agn" : ["group_stances_agn"],
            "for_norms" : ["norms!"],
            "agn_norms" : ["norms"],
            "for_bill_norms" : ["norms.."],
            "agn_bill_norms" : ["norms?"],
            "split_group" : ["Split here"],
            "split_record" : ["Split here as well"],
            "split_credo" : ["Split here too"],
            "MI_stance" : "something",
            "MI_group" : "something else",
            "MI_credo" : "something more",
            "MI_record" : "something even more",
            "MI_norm" :  "something eve even more",
            "result" : "FOR",
            "strategy" : "Good Strategy",
            "reason" : "Some stances",
            "downside" : "Some more stances",
            "downside_record" : ["Even more stances"]
            }

    def test_init_default(self):
        """Tests that default values are set for instance variables"""
        decision = Decision()

        # Attributes used in making the decision)
        self.assertEqual(decision.bill, None)
        self.assertEqual(decision.member, None)
        self.assertEqual(decision.for_stances, [])
        self.assertEqual(decision.agn_stances, [])
        self.assertEqual(decision.con_rel_for_stances, [])
        self.assertEqual(decision.con_rel_agn_stances, [])
        self.assertEqual(decision.groups_for, [])
        self.assertEqual(decision.groups_agn, [])
        self.assertEqual(decision.for_norms, [])
        self.assertEqual(decision.agn_norms, [])
        self.assertEqual(decision.for_bill_norms, [])
        self.assertEqual(decision.agn_bill_norms, [])
        self.assertEqual(decision.split_group, [])
        self.assertEqual(decision.split_record, [])
        self.assertEqual(decision.split_credo, [])
        self.assertEqual(decision.MI_stance, None)
        self.assertEqual(decision.MI_group, None)
        self.assertEqual(decision.MI_credo, None)
        self.assertEqual(decision.MI_record, None)
        self.assertEqual(decision.MI_norm, None)

        # Attributes about the actual decision)
        self.assertEqual(decision.result, None)
        self.assertEqual(decision.strategy, None)
        self.assertEqual(decision.reason, None)
        self.assertEqual(decision.downside, None)
        self.assertEqual(decision.downside_record, [])

    def test_init_hash(self):
        """ Verifies that input data from a hash is properly set."""
        decision = Decision(self.input_hash)
        for key, value in self.input_hash.iteritems():
            self.assertEqual(value, decision.__dict__[key])
        for key, value in decision.__dict__.iteritems():
            self.assertEqual(value, self.input_hash[key])

    def test_init_hash_default(self):
        """ Verifies defaults are still defined when a hash is provided."""
        self.input_hash.pop("member")
        decision = Decision(self.input_hash)
        for key, value in self.input_hash.iteritems():
            self.assertEqual(value, decision.__dict__[key])
        self.assertEqual(decision.member, None)
