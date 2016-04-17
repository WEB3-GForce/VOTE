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

class PopularDecisionStrategy(Strategy):
    """ From Professor Slade's Lisp code:
    
        ==================================================================
          0   Popular Decision                        [A] @(POPULAR)

          Remarks:       Vote is consistent with major constituencies.
          Quote:         I just try to vote my district.
                         I was sent to Washington to represent the way people back home feel.
                         This is what the vast majority want.
                         I owe it to my constituents if they feel that strongly about it. [Delegate stance]
          Rank:          "A"
          Test:          All stances on one side of bill.
          Example:
        ==================================================================
        
    As shown, Popular Decision is a strategy to use for "obvious" decisions. If
    there are only reasons to vote FOR and no reasons to vote AGN the bill (or
    vice versa), the popular side is chosen.
    """

    def __init__(self, decision, member, bill):
        """Constructs a new PopularDecisionStrategy.
        
        Arguments:
            decision: The Decision object the Strategy will attempt to compute
                a result for.
            member: A Member object of the member who is deciding on the bill
            bill: A Bill object of the bill being decided upon.
        """
        super(PopularDecisionStrategy, self).__init__(decision, member, bill)
        self._name = "Popular Decision"

    def _run(self):
        """Implements the logic of Popular Decision. Simply put, if there are
        only stances on one side of the issue, choose that side.
        """
        for_stances = self._decision.for_stances
        agn_stances = self._decision.agn_stances

        if for_stances and not agn_stances:
            self._finalize_decision(outcomes.FOR, for_stances, [])
        elif agn_stances and not for_stances:
            self._finalize_decision(outcomes.AGN, agn_stances, [])

    def _explain(self):
        """Explains the Popular Decision."""
        logger.LOGGER.info("All stances are %s this bill." % self._decision.result)
        logger.LOGGER.info(self._decision.reason)
        opposite = outcomes.OPPOSITE[self._decision.result]
        logger.LOGGER.info("There are no reasons to vote %s this bill." % opposite)

