import os
import logging
from logging import handlers

from src.config import config
from src.constants import config as config_constants

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
    format_string = "[%(levelname)s %(asctime)s @ %(pathname)s:%(funcName)s:%(lineno)d] %(message)s"
    formatter = logging.Formatter(format_string)

    # Remove all previous handlers
    rootLogger = logging.getLogger()
    rootLogger.handlers = []
    rootLogger.setLevel(logging.NOTSET)

    if config_log:
        file_handler = handlers.RotatingFileHandler(LOG_FILE,
            maxBytes=config_log_size, backupCount=config_backup_size)
        file_handler.setLevel(logging.NOTSET)
        file_handler.setFormatter(formatter)
        rootLogger.addHandler(file_handler)

    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    if config_debug:
        console.setLevel(logging.NOTSET)
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)
