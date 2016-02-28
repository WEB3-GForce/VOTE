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
import os
import unittest

from src.config import config

class ConfigTest(unittest.TestCase):
    """ Test suite for config.py."""

    ORIGINAL_CONFIG = config.CONFIG
    CONFIG_PATH = os.path.dirname(__file__) + "/../../src/config/"

    def tearDown(self):
        # Restore the original config so as not to mess up other tests
        config.CONFIG = ConfigTest.ORIGINAL_CONFIG

    def test_load_test(self):
        """ Verifies that the test.json config file is properly loaded."""
        config.load_config(ConfigTest.CONFIG_PATH + "test.json")
        with open(ConfigTest.CONFIG_PATH + "test.json", "r") as config_file:
            self.assertEqual(config.CONFIG, json.load(config_file))

    def test_load_staging(self):
        """ Verifies that the staging.json config file is properly loaded."""
        config.load_config(ConfigTest.CONFIG_PATH + "staging.json")
        with open(ConfigTest.CONFIG_PATH + "staging.json", "r") as config_file:
            self.assertEqual(config.CONFIG, json.load(config_file))

    def test_load_dev(self):
        """ Verifies that the dev.json config file is properly loaded."""
        config.load_config(ConfigTest.CONFIG_PATH + "dev.json")
        with open(ConfigTest.CONFIG_PATH + "dev.json", "r") as config_file:
            self.assertEqual(config.CONFIG, json.load(config_file))

    def test_load_prod(self):
        """ Verifies that the prod.json config file is properly loaded."""
        config.load_config(ConfigTest.CONFIG_PATH + "prod.json")
        with open(ConfigTest.CONFIG_PATH + "prod.json", "r") as config_file:
            self.assertEqual(config.CONFIG, json.load(config_file))