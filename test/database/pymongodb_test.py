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

import copy
import unittest

from src.classes.member import Member
from src.config import config
from src.constants import config as config_constants
from src.constants import database as db_constants
from src.database.pymongodb import PymongoDB

class PymongoDBTest(unittest.TestCase):
    """ Test suite for pymongodb.py."""

    ORIGINAL_CONFIG = copy.deepcopy(config.CONFIG)

    @classmethod
    def setUpClass(cls):
        # Make sure that the database is clean before this class is run.
        DB = PymongoDB()
        DB._CLIENT.drop_database(DB.DB)

    def setUp(self):
        self.DB = PymongoDB.get_db()

    def tearDown(self):
        # Restore the original config so as not to mess up other tests
        config.CONFIG = copy.deepcopy(PymongoDBTest.ORIGINAL_CONFIG)
        # Delete the database each time to start fresh.
        self.DB._CLIENT.drop_database(self.DB.DB)


    def test_get_db(self):
        """ Verifies that get_db returns the proper DB to be used."""
        PymongoDB._DB = None
        db = PymongoDB.get_db()
        self.assertEqual(db.DB.name, config.CONFIG[config_constants.DATABASE])

        # Subsequent calls to get_db should return the same object)
        self.assertEquals(db, PymongoDB.get_db())

    def test_create_db(self):
        """ Verifies that each valid type of db is created properly."""
        for db_type in db_constants.DB_TYPES:
            config.CONFIG[config_constants.DATABASE] = db_type
            db = PymongoDB()
            self.assertEqual(db.DB.name, db_type)

    def test_create_db_invalid_type(self):
        """ Verifies an exception is thrown for invalid types."""
        config.CONFIG[config_constants.DATABASE] = "InvalidOption"
        self.assertRaises(ValueError, PymongoDB)

    def test_get_collection(self):
        """ Verifies that each valid collection can be retrieved."""
        for collection_name in db_constants.DB_COLLECTIONS:
            collection = self.DB.get_collection(collection_name)
            self.assertEqual(collection.name, collection_name)

    def test_get_collection_invalid_type(self):
        """ Verifies an exception is thrown for invalid collection names."""
        self.assertRaises(ValueError, self.DB.get_collection,
            "InvalidCollection")

    def test_insert_and_find_one(self):
        """ Verifies a custom class can be properly inserted and found."""
        member = Member()
        insert_result = self.DB.insert_one(db_constants.MEMBERS, member)
        result = self.DB.find_one(db_constants.MEMBERS,
            {db_constants.ENTRY_ID: insert_result.inserted_id})

        self.assertTrue(db_constants.ENTRY_ID in result.__dict__)
        result.__dict__.pop(db_constants.ENTRY_ID)
        self.assertEqual(member.__dict__, result.__dict__)

    def test_insert_and_find(self):
        """ Verifies multiple custom classes can be found."""
        member = Member()
        member2 = Member()
        member3 = Member()

        id1 = self.DB.insert_one(db_constants.MEMBERS, member)
        id2 = self.DB.insert_one(db_constants.MEMBERS, member2)
        id3 = self.DB.insert_one(db_constants.MEMBERS, member3)

        ids = [id1.inserted_id, id2.inserted_id, id3.inserted_id]

        for found_member in self.DB.find("members"):
            self.assertEqual(type(found_member), Member)
            self.assertTrue(found_member._id in ids)

    def test_find_none(self):
        """ Verifies find works properly on an empty database."""
        for _ in self.DB.find("members"):
            self.fail("No objects should be in the database")


    def convertUnicodeToAscii(self, result):
        """Converts any unicode to ascii for equality testing."""
        for key, value in result.__dict__.iteritems():
            if type(value) is unicode:
                result.__dict__[key] = value.encode("ascii", "ignore")

    def test_insert_and_replace_one(self):
        """ Verifies a custom class can be properly replaced."""
        member = Member()
        member2 = Member()
        member2.last_name = "Test"
        member2.first_name = "Test"

        insert_result = self.DB.insert_one(db_constants.MEMBERS, member)
        self.DB.replace_one(db_constants.MEMBERS,
            {db_constants.ENTRY_ID: insert_result.inserted_id}, member2)
        result = self.DB.find_one(db_constants.MEMBERS,
            {db_constants.ENTRY_ID: insert_result.inserted_id})

        self.convertUnicodeToAscii(result)
        self.assertTrue(db_constants.ENTRY_ID in result.__dict__)
        result.__dict__.pop(db_constants.ENTRY_ID)
        self.assertNotEqual(member.__dict__, result.__dict__)
        self.assertEqual(member2.__dict__, result.__dict__)

    def test_insert_and_delete_one(self):
        """ Verifies a custom class can be properly deleted."""
        member = Member()

        insert_result = self.DB.insert_one(db_constants.MEMBERS, member)
        self.DB.delete_one(db_constants.MEMBERS,
            {db_constants.ENTRY_ID: insert_result.inserted_id})
        result = self.DB.find_one(db_constants.MEMBERS,
            {db_constants.ENTRY_ID: insert_result.inserted_id})
        self.assertIsNone(result)
