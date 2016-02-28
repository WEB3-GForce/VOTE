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
import exceptions
import pymongo
from src.config import config
from src.constants import config as config_constants
from src.constants import database as db_constants


class PymongoDB(object):

    _DB = None

    @classmethod
    def db(cls):
        if PymongoDB._DB:
            return PymongoDB._DB
        PymongoDB._DB = _PymongoDB(config.CONFIG[config_constants.DATABASE])
        return PymongoDB._DB

class _PymongoDB(object):

    def __init__(self, db_type):
        if db_type not in db_constants.DB_TYPES:
            raise exceptions.ValueError("Invalid database type: " + db_type)

        self._CLIENT = pymongo.MongoClient(
            config.CONFIG[config_constants.DB_CLIENT])
        self.DB = self._CLIENT[db_type]
        self.MEMBERS = self.DB[db_constants.MEMBERS_NAME]
        self.GROUPS = self.DB[db_constants.GROUPS_NAME]
        self.BILLS = self.DB[db_constants.BILLS_NAME]
        self.ISSUES = self.DB[db_constants.ISSUES_NAME]

        # TODO(WEB3-GForce) Get translation working
        # self.DB.add_son_manipulator(Transform())
