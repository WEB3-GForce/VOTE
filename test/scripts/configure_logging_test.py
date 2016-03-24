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
import os
import sys
import unittest

from contextlib import contextmanager
from  StringIO import StringIO

from src.config import config
from src.constants import config as config_constants
from src.constants import logger
from src.scripts import configure_logging

class ConfigureLoggingTest(unittest.TestCase):
    """ Test suite for configure_logging.py."""

    ORIGINAL_CONFIG = copy.deepcopy(config.CONFIG)
    CONFIG_PATH = os.path.dirname(__file__) + "/../../src/config/"

    LOG_FILE = "%s/../../log/%s/vote.log" % (os.path.dirname(__file__),
        config.CONFIG[config_constants.DATABASE])

    @contextmanager
    def capture(self, command, *args, **kwargs):
        """Captures stderr. Based on:
            http://schinckel.net/2013/04/15/capture-and-test-sys.stdout-sys.stderr-in-unittest.testcase/
        """
        command(*args, **kwargs)
        sys.stderr.seek(0)
        yield sys.stderr.read()

    @classmethod
    def setUpClass(cls):
        # Make sure that the log is clear
        open(ConfigureLoggingTest.LOG_FILE, "w").close()

    def setUp(self):
        # Make sure stderr is mocked out.
        self.stderr = StringIO()
        self.original_stderr = sys.stderr
        sys.stderr = self.stderr

    def tearDown(self):
        # Restore the original config so as not to mess up other tests
        config.CONFIG = copy.deepcopy(ConfigureLoggingTest.ORIGINAL_CONFIG)

        # Restore stderr.
        sys.stderr = self.original_stderr

        # Clear the log after each test.
        open(ConfigureLoggingTest.LOG_FILE, "w").close()

    def test_log_file_and_stderr(self):
        """Verifies file and stderr logging both work."""
        config.CONFIG[config_constants.DEBUG] = True
        config.CONFIG[config_constants.LOG] = True
        configure_logging.configure_logging()

        test_message1 = "Here is the first test"
        with self.capture(logger.LOGGER.info, test_message1) as output:
            self.assertTrue(test_message1 in output)
            self.assertTrue("INFO" in output)

        with open(ConfigureLoggingTest.LOG_FILE, "r") as log_file:
            output = log_file.read()
            self.assertTrue(test_message1 in output)
            self.assertTrue("INFO" in output)

    def test_stderr_only(self):
        """Verifies logging only to stderr works."""
        config.CONFIG[config_constants.DEBUG] = True
        config.CONFIG[config_constants.LOG] = False
        configure_logging.configure_logging()

        test_message1 = "Here is the first test"
        with self.capture(logger.LOGGER.info, test_message1) as output:
            self.assertTrue(test_message1 in output)
            self.assertTrue("INFO" in output)

        with open(ConfigureLoggingTest.LOG_FILE, "r") as log_file:
            output = log_file.read()
            self.assertTrue(test_message1 not in output)
            self.assertTrue("INFO" not in output)

    def test_no_logging_except_errors(self):
        """Verifies that only errors are logging when no logging specified"""
        config.CONFIG[config_constants.DEBUG] = False
        config.CONFIG[config_constants.LOG] = False
        configure_logging.configure_logging()

        test_message1 = "Here is the first test"
        with self.capture(logger.LOGGER.info, test_message1) as output:
            self.assertTrue(test_message1 not in output)
            self.assertTrue("INFO" not in output)

        with self.capture(logger.LOGGER.error, test_message1) as output:
            self.assertTrue(test_message1 in output)
            self.assertTrue("ERROR" in output)

        with open(ConfigureLoggingTest.LOG_FILE, "r") as log_file:
            output = log_file.read()
            self.assertTrue(test_message1 not in output)
            self.assertTrue("INFO" not in output)
            self.assertTrue("ERROR" not in output)