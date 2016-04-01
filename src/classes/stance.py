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
from src.constants import logger
from src.constants import importance
from src.constants import stance_sort_key

class Stance(PrintableObject):
    """"Represents what an entity feels about a given issue.
    
    Stances are key to VOTE. In short, a stance tells what it's owner feels
    about a given issue. It defines how strongly the owner feels about the
    issue (importance), what side the owner is on (PRO, CON), etc. Typically,
    members and groups hold stances. Bills also contain stances denoting how
    voting for or against the bill will reflect what issues a member supports
    or disapproves of.
    
    Attributes:
        source: An identifier for the source of the relationship. It could be
            an id, name, synonym, etc.
        source_db: The name of the database table that source belongs to
        issue: An identifier of the issue the stance is on
        importance: An _Importance object denoting how important the stance
            is to the source
        side: Whether the source is for (PRO) or against (CON) the issue
        relation: An optional argument. If this stance was adopted from a
            relationship, this entry holds the relationship it was adopted from
        siblings: A list of related stances. The stance_alike(...) method must
            return true in order for a stance to be in this list
        sort_key: How stances should be sorted. This is typically set by the
            owner of the stance
    """

    def __init__(self, entries=None):
        """Constructs a new Stance based upon a dictionary of attributes.
        
        Initializes the instance variables to default values and then updates
        them with the entries provided in the hash.
        
        Arguments:
            entries: The hash of the attribute values of the form
                {"attribute_1" : "value", "attribute2" : "value", ...}
        """
        self.source = None
        self.source_db = None
        self.issue = None
        self.importance = None
        self.side = None
        self.relation = None
        self.siblings = []
        # This private value is used to specify the string value of the sort key
        # such as LOYALTY. This is set by calling the sort_key value. This is
        # private in the sense that this regular code should not set this
        # directly. However, this value can be read if another code needs to
        # determine what sort key is being used.
        self._sort_key = None

        if entries is not None:
            self.__dict__.update(entries)

    @property
    def sort_key(self):
        """Returns the key to use for sorting.
        
        Generally, the owner of the stance will define the sort key to be
        used. If this is not provided, stances are sorted in order of
        importance.
        """
        stance_import = self.importance
        relation_import = importance.B
        if self.relation and self.relation.importance:
            relation_import = self.relation.importance

        if self._sort_key == stance_sort_key.LOYALTY:
            return [relation_import, stance_import]
        elif self._sort_key == stance_sort_key.EQUITY:
            return [stance_import, relation_import]
        else:
            return self.importance

    @sort_key.setter
    def sort_key(self, keyword):
        """Sets the _sort_key based on the provided keyword.
        
        The _sort_key is a list of two _Importance objects: one as the primary
        key, the other as the secondary key. Which importance goes where is
        defined by the keyword argument.
        
        Arguments:
            keyword: a constant from src.constants.stance_sort_key that defines
                how to produce the sort_key.
        """
        if keyword in stance_sort_key.SORT_KEY_LIST:
            self._sort_key = keyword
        else:
            logger.LOGGER.error("Unknown sort_key: %s" % keyword)

    def match(self, stance2):
        """Determines if another stance matches this stance.
        
        Arguments:
            stance2: the other stance to check 
            
        Returns:
            Whether or not the stances match. Two stances match if they are on
            the same issue and take the same side on the issue.
        """
        return self.issue == stance2.issue and self.side == stance2.side


    def total_match(self, stance2):
        """Determines if another stance matches this stance totally.
        
        Arguments:
            stance2: the other stance to check 
        
        Returns:
            Whether the stances match totally. In addition to basic matching,
            the stances must also have the same importance.
        """
        return self.match(stance2) and self.importance == stance2.importance
