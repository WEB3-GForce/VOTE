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

class Issue(PrintableObject):
    """"Represents a particular topic of interest or importance.
    
    Issues represent topics, goals, ideals, and values held by Congressmen and
    the public at large, for example CIVIL-RIGHTS, FAIRNESS, ELDERLY,
    HANDICAPPED, etc. Issues are key to the VOTE decision making strategy.
    Members and groups both hold stances on issues. Voting for or against a
    bill reflects having certain stances on issues. In many ways, issues are
    the main drivers of VOTE.
    
    Attributes:
        name: The name of the issue
        number: Whether the issue name is singular or plural
        type: What type of issue this is (e.g. ELDERLY is a GROUP, SPACE is a
            PROGRAM, EDUCATION is a POLICY)
        isa: A list of general categories that this issue falls under
            (e.g. SPACE is under FEDERAL-PROGRAMS, SPENDING is an ECONOMIC
            issue, AGE-DISCRIMINATION involves CIVIL-RIGHTS)
        synonyms: A list of synonyms for the name of this issue
        opposite: A list of issues that are the opposite of the current issue
        polarity: A description of the intrinsic position for this issue
            (e.g. EDUCATION means to "Support federal spending on education")
        pro_english_description: An English description of the issue biased
            favorably
        con_english_description: A pejorative English description of the issue

        pro_stances: A list of stances supporting this issue
        con_stances: A list of stances opposing this issue
        norm: The normative stance on this issue
    """

    def __init__(self, entries=None):
        """Constructs a new Issue based upon a dictionary of attributes.
        
        Initializes the instance variables to default values and then updates
        them with the entries provided in the hash.
        
        Arguments:
            entries: The hash of the attribute values of the form
                {"attribute_1" : "value", "attribute2" : "value", ...}
        """
        self.name = ""
        self.number = ""
        self.type = ""
        self.isa = []
        self.synonyms = []
        self.opposite = []
        self.polarity = ""
        self.pro_english_description = ""
        self.con_english_description = ""

        self.pro_stances = []
        self.con_stances = []
        self.norm = None

        if entries is not None:
            self.__dict__.update(entries)
