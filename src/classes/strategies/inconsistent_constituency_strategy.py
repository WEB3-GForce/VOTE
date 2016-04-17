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

class InconsistentConstituencyStrategy(Strategy):
    """ From Professor Slade's Lisp code:
    
        ==================================================================
          1   Inconsistent constituency               [B] @(INCONSISTENT-CONSTITUENCY)
         Same group on both sides of issue
        ==================================================================
        
    In short, if the MI stance sources have come to a consensus on a given
    course of action yet some groups are split on the issue, the member
    will decide in line with the consensus.
    """

    def __init__(self, decision, member, bill):
        """Constructs a new InconsistentConstituencyStrategy.
        
        Arguments:
            decision: The Decision object the Strategy will attempt to compute
                a result for.
            member: A Member object of the member who is deciding on the bill
            bill: A Bill object of the bill being decided upon.
        """
        super(InconsistentConstituencyStrategy, self).__init__(decision, member, bill)
        self._name = "Inconsistent Constituency"

    def _run(self):
        """Implements the logic of Inconsistent Constituency. Simply put, if
        there is a consensus toward a decision and some groups are divided on
        the issue, go with the consensus.
        """
        result = self._consensus()
        if self._decision.split_group and result:
            self._set_decision(result)

    def _explain(self):
        """Explains the Inconsistent Constituency."""
        self._explain_simple_consensus()
        logger.LOGGER.info("One or more groups have stances on both sides of this bill:")
        logger.LOGGER.info(self._decision.split_group)

