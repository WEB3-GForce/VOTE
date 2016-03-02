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

class Group(PrintableObject):
    """"Represents information about a given political group (such as Democrats
    or Republicans).
    
    Groups represent nearly any entity that can have relationships with
    Congressmen. They could be lobby groups, political parties, constituent
    groups, etc. There are also special groups such as COUNTRY which represent
    the nation as a whole and the general attitudes of the people.

    Attributes: 
        name: The name of the group
        number: Whether the group name is singular or plural
        synonyms: A List of synonyms of the group name
        pro_english_description: An English description of the group biased
            favorably
        con_english_description: A pejorative English description of the group                

        issues: A list of issues importance to this group
        stances: A list of stances the group has on several issues
        norm: The normative relation to this group
    """

    def __init__(self, entries=None):
        """Constructs a new Group based upon a dictionary of attributes.
        
        Initializes the instance variables to default values and then updates
        them with the entries provided in the hash.
        
        Arguments:
            entries: The hash of the attribute values of the form
                {"attribute_1" : "value", "attribute2" : "value", ...}
        """
        self.name = ""
        self.number = ""
        self.synonyms = []
        self.pro_english_description = ""
        self.con_english_description = ""
        self.issues = []
        self.stances = []
        self.norm = None

        if entries is not None:
            self.__dict__.update(entries)
