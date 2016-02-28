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
import json

from src.constants import config as config_constants

# This variable contains the config hash from the loaded config file
CONFIG = {}

def load_config(file_name):
    """ Loads the config hash from the specified config file into the CONFIG
    variable.
    
    Arguments:
        file_name: the name of the config hash such as "prod.json"
    
    Raises:
        IOError: If file_name doesn't exist.
        ValueError: If file_name isn't a json object.
    """
    global CONFIG
    with open(file_name, "r") as config_file:
        CONFIG = json.load(config_file)
    return CONFIG

# _config_dir = os.path.dirname(os.path.abspath(__file__))
# load_config(_config_dir + "/" + config_constants.DEFAULT_CONFIG_FILE)
