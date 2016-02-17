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

class Member(PrintableObject):
    """"This class represents a particular member of Congress.
    
    This class encapsulates information about a member important for identifying
    the member (such as full name) along with special state that is needed to
    predict how a member might vote (such as voting history, personal stances
    on issues, and relationships with other groups).
    
    Attributes:
        full_name: The full name of the member
        first_name: The first name of the member
        last_name: The last name of the member
        gender: The gender of the member, either MALE or FEMALE
        district: The name of the district from which the member was elected
        term_start: The year the member was elected to Congress
        term_end: The year the member left Congress
        party: The political party affiliation of the member
        committees: A list of committees on which the member serves

        voting_record: A list of votes on previous bills. Formatted as:
            [["BillNumber1", "FOR|AGN"], ["BillNumber2", "FOR|AGN"], ...]         
        credo: A list of stances personal to this member
        relations: A list of relations the member has with groups

        stances: The member's stances on issues inferred from voting_record
        pro_rel_stances: A list of stances inferred from PRO relationships
        con_rel_stances: A list of stances inferred from CON relationships
        stance_sort_key: A key used to determine how stances should be sorted.
    """

    def __init__(self, **entries):
        """Constructs a new Member based upon a dictionary of attributes.
        
        Initializes the instance variables to default values and then updates
        them with the entries provided in the hash.
        
        Arguments:
            **entries: The hash of the attribute values of the form
                {"full_name" : "some_name", "first_name" : "some_first_name",
                ...}
        """
        # Attributes that identify the member.
        self.full_name = ""
        self.first_name = ""
        self.last_name = ""
        self.gender = None
        self.district = ""
        self.term_start = None
        self.term_end = None
        self.party = None

        # Attributes that identify the stances and groups the member cares about
        self.voting_record = []  
        self.credo = []
        self.relations = []

        # Attributes that are populated when VOTE is run and when deciding how
        # the member will vote.
        self.stances = []
        self.pro_rel_stances = []
        self.con_rel_stances = []
        self.stance_sort_key = None
        
        self.__dict__.update(entries)
