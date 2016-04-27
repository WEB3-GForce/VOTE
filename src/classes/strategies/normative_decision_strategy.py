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
from src.constants import outcomes
from src.constants import logger

class NormativeDecisionStrategy(Strategy):
    """ From Professor Slade's Lisp code:

        ==================================================================
          17  Normative decision                      [D] @(NORMATIVE)

          Remarks:       Decision reflects normative opinion on relevant issues.
          Rank:          "D"
          Test:          Bill stances match normative stances for given issues.
          Test-code:     STRAT-NORMATIVE
        ==================================================================
    
    
    In other words, if general sentiments are all on one side of a bill,
    vote in line with this normative position (e.g. The norm in America is to
    uphold Freedom of Speech).
    """

    def __init__(self, decision, member, bill):
        """Constructs a new NormativeDecisionStrategy.
        
        Arguments:
            decision: The Decision object the Strategy will attempt to compute
                a result for.
            member: A Member object of the member who is deciding on the bill
            bill: A Bill object of the bill being decided upon.
        """
        super(NormativeDecisionStrategy, self).__init__(decision, member, bill)
        self._name = "Normative Decision"

    def _run(self):
        """Implements the logic of Normative Decision."""
        for_norms = self._decision.for_bill_norms
        agn_norms = self._decision.agn_bill_norms

        if for_norms and not agn_norms:
            return self._finalize_decision(outcomes.FOR, for_norms, agn_norms)
        elif agn_norms and not for_norms:
            return self._finalize_decision(outcomes.AGN, agn_norms, for_norms)

    def _explain(self):
        """Explains the Normative Decision decision."""
        result = self._decision.result
        logger.LOGGER.info("Public opinion norms are all %s this bill:" % result)
        logger.LOGGER.info(self._decision.reason)
        logger.LOGGER.info("There are no norms %s this bill" % outcomes.OPPOSITE[result])
