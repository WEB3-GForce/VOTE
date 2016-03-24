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

import os
import logging
from logging import handlers

from src.config import config
from src.constants import config as config_constants
from src.constants import logger


def configure_logging():
    """Configure logging based on the configuration settings. The logger can
    potentially log to both the screen and console at the same time.
    
    This script should be run before attempting to use the logger.
    
    Based on:
    https://docs.python.org/2/howto/logging-cookbook.html#logging-to-multiple-destinations
    """
    config_db = config.CONFIG[config_constants.DATABASE]
    config_debug = config.CONFIG[config_constants.DEBUG]
    config_log = config.CONFIG[config_constants.LOG]
    config_log_size = config.CONFIG[config_constants.LOG_SIZE]
    config_backup_size = config.CONFIG[config_constants.LOG_BACKUP_SIZE]

    LOG_FILE = "%s/../../log/%s/vote.log" % (os.path.dirname(__file__),
        config_db)
    formatter = logging.Formatter(logger.FORMAT_STRING)

    # Remove all previous handlers
    logger.LOGGER.handlers = []
    logger.LOGGER.setLevel(logging.NOTSET)

    if config_log:
        file_handler = handlers.RotatingFileHandler(LOG_FILE,
            maxBytes=config_log_size, backupCount=config_backup_size)
        file_handler.setLevel(logging.NOTSET)
        file_handler.setFormatter(formatter)
        logger.LOGGER.addHandler(file_handler)

    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    if config_debug:
        console.setLevel(logging.NOTSET)
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)
