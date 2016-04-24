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

class ChangeOfHeartStrategy(Strategy):
    """ From Professor Slade's Lisp code:
    
        ==================================================================
          7   Change of heart                         [C]  (CHANGE-OF-HEART)

          Remarks:       Reverse a credo/vote position on the record to accomodate
                         conflict in constituencies.
          Quote:         A foolish consistency is the hobgoblin of small minds.
          Rank:          "C"
          Test:          Credo importance is less than conflicting relation importance.
        ==================================================================
        
    In short, if the member's personal credo is split on the bill and there is
    a simple majority on the bill, vote in favor of the majority.
    """

    def __init__(self, decision, member, bill):
        """Constructs a new ChangeOfHeartStrategy.
        
        Arguments:
            decision: The Decision object the Strategy will attempt to compute
                a result for.
            member: A Member object of the member who is deciding on the bill
            bill: A Bill object of the bill being decided upon.
        """
        super(ChangeOfHeartStrategy, self).__init__(decision, member, bill)
        self._name = "Change of Heart"

    def _run(self):
        """Implements the logic of Change of Heart."""
        result = self._majority()
        if result and self._decision.split_credo:
            return self._set_decision(result)

    def _explain(self):
        """Explains the Change of Heart."""
        self._explain_simple_majority()
        msg = "The congressperson's credo is split, yet there is a majority %s this bill." % self._decision.result
        logger.LOGGER.info(msg)
        logger.LOGGER.info(self._decision.split_credo)

