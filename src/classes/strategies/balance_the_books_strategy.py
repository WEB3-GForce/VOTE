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
from src.util import util

class BalanceTheBooksStrategy(Strategy):
    """ From Professor Slade's Lisp code:

        ==================================================================
          5   Balance the books                       [C]  (BALANCE-THE-BOOKS)

          Remarks:       Offset current vote with past or future votes.
          Quote:         I know you are upset with this vote, but I have always been there in the
                           past, and I shall be there in the future.
                         I will make it up to you.
                         (point to specific past votes)
          Rank:          "C"
        ==================================================================

        This is also the same as:
        
        ==================================================================
          11  Mixed constituency                      [C]  (MIXED-CONSTITUENCY)

          Remarks:       E.g., rural/urban. can justify pro-rural vote to urbans by
                         pointing to other constituency, and vice-versa.
          Rank:          "C"
          Test:          District must be divided and there should be symmetry on stances.
        ==================================================================

    In short, if there is a majority opinion on the bill and the member's voting
    history shows that the member is split on the decision, go with the majority
    """

    def __init__(self, decision, member, bill):
        """Constructs a new BalanceTheBooksStrategy.
        
        Arguments:
            decision: The Decision object the Strategy will attempt to compute
                a result for.
            member: A Member object of the member who is deciding on the bill
            bill: A Bill object of the bill being decided upon.
        """
        super(BalanceTheBooksStrategy, self).__init__(decision, member, bill)
        self._name = "Balance the Books"

    def _run(self):
        """Implements the logic of Balance the Books."""
        result = self._majority()
        if result and self._decision.split_record:
            return self._set_decision(result)

    def _explain(self):
        """Explains the Balance the Books decision."""
        self._explain_simple_majority()
        logger.LOGGER.info("The record supports positions on both sides of the bill.")
        logger.LOGGER.info(outcomes.FOR)
        logger.LOGGER.info(util.collect_bill_stances(self._decision.for_stances))

        logger.LOGGER.info(outcomes.AGN)
        logger.LOGGER.info(util.collect_bill_stances(self._decision.agn_stances))