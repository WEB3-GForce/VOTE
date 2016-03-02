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

class Bill(PrintableObject):
    """ Represents a given bill in Congress.
    
    This class defines important information about bills that Congressmen
    vote upon. In particular, it provides a list of stances denoting what values
    can be inferred if a person votes for or against the bill.

    Attribute:
        bill_number:The number of the bill like "HR-3"
        name: The name of the bill
        synonyms: A list of synonyms the bill goes by
        importance: The intrinsic importance of the bill
        session: The session of Congress the bill belongs to
        majority_factor: A factor used to determine how many votes are needed
            for a bill to pass

        date_of_vote: The date the bill was voted upon
        vote_tally: A tally of the votes in the form:
            ["PASSED|REJECTED", #FOR, #AGN,
            {"REPUBLICANS": [#FOR, #AGN], "DEMOCRATS": [#FOR, #AGN], ...}]
        president_position: the president's position on the bill (FOR or AGN)

        sort_key: Determines how bills will be sorted.

        issues: A list of issues the bill addresses
        stances_for: What voting for this bill implies
        stances_agn: What voting against this bill implies
        inferred_stances_for: What voting for this bill implies inferred
            from remarks
        inferred_stances_agn: What voting against this bill implies inferred
            from remarks
        remarks: List of remarks on the bill
    """

    def __init__(self, entries=None):
        """Constructs a new Bill based upon a dictionary of attributes.
        
        Initializes the instance variables to default values and then updates
        them with the entries provided in the hash.
        
        Arguments:
            entries: The hash of the attribute values of the form
                {"attribute_1" : "value", "attribute2" : "value", ...}
        """
        # Attributes that specify what bill this is
        self.bill_number = ""
        self.name = ""
        self.synonyms = []
        self.importance = None
        self.session = ""
        self.majority_factor = None
        self.date_of_vote = None

        # Attributes that relay the result of the actual-life vote on the bill
        self.vote_tally = []
        self.president_position = None
        self.sort_key = None

        # Attributes responsible for holding stances on issues the bill touches
        self.issues = []
        self.stances_for = []
        self.stances_agn = []
        self.inferred_stances_for = []
        self.inferred_stances_agn = []
        self.remarks = []

        if entries is not None:
            self.__dict__.update(entries) 

