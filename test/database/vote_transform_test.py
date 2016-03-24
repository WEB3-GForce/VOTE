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

import json
import unittest

from src.constants import database as db_constants
from src.database.vote_transform import VoteTransform

class VoteTransformTest(unittest.TestCase):
    """ Test suite for vote_transform.py."""

    def setUp(self):
        self.transform = VoteTransform()

    def test_custom_class_transform(self):
        """ Verifies that custom classes can be properly encoded and decoded."""
        for each_class in db_constants.DB_CUSTOM_CLASSES:
            class_object = each_class()
            encoding = self.transform.transform_incoming(class_object)
            output = self.transform.transform_outgoing(encoding)
            self.assertTrue(type(output) is type(class_object))
            self.assertEqual(output.__dict__, class_object.__dict__)

    def test_custom_class_in_json_transform(self):
        """ Verifies custom classes within json are encoded and decoded."""
        for each_class in db_constants.DB_CUSTOM_CLASSES:
            class_object = each_class()
            json = {"test": class_object}

            encoding = self.transform.transform_incoming(json)
            output = self.transform.transform_outgoing(encoding)

            self.assertTrue(type(output) is dict)
            self.assertEqual(output["test"].__dict__, class_object.__dict__)

    def test_custom_class_in_custom_class_transform(self):
        """ Verifies a custom classes within another is handled properly."""
        for each_class in db_constants.DB_CUSTOM_CLASSES:
            class_object = each_class()
            class_object2 = each_class()
            class_object.test = class_object2

            encoding = self.transform.transform_incoming(class_object)
            output = self.transform.transform_outgoing(encoding)

            self.assertTrue(type(output) is type(class_object))
            self.assertEqual(output.test.__dict__, class_object2.__dict__)


    def test_list_transform(self):
        """ Verifies custom classes within lists are encoded and decoded."""
        for each_class in db_constants.DB_CUSTOM_CLASSES:
            class_object_list = [each_class(), each_class()]
            class_object_list[1].extra = "something different"
            json = {"test": class_object_list}

            encoding = self.transform.transform_incoming(json)
            output = self.transform.transform_outgoing(encoding)

            self.assertTrue(type(output) is dict)
            self.assertEqual(len(class_object_list), len(output["test"]))

            for input_class, output_class in zip(class_object_list, output["test"]):
                self.assertEqual(input_class.__dict__, output_class.__dict__)

    def test_dict_transform(self):
        """ Verifies custom classes in dictionaries are encoded and decoded."""
        for each_class in db_constants.DB_CUSTOM_CLASSES:
            class_object = each_class()
            json = {"test": {"test2" : class_object }}

            encoding = self.transform.transform_incoming(json)
            output = self.transform.transform_outgoing(encoding)

            output_class = output["test"]["test2"]
            self.assertTrue(type(output) is dict)
            self.assertEqual(output_class.__dict__, class_object.__dict__)
