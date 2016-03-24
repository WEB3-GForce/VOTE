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
from src.constants import database as db_constants

class VoteTransform(object):
    """ This class provides methods to encode and decode src/classes objects
    into json. Given a json object, the functions work recursively to ensure
    that substructures are properly converted.
    
    The code is inspired from the now deprecated SonManipulator of Pymongo.
    http://api.mongodb.org/python/current/examples/custom_type.html
    
    The following methods are the public API for this class:

        transform_incoming
        transform_outgoing
        
    The names reference when they should be used, i.e. whether data is going
    into or out of the database.
    
    The encoding works as follows:
    
        1. A json object or an object from src/classes is passed in
        
            {
              ...
              "issues" : [Issue, Issue, Issue]
            }
            
            Member

        2. The object is traversed recursively to find all instances of
        "src/classes" objects
        
        3. When such an object is found, it is converted as follows:
        
            Object -> {"_type": Object_class,
                       "object_instance_value1" : ..., ...}

            e.g.
            
            Member -> {"_type": "Member", ... }
            
            The rest of the dictionary contains the entries of Member.__dict__
            
        4. Once all objects are converted, the resulting json is returned to
        the user
        
    The decoding works as follows:
    
        1. A json object is passed in
        
        2. The object is traversed recursively to find dictionaries representing
        "src/classes" objects
        
        3. If the dictionary has a "_type" key corresponding to a "src/classes"
        class, the dictionary is used to construct a new object of the
        corresponding class. The "_type" key is removed.
        
        4. Once all objects are converted, the resulting json is returned.
        
            a. NOTE: if the initial json represents a "src/classes" object, the
            decoded object is returned instead.
    """

    def _encode_custom_class(self, value):
        """" Translates a "src/classes" object into json.
        
        Arguments:
            value: the "src/classes" object to encode
            
        Returns:
            The encoding of the "src/classes" object or None if the value does
            not represent such an object.
        """
        for custom_class in db_constants.DB_CUSTOM_CLASSES:
            if isinstance(value, custom_class):
                transformed_dict = self.transform_incoming(
                    copy.deepcopy(value.__dict__))
                transformed_dict[db_constants.ENTRY_TYPE] = (
                    custom_class.__name__)
                return transformed_dict
        return None

    def _encode_list(self, input_list):
        """ Encodes a list and its values into json."""
        new_list = []
        for item in input_list:
            new_list.append(self._encode(item))
        return new_list

    def _encode(self, value):
        """ Handles encoding of a value. It relies upon helper methods to encode
        dictionaries, lists, "src/classes" objects, and other data types."
        
        Arguments:
            value: the data to encode
        
        Returns:
            A json encoding of value
        """
        if isinstance(value, dict):
            return self.transform_incoming(value)
        elif isinstance(value, list):
            return self._encode_list(value)
        else:
            encoded_class = self._encode_custom_class(value)
            if encoded_class is not None:
                return encoded_class
            else:
                return value

    def _decode_custom_class(self, value):
        """" Translates json into a "src/classes" object.
        
        Arguments:
            value: the json to decode
            
        Returns:
            The decoded "src/classes" object or None if the value does
            not represent such an object.
        """
        ENTRY_TYPE = db_constants.ENTRY_TYPE
        for custom_class in db_constants.DB_CUSTOM_CLASSES:
            if (ENTRY_TYPE in value and
                value[ENTRY_TYPE] == custom_class.__name__):
                value.pop(ENTRY_TYPE)
                transformed_hash = self.transform_outgoing(value)
                return custom_class(transformed_hash)
        return None

    def _decode_list(self, input_list):
        """ Decodes a list and its values from json."""
        new_list = []
        for item in input_list:
            new_list.append(self._decode(item))
        return new_list

    def _decode(self, value):
        """ Handles decoding of a value. It relies upon helper methods to decode
        dictionaries, lists, "src/classes" objects, and other data types.
        
        Arguments:
            value: the data to decode
        
        Returns:
            A json decoding of the value.
        """
        if isinstance(value, dict):
            decoded_class = self._decode_custom_class(value)
            if decoded_class is not None:
                return decoded_class
            else:
                return self.transform_outgoing(value)
        elif isinstance(value, list):
            return self._decode_list(value)
        else:
            return value

    def transform_incoming(self, son):
        """ The public encoding method. Encodes a json object or a
        "src/classes" object into a json object ready to be used by Pymongo.
        Recursively goes through the json object and converts any "src/classes"
        objects into json.
        
        Arguments:
            son: the json to encode or an object from "src/classes"
        
        Returns:
            An encoded json object ready to be used with the Pymongo database
        """
        check = lambda custom_class: isinstance(son, custom_class)
        if any(check(a_class) for a_class in  db_constants.DB_CUSTOM_CLASSES):
            return self._encode_custom_class(son)

        for (key, value) in son.items():
            son[key] = self._encode(value)
        return son

    def transform_outgoing(self, son):
        """ The public decoding method. Decodes "src/classes" objects in the
        json object so that they are ready to be used by VOTE. If the json
        object  provided represents a "src/classes" objects, a new object will
        be made automatically.
        
        Arguments:
            son: the json to decode
        
        Returns:
            The json object or an object from "src/classes" which was encoded
        """
        custom_class = self._decode_custom_class(son)
        if custom_class:
            return custom_class
        for (key, value) in son.items():
            son[key] = self._decode(value)
        return son
