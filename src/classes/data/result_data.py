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

class ResultData(PrintableObject):
    """This class defines a generic container other classes can use to store
    data resulting from some process. Typically, VOTE will need to store data
    in the following format:
        
        1. Outcome of some process
        2. Data that supports the outcome or describes what was being decided
        upon
    
    Since the data can often contain arrays, this class simplifies array
    indexing by allowing code to utilize accessor methods. 
    
    Attributes:
        outcome: The outcome of some process (like a vote). Typically FOR or AGN
        data: Data associated with the outcome. For example, it could be the
            bill that was voted upon.
    """

    def __init__(self, entries=None):
        """Constructs a new ResultData based upon a dictionary of attributes.
        
        Initializes the instance variables to default values and then updates
        them with the entries provided in the hash.
        
        Arguments:
            entries: The hash of the attribute values of the form
                {"outcome" : "some_outcome", "data" : "some_data",
                ...}
        """
        self.outcome = None
        self.data = None

        if entries is not None:
            self.__dict__.update(entries)
