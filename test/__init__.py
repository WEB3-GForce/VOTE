import os
from src.config import config

config.load_config(os.path.dirname(__file__) + "/../src/config/test.json")