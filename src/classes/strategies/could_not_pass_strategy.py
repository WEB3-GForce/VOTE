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

class CouldNotPassStrategy(Strategy):
    """ From Professor Slade's Lisp code:
    
        ==================================================================
          9   It couldn't pass                        [C]  (IT-COULD-NOT-PASS)

          Remarks:       Do not waste a vote on a symbolic measure.  Better to
                         build credibility and a consensus for the future.
          Quote:         Why waste a vote on a measure that has so little chance of passing.
          Rank:          "C"
          Test:          Bill has far higher importance (and low likelihood of passage)
                         but for issue stance consistent (but stronger than) with my own.
                         This is the flip side of not-good-enough.
        ==================================================================
        
    If there is a majority against the bill and if it is unlikely the bill will
    pass (aka, there are more agn_votes than for_votes in the vote_tally), vote
    with the majority.
    
    Attributes:
        _NOT_PASS_RATIO: The ratio of for votes to agn votes that is used as the
            threshold to determine if it is unlikely a bill will pass.
    """

    def __init__(self, decision, member, bill):
        """Constructs a new ChangeOfHeartStrategy.
        
        Arguments:
            decision: The Decision object the Strategy will attempt to compute
                a result for.
            member: A Member object of the member who is deciding on the bill
            bill: A Bill object of the bill being decided upon.
        """
        super(CouldNotPassStrategy, self).__init__(decision, member, bill)
        self._name = "Could Not Pass"

        self._NOT_PASS_RATIO = 1.0

    def _run(self):
        """Implements the logic of Could Not Pass."""
        result = self._majority()
        if result == outcomes.AGN and self._could_not_pass():
            return self._set_decision(result)

    def _could_not_pass(self):
        """ Determines whether the bill is unlikely to pass. A bill is unlikely
        to pass if its VoteTally vote_ratio is less than _NOT_PASS_RATIO. In
        other words, there are more AGN votes than FOR votes. How much more
        depends on the value of _NOT_PASS_RATIO.
        
        Returns:
            True if the bill could not pass, False if could pass
        """
        if self._bill.vote_tally:
            return self._bill.vote_tally.vote_ratio() < self._NOT_PASS_RATIO
        return False

    def _explain(self):
        """Explains the Could Not Pass."""
        self._explain_simple_majority()
        logger.LOGGER.info("The bill is unlikely to pass.")
        logger.LOGGER.info("Ratio of for votes to agn votes: %f" % self._bill.vote_tally.vote_ratio())

