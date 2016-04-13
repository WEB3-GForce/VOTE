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

from src.classes.bill import Bill
from src.classes.decision import Decision
from src.classes.member import Member
from src.classes.strategies import strategy_hash
from src.constants import database as db_constants
from src.database import queries
from src.database.pymongodb import PymongoDB
from src.scripts.database import load_data
from src.vote import vote

from test.test_helpers.always_fail_strategy import AlwaysFailStrategy
from test.test_helpers.always_succeed_strategy import AlwaysSucceedStrategy

class VoteTest(unittest.TestCase):
    """ Test suite for vote.py."""

    @classmethod
    def drop_collections(cls, DB):
        """Removes all the collections from a DB"""
        for collection_name in db_constants.DB_COLLECTIONS:
            DB.DB.drop_collection(collection_name)


    @classmethod
    def setUpClass(cls):
        # Make sure that the database is clean before this class is run.
        DB = PymongoDB()
        VoteTest.drop_collections(DB)

        # Ignore all output to the screen.
        sys.stdout = StringIO()

        VoteTest.backup_hash = strategy_hash.STRATEGY_HASH

    @classmethod
    def tearDownClass(cls):
        sys.stdout = sys.__stdout__
        strategy_hash.STRATEGY_HASH = VoteTest.backup_hash

    def setUp(self):
        self.DB = PymongoDB.get_db()
        load_data.load_data()
        self.member = self.DB.find_one(db_constants.MEMBERS,
            {"full_name" : "vote_test"})

        self.MEMBER = "vote_test"
        self.BILL1 = "VOTE_BILL1"
        self.BILL2 = "VOTE_BILL2"
        self.BILL3 = "VOTE_BILL3"

        self.GROUP1 = "VOTE_GROUP1"
        self.GROUP2 = "VOTE_GROUP2"

        self.strategy1_name = "AlwaysSucceed"
        self.strategy2_name = "AlwaysFail"
        self.strategy3_name = "AlwaysFail2"
        self.strategy4_name = "Inactive"

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

        AlwaysFailStrategy.call_count = 0
        self.DB.DB.drop_collection(db_constants.DECISIONS)


    def tearDown(self):
        # Delete the database each time to start fresh.
        VoteTest.drop_collections(self.DB)

    def test_initialize_decision_one(self):
        """ Verifies initialization works properly."""

        # For all such tests, I assume that the functions know what they are
        # doing. I just check to make sure they have been assigned
        decision = Decision()
        vote._initialize_decision(decision, self.member, self.bill1)

        self.assertEqual(decision.member, self.member._id)
        self.assertEqual(decision.bill, self.bill1._id)
        self.assertTrue(len(self.member.stances) > 0)
        self.assertTrue(len(self.member.pro_rel_stances) > 0)
        self.assertTrue(len(decision.for_stances) > 0)
        self.assertTrue(len(decision.agn_stances) == 0)

    def test_initialize_decision_two(self):
        """ Verifies initialization works properly."""
        decision = Decision()
        vote._initialize_decision(decision, self.member, self.bill2)

        self.assertEqual(decision.member, self.member._id)
        self.assertEqual(decision.bill, self.bill2._id)
        self.assertTrue(len(self.member.stances) > 0)
        self.assertTrue(len(self.member.pro_rel_stances) > 0)
        self.assertTrue(len(decision.for_stances) > 0)
        self.assertTrue(len(decision.agn_stances) > 0)

    def test_initialize_decision_three(self):
        """ Verifies initialization works properly."""
        decision = Decision()
        vote._initialize_decision(decision, self.member, self.bill3)

        self.assertEqual(decision.member, self.member._id)
        self.assertEqual(decision.bill, self.bill3._id)
        self.assertTrue(len(self.member.stances) > 0)
        self.assertTrue(len(self.member.pro_rel_stances) > 0)
        self.assertTrue(len(decision.for_stances) == 0)
        self.assertTrue(len(decision.agn_stances) > 0)

    def test__save(self):
        """ Verifies a decision is properly saved to the DB."""
        decision = Decision()
        decision.strategy = "This is a test"
        decision.bill = "Some Bill"
        decision.member = "Some Member"

        vote._save(decision)
        result = self.DB.find_one(db_constants.DECISIONS,
            {"strategy" : decision.strategy})

        # Remove the id that the database adds as this is not in the original
        # one
        result.__dict__.pop("_id")

        self.assertEquals(decision.__dict__, result.__dict__)


    def test__retrieve_strategy_list(self):
        """ Verifies all active StrategyEntries are returned sorted by rank"""

        result = vote._retrieve_strategy_list()
        answer = [self.strategy3_name, self.strategy1_name, self.strategy2_name]
        self.assertEqual(len(result), len(answer))
        for i in range(0, len(result)):
            self.assertEqual(result[i].name, answer[i])


    def test__apply_decision_strategies_no_strategies_in_hash(self):
        """ Verifies correctness if StrategyEntry's specify invalid strategies."""
        strategy_hash.STRATEGY_HASH = {}
        decision = Decision()

        result = vote._apply_decision_strategies(self.member, self.bill1, decision)
        self.assertFalse(result)
        self.assertEquals(decision.strategy, None)

    def test__apply_decision_strategies_all_strategies_fail(self):
        """ Verifies that false is returned if strategies fail."""
        strategy_hash.STRATEGY_HASH = {"AlwaysFail": AlwaysFailStrategy,
                                       "AlwaysFail2" : AlwaysFailStrategy}
        decision = Decision()

        result = vote._apply_decision_strategies(self.member, self.bill1, decision)
        self.assertFalse(result)
        self.assertEquals(decision.strategy, None)
        self.assertEquals(AlwaysFailStrategy.call_count, 2)

    def test__apply_decision_strategies_one_succeeds(self):
        """ Verifies that false is returned if strategies fail."""
        strategy_hash.STRATEGY_HASH = {"AlwaysFail": AlwaysFailStrategy,
                                       "AlwaysFail2" : AlwaysFailStrategy,
                                       "AlwaysSucceed" : AlwaysSucceedStrategy}
        decision = Decision()

        result = vote._apply_decision_strategies(self.member, self.bill1, decision)
        self.assertTrue(result)
        self.assertEquals(decision.strategy, "AlwaysSucceedStrategy")

        # Verify that the reasons and downsides get grouped.
        for i in range(0, len(decision.reason) - 1):
            keyi = [decision.downside[i].issue, decision.downside[i].side]
            keyi_plus_one = [decision.reason[i + 1].issue, decision.reason[i + 1].side]
            self.assertTrue(keyi <= keyi_plus_one)

        for i in range(0, len(decision.downside) - 1):
            keyi = [decision.downside[i].issue, decision.downside[i].side]
            keyi_plus_one = [decision.downside[i + 1].issue, decision.downside[i + 1].side]
            self.assertTrue(keyi <= keyi_plus_one)

    def test__vote_helper_fails(self):
        """ Verifies that false is returned if strategies fail."""
        strategy_hash.STRATEGY_HASH = {"AlwaysFail": AlwaysFailStrategy,
                                       "AlwaysFail2" : AlwaysFailStrategy}
        result = vote._vote_helper(self.member, self.bill1)

        self.assertEquals(result.strategy, None)

        for _ in self.DB.find(db_constants.DECISIONS):
            raise Exception("Decision Object should not be saved if no decision made")

    def test__vote_helper_success(self):
        """ Verifies the function updates decision properly on success."""
        strategy_hash.STRATEGY_HASH = {"AlwaysFail": AlwaysFailStrategy,
                                       "AlwaysSucceed" : AlwaysSucceedStrategy}
        decision = vote._vote_helper(self.member, self.bill2)

        # Make sure decision was initialized.
        self.assertEqual(decision.member, self.member._id)
        self.assertEqual(decision.bill, self.bill2._id)
        self.assertTrue(len(decision.for_stances) > 0)
        self.assertTrue(len(decision.agn_stances) > 0)

        # Make sure decision metrics were updated. Just test a few
        self.assertNotEquals(decision.MI_stance, None)
        self.assertTrue(len(decision.groups_for) > 0)

        # Verify that the decision was made.
        self.assertEquals(decision.strategy, "AlwaysSucceedStrategy")
        self.assertTrue(len(decision.reason) >= 0)
        self.assertTrue(len(decision.downside) >= 0)

        # Make sure the decision was stored in the DB
        decision_in_db = self.DB.find_one(db_constants.DECISIONS, {"member": decision.member})

        self.assertEquals(decision.strategy, decision_in_db.strategy)

        for stance1, stance2 in zip(decision.reason, decision_in_db.reason):
            self.assertTrue(stance1.__dict__, stance2.__dict__)

        for stance1, stance2 in zip(decision.downside, decision_in_db.downside):
            self.assertEquals(stance1.__dict__, stance2.__dict__)

    def test__get_bills_no_identifier(self):
        """ Verifies a cursor for Bills is returned as the default."""
        cursor = vote._get_bills()
        self.assertEqual(type(cursor.next()), Bill)

    def test__get_bills_bad_identifier(self):
        """ Verifies a cursor for Bills is returned for a bad identifier."""
        cursor = vote._get_bills("Bad Identifier")
        self.assertEqual(type(cursor.next()), Bill)

    def test__get_bills_good_identifier(self):
        """ Verifies an array for the bill is returned on success."""
        result = vote._get_bills("VOTE_BILL2")
        self.assertEqual(result[0].name, "VOTE_BILL2")

    def test__get_members_no_identifier(self):
        """ Verifies a cursor for Member is returned as the default."""
        cursor = vote._get_members()
        self.assertEqual(type(cursor.next()), Member)

    def test__get_members_bad_identifier(self):
        """ Verifies a cursor for Member is returned for a bad identifier."""
        cursor = vote._get_members("Bad Identifier")
        self.assertEqual(type(cursor.next()), Member)

    def test__get_members_good_identifier(self):
        """ Verifies an array for the member is returned on success."""
        result = vote._get_members("vote_test")
        self.assertEqual(result[0].full_name, "vote_test")

    def test_vote_bad_member(self):
        """ Verifies that None is returned for an invalid member identifier."""
        result = vote.vote("BAD_MEMBER", self.BILL1)
        self.assertEquals(result, None)

    def test_vote_bad_bill(self):
        """ Verifies that None is returned for an invalid bill identifier."""
        result = vote.vote(self.MEMBER, "Bad Bill")
        self.assertEquals(result, None)

    def test_vote_fail(self):
        """ Verifies proper decision returned when no decision is reached."""
        strategy_hash.STRATEGY_HASH = {"AlwaysFail": AlwaysFailStrategy}
        result = vote.vote(self.MEMBER, self.BILL1)
        self.assertEquals(result.strategy, None)

    def test_vote_success(self):
        """ Verifies decision is returned upon success."""
        strategy_hash.STRATEGY_HASH = {"AlwaysFail": AlwaysFailStrategy,
                                       "AlwaysFail2" : AlwaysFailStrategy,
                                       "AlwaysSucceed": AlwaysSucceedStrategy}
        result = vote.vote(self.MEMBER, self.BILL1)

        # Make sure that the decision is properly reached.
        self.assertEquals(result.strategy, "AlwaysSucceedStrategy")
        self.assertTrue(len(result.reason) > 0)
        self.assertTrue(len(result.downside) > 0)

    def test_vote_all(self):
        """ Verifies vote_all for all members on all bills."""
        strategy_hash.STRATEGY_HASH = {"AlwaysFail": AlwaysFailStrategy,
                                       "AlwaysFail2" : AlwaysFailStrategy,
                                       "AlwaysSucceed": AlwaysSucceedStrategy}
        vote.vote_all()

        member_count = self.DB.DB[db_constants.MEMBERS].count()
        bill_count = self.DB.DB[db_constants.BILLS].count()
        decision_count = self.DB.DB[db_constants.DECISIONS].count()

        # Make sure there is a decision for every member on every vote.
        self.assertEquals(member_count * bill_count, decision_count)

        for member in self.DB.find(db_constants.MEMBERS):
            vote_cursor = self.DB.find(db_constants.DECISIONS,
                {"member":member._id})
            self.assertEquals(bill_count, vote_cursor.cursor.count())

        for bill in self.DB.find(db_constants.BILLS):
            vote_cursor = self.DB.find(db_constants.DECISIONS, {"bill":bill._id})
            self.assertEquals(member_count, vote_cursor.cursor.count())

    def test_vote_all_member_specified(self):
        """ Verifies vote_all when voting for one member on all bills."""
        strategy_hash.STRATEGY_HASH = {"AlwaysFail": AlwaysFailStrategy,
                                       "AlwaysFail2" : AlwaysFailStrategy,
                                       "AlwaysSucceed": AlwaysSucceedStrategy}
        vote.vote_all(member_identifier=self.MEMBER)

        bill_count = self.DB.DB[db_constants.BILLS].count()
        decision_count = self.DB.DB[db_constants.DECISIONS].count()

        self.assertEquals(bill_count, decision_count)

        member = self.DB.find_one(db_constants.MEMBERS, {"full_name" : self.MEMBER})
        vote_cursor = self.DB.find(db_constants.DECISIONS, {"member":member._id})
        self.assertEquals(bill_count, vote_cursor.cursor.count())

        for bill in self.DB.find(db_constants.BILLS):
            vote_cursor = self.DB.find(db_constants.DECISIONS,
                {"bill":bill._id})
            self.assertEquals(1, vote_cursor.cursor.count())

    def test_vote_all_bill_specified(self):
        """ Verifies vote_all for all members on a given bill."""
        strategy_hash.STRATEGY_HASH = {"AlwaysFail": AlwaysFailStrategy,
                                       "AlwaysFail2" : AlwaysFailStrategy,
                                       "AlwaysSucceed": AlwaysSucceedStrategy}
        vote.vote_all(bill_identifier=self.BILL2)

        member_count = self.DB.DB[db_constants.MEMBERS].count()
        decision_count = self.DB.DB[db_constants.DECISIONS].count()

        # Make sure there is a decision for every member on every vote.
        self.assertEquals(member_count, decision_count)

        for member in self.DB.find(db_constants.MEMBERS):
            vote_cursor = self.DB.find(db_constants.DECISIONS,
                {"member":member._id})
            self.assertEquals(1, vote_cursor.cursor.count())

        bill = self.DB.find_one(db_constants.BILLS, {"name": self.BILL2})
        vote_cursor = self.DB.find(db_constants.DECISIONS, {"bill":bill._id})
        self.assertEquals(member_count, vote_cursor.cursor.count())

    def test_vote_all_member_and_bill_specified(self):
        """ Verifies vote_all for a particular member on a particular bill"""
        strategy_hash.STRATEGY_HASH = {"AlwaysFail": AlwaysFailStrategy,
                                       "AlwaysFail2" : AlwaysFailStrategy,
                                       "AlwaysSucceed": AlwaysSucceedStrategy}
        vote.vote_all(member_identifier=self.MEMBER, bill_identifier=self.BILL2)

        decision_count = self.DB.DB[db_constants.DECISIONS].count()
        self.assertEquals(1, decision_count)

        member = self.DB.find_one(db_constants.MEMBERS, {"full_name" : self.MEMBER})
        bill = self.DB.find_one(db_constants.BILLS, {"name": self.BILL2})
        decision = self.DB.find_one(db_constants.DECISIONS, {"member":member._id})

        self.assertEquals(decision.member, member._id)
        self.assertEquals(decision.bill, bill._id)
