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

class Decision(PrintableObject):
    """" Decision objects are used to represent VOTE's predictions about how
    a given member will decide to vote on a bill. It contains state information
    used to make the decision along with the results of the decision itself.

    Attributes
        bill: the bill the decision is being made on
        member: the member making the decision
        for_stances: list of stances in favor of voting for the bill
        agn_stances: list of stances opposed to the bill
        con_rel_for_stances: list of stances in favor of the bill held by the
            opposition
        con_rel_agn_stances: list of stances opposed to the bill held by the
            opposition
        groups_for: list of groups in support of the bill
        groups_agn : list of groups opposed to the bill
        for_norms: norms associated with for_stances
        agn_norms: norms associated with agn_stances
        for_bill_norms: norms associated with bill's for stances
        agn_bill_norms: norms associated with bill's agn stances
        split_group: list of groups on both sides
        split_record: whether the member's voting record indicates the member
            would be on both sides of the bill. An empty list if the member is
            not split. Otherwise, contains the split stances.
        split_credo: whether the member's personal credo is split. An empty list
            if the credo is not split. Otherwise, contains the split stances.
        MI_stance: for/agn/nil -- >important? for agn
        MI_group: for/agn/nil
        MI_credo: for/agn/nil
        MI_record: for/agn/nil
        MI_norm: for/agn/nil
        result: whether to vote FOR or AGN the bill
        strategy: decision strategy used to arrive at result
        reason: stances supporting the result
        downside: negative aspects of the decision
        downside_record: voting record stances supporting the downside
    """

    def __init__(self, entries=None):
        """Constructs a new Decision based upon a dictionary of attributes.
        
        Initializes the instance variables to default values and then updates
        them with the entries provided in the hash.
        
        Arguments:
            entries: The hash of the attribute values of the form
                {"bill" : "some_bill_identifier",
                "member" : "some_member_identifier",
                ...}
        """
        # Attributes used in making the decision
        self.bill = None
        self.member = None
        self.for_stances = []
        self.agn_stances = []
        self.con_rel_for_stances = []
        self.con_rel_agn_stances = []
        self.groups_for = []
        self.groups_agn = []
        self.for_norms = []
        self.agn_norms = []
        self.for_bill_norms = []
        self.agn_bill_norms = []
        self.split_group = []
        self.split_record = []
        self.split_credo = []
        self.MI_stance = None
        self.MI_group = None
        self.MI_credo = None
        self.MI_record = None
        self.MI_norm = None

        # Attributes about the actual decision
        self.result = None
        self.strategy = None
        self.reason = None
        self.downside = None
        self.downside_record = []

        if entries is not None:
            self.__dict__.update(entries)
