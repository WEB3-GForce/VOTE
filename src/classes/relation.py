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

from src.classes.printable_object import PrintableObject

class Relation(PrintableObject):
    """Defines a relationship between two entities.
    
    A Relation object models a relationship in the real world. Most commonly,
    members have Relation objects describing their relations with groups.
    Relations are important since members often adopt goals (Stances) from
    groups they care about.
    
    Attributes:
    
        source: An identifier for the source of the relationship. It could be
            an id, name, synonym, etc.
        source_db: The name of the database table that source belongs to.
        group: An identifier for the object of the relationship. It could be
            an id, name, synonym etc.
        importance: How important the relationship is to the source.
        side: whether this relationship is positive (PRO) or negative (CON)
    """

    def __init__(self, entries=None):
        """Constructs a new Relation based upon a dictionary of attributes.
        
        Initializes the instance variables to default values and then updates
        them with the entries provided in the hash.
        
        Arguments:
            entries: The hash of the attribute values of the form
                {"attribute_1" : "value", "attribute2" : "value", ...}
        """

        self.source = None
        self.source_db = None
        self.group = None
        self.importance = None
        self.side = None

        if entries is not None:
            self.__dict__.update(entries)

