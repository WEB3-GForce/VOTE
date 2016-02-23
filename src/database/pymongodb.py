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
from src.constants import database as constants_database

class PymongoDB(object):

    _DB = None

    @classmethod
    def db(cls):
        if PymongoDB._DB:
            return PymongoDB._DB
        PymongoDB._DB = _PymongoDB("test")
        return PymongoDB._DB

class _PymongoDB(object):

    # This is the default Mongo client
    _CLIENT = pymongo.MongoClient()

    def __init__(self, db_type):
        if db_type not in constants_database.DB_TYPES:
            raise exceptions.ValueError("Invalid database type: " + db_type)

        self.DB = _PymongoDB._CLIENT[db_type]
        self.MEMBERS = self.DB[constants_database.MEMBERS_NAME]
        self.GROUPS = self.DB[constants_database.GROUPS_NAME]
        self.BILLS = self.DB[constants_database.BILLS_NAME]
        self.ISSUES = self.DB[constants_database.ISSUES_NAME]

        # self.DB.add_son_manipulator(Transform())
