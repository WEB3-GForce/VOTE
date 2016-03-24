import os
from src.config import config
from src.scripts import configure_logging

config.load_config(os.path.dirname(__file__) + "/../src/config/test.json")
configure_logging.configure_logging()