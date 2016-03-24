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
from src.database import vote_transform
from src.database import vote_cursor

class PymongoDB(object):
    """ This class represents the database used to store objects in VOTE. It
    defines wrapper methods that automatically convert src/classes objects into
    json and vice versa. Hence, other code can work solely with the objects
    defined in src/classes.
    
    To retrieve a database object, use the class method getDB(). DO NOT
    directly instantiate an object for this class.
    """

    # An object representing the database to be used throughout the project.
    _DB = None

    @classmethod
    def get_db(cls):
        """ A class method to retrieve the database object."""
        if PymongoDB._DB:
            return PymongoDB._DB
        PymongoDB._DB = PymongoDB()
        return PymongoDB._DB

    def __init__(self):
        """ Initializes a new PymongoDB instance based upon the configuration
        settings.
        
        Attributes:
            DB: This represents the direct Pymongo database. Generally, code
            should use this class wrapper. However, since its functionality is
            limited, code will occasionally need to access the DB directly.
        
        Raises:
            ValueError: An invalid database type is specified in the
                configurations.
        """
        db_type = config.CONFIG[config_constants.DATABASE]
        if db_type not in db_constants.DB_TYPES:
            msg = "Invalid database type.\n Valid Options: %s\n Given: %s\n" % (
                db_constants.DB_TYPES, db_type)
            raise exceptions.ValueError(msg)

        self._CLIENT = pymongo.MongoClient(
            config.CONFIG[config_constants.DB_CLIENT])
        self.DB = self._CLIENT[db_type]
        self._transformer = vote_transform.VoteTransform()

    def get_collection(self, name):
        """ Returns a pymongo Collection corresponding to the given name
        
        Arguments:
            name: the name of the collection
        
        Raises:
            ValueError: If the collection is not defined
        """
        if name not in db_constants.DB_COLLECTIONS:
            msg = "Invalid connection.\n Valid Options: %s\n Given: %s\n" % (
                db_constants.DB_COLLECTIONS, str(name))
            raise exceptions.ValueError(msg)
        return self.DB[name]

    def insert_one(self, collection, query):
        """ A wrapper for the Pymongo Collection insert_one function that
        properly translates src/classes objects.
        
        Arguments:
            collection: the name of the collection to insert into.
            query: the data to insert
        
        Return:
            The result of Pymongo Collection insert_one
        """
        collection = self.get_collection(collection)
        return collection.insert_one(
            self._transformer.transform_incoming(query))

    def find(self, collection, query=None):
        """ A wrapper for the Pymongo Collection find function that properly
        translates src/classes objects.
        
        This function is typically used as an iterator in a loop. The VoteCursor
        translates the query results into src/classes objects.
        
        Arguments:
            collection: the name of the collection to search
            query: optional query parameters
        
        Return:
            A VoteCursor that encapsulates the result of Pymongo Collection find
        """
        collection = self.get_collection(collection)
        result = collection.find(query)
        return vote_cursor.VoteCursor(result)

    def find_one(self, collection, query):
        """ A wrapper for the Pymongo Collection find_one function that properly
        translates src/classes objects.
        
        Arguments:
            collection: the name of the collection to search
            query: a Pymongo query for the desired object
        
        Return:
            The result of Pymongo Collection find_one
        """
        collection = self.get_collection(collection)
        result = collection.find_one(query)
        if result is None:
            return None
        return self._transformer.transform_outgoing(result)

    def replace_one(self, collection, query, replacement):
        """ A wrapper for the Pymongo Collection replace_one function that
        properly translates src/classes objects.
        
        Arguments:
            collection: the name of the collection to operate upon
            query: A Pymongo query for the object to replace
            replacement: the data to insert in place of the original
        
        Return:
            The result of Pymongo Collection replace_one
        """
        collection = self.get_collection(collection)
        return collection.replace_one(query,
            self._transformer.transform_incoming(replacement))

    def delete_one(self, collection, query):
        """ A wrapper for the Pymongo Collection delete_one function that
        properly translates src/classes objects.
        
        Arguments:
            collection: the name of the collection to operate on
            query: A Pymongo query for the object to delete
        
        Return:
            The result of Pymongo Collection delete_one
        """
        collection = self.get_collection(collection)
        return collection.delete_one(
            self._transformer.transform_incoming(query))
