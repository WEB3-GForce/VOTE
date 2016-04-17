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

from src.classes.strategies.strategy import Strategy
from src.constants import logger
from src.constants import outcomes

class NonPartisanDecisionStrategy(Strategy):
    """ From Professor Slade's Lisp code:
    
        ==================================================================
          2   Non-partisan Decision                   [B]  (NON-PARTISAN)

          Remarks:       Vote of conscience or credo that violates party line.  Not a district vote.
          Quote:         Sometimes party loyalty demands too much. (JFK)
          Rank:          "B"
          Test:          Major conflict between credo and party stances.
        ==================================================================

    In short, if a member feels strongly about a particular bill but that
    person's party is against it, the person will vote in line with his/her
    convictions.
    """

    def __init__(self, decision, member, bill):
        """Constructs a new NonPartisanDecisionStrategy.
        
        Arguments:
            decision: The Decision object the Strategy will attempt to compute
                a result for.
            member: A Member object of the member who is deciding on the bill
            bill: A Bill object of the bill being decided upon.
        """
        super(NonPartisanDecisionStrategy, self).__init__(decision, member, bill)
        self._name = "Non-partisan Decision"

        self._opposing_groups = None

    def _run(self):
        """Implements the logic of Non-partisan Decision. Simply put, if one
        strongly cares about one's credo and one's party is against the credo,
        vote in line with one's convictions.
        
        To be more specific, stances in the member's credo must be of importance
        A, the highest possible.
        
        If defined, decision.MI_*** contain stances all of the same importance.
        Please see decision_analyze.py for more details.
        """
        credo = self._decision.MI_credo
        party = self._member.party
        self._opposing_groups = self._decision.groups_agn
        if credo and credo.outcome == outcomes.AGN:
            self._opposing_groups = self._decision.groups_for

        if credo is None or party is None or not self._opposing_groups:
            return

        mapfun = lambda stance: stance.source
        credo_stance = credo.data[0]
        if (party in map(mapfun, self._opposing_groups) and
            credo_stance.importance.most_important()):
            self._set_decision(credo.outcome)

    def _explain(self):
        """Explains the Non-partisan Decision."""
        credo = self._decision.MI_credo
        party = self._member.party

        filter_fun = lambda stance: party == stance.source
        party_stances = filter(filter_fun, self._opposing_groups)

        logger.LOGGER.info("The member's party (%s) has stances %s this bill:"
                    % (party, outcomes.OPPOSITE[credo.outcome]))
        logger.LOGGER.info(party_stances)
        logger.LOGGER.info("While the member has a strong personal stance %s the bill:" % credo.outcome)
        logger.LOGGER.info(credo.data)

