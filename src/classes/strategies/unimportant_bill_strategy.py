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

from src.classes.data import importance
from src.classes.strategies.strategy import Strategy
from src.constants import database as db_constants
from src.constants import logger
from src.constants import outcomes
from src.database.pymongodb import PymongoDB
from src.database import queries

class UnimportantBillStrategy(Strategy):
    """ From Professor Slade's Lisp code:

        ==================================================================
          4   Unimportant Bill                        [B]   (UNIMPORTANT-BILL)

          Date-open:     Monday, May 22, 1989
          Symbol:        STRATEGY.681
          Name:          "Unimportant Bill"
          Sort-key:      "BUnimportant Bill"
          Synonyms:      (UNIMPORTANT-BILL)
          Isa-depth:     ""
          Remarks:       Not much riding on this bill.

          Quote:         [Morrison:] some things that are close calls are not treated
                         as close calls because they're not important enough.  I mean
                         its very different if there's enough riding -- either substantively
                         or politically -- on a vote.  You might have exactly the same
                         tensions among the various priorities if you were to pull
                         this up, but it might be about how you spend $100,000 and you
                         say, [this doesn't matter].
          Rank:          "B"
          Test:          Importance of bill is minimal.
        ==================================================================        

    In short, if the bill has a low importance and there is a consensus for the
    decision, vote in line with the consensus.
    """

    def __init__(self, decision, member, bill):
        """Constructs a new UnimportantBillStrategy.
        
        Arguments:
            decision: The Decision object the Strategy will attempt to compute
                a result for.
            member: A Member object of the member who is deciding on the bill
            bill: A Bill object of the bill being decided upon.
        """
        super(UnimportantBillStrategy, self).__init__(decision, member, bill)
        self._name = "Unimportant Bill"

    def _run(self):
        """Implements the logic of Unimportant Bill."""
        result = self._consensus()
        bill_import = self._bill.importance
        if result and bill_import and bill_import <= importance.C:
            return self._set_decision(result)

    def _explain(self):
        """Explains the Unimportant Bill decision."""
        self._explain_simple_consensus()
        logger.LOGGER.info("And this bill has a low level of importance (%s)" % self._bill.importance)
