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

class VoteTally(PrintableObject):
    """This class is used to keep track of how many votes there are FOR and
    AGN a bill. This is used to predict whether a bill will be PASSED or
    REJECTED. For testing, the tally of votes can be acquire for bills that have
    already been decided upon. However, the ideal is that this field would be
    dynamically updated by VOTE as it predicts how members will vote for a
    particular bill.
    
    Attributes:
        outcome: The outcome of Congress on the bill (PASSED or REJECTED).
        for_votes: The number of votes in favor of the bill.
        agn_votes: The number of votes against the bill.
        party_votes: A hash of the form:
        
            {"political_party_name": {outcomes.FOR_VOTES : 10,
                outcomes.AGN_VOTES : 20}
            
            In other words, given a political party, the hash returns another
            hash that contains the number of votes the party had for the bill
            and the number of votes the party had against the bill.
    """

    def __init__(self, entries=None):
        """Constructs a new VoteTally based upon a dictionary of attributes.
        
        Initializes the instance variables to default values and then updates
        them with the entries provided in the hash.
        
        Arguments:
            entries: The hash of the attribute values of the form
                {"outcome" : "some_outcome", "for_votes" : 20,
                ...}
        """
        self.outcome = None
        self.for_votes = 0
        self.agn_votes = 0
        self.party_votes = {}

        if entries is not None:
            self.__dict__.update(entries)

    def vote_ratio(self):
        """Returns the ratio for votes to agn votes."""
        return self.for_votes / (self.agn_votes * 1.0)