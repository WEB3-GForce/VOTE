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
from src.constants import logger
from src.constants import outcomes

class NotGoodEnoughStrategy(Strategy):
    """ From Professor Slade's Lisp code:
    
        ==================================================================
          12  Not good enough                         [C]  (NOT-GOOD-ENOUGH)

          Remarks:       Bill importance is less than my own stances would call for.
                         For example, personal stance of A, bill importance of C.
          Quote:         I would have voted for a stronger bill.
                         This measure is a fraud.  It has no teeth in it.
          Rank:          "C"
          Test:          Compare importance of bill stance with own stances.  Check for disparity.
        ==================================================================
        
    If there is a majority for the bill and the side favoring the majority is
    more important that the side against, vote in line with the majority.
    """

    def __init__(self, decision, member, bill):
        """Constructs a new MinimizeAdverseEffectsStrategy.
        
        Arguments:
            decision: The Decision object the Strategy will attempt to compute
                a result for.
            member: A Member object of the member who is deciding on the bill
            bill: A Bill object of the bill being decided upon.
        """
        super(NotGoodEnoughStrategy, self).__init__(decision, member, bill)
        self._name = "Not Good Enough"

    def _run(self):
        """Implements the logic of Not Good Enough."""
        result = self._majority()
        if result == outcomes.FOR:
            MI_upside_level = self._get_FOR_MI_level()
            MI_bill_level = self._get_FOR_MI_bill_level()
            if MI_upside_level > MI_bill_level:
                return self._set_decision(outcomes.AGN)

    def _get_FOR_MI_level(self):
        """Returns the value of the most important stance FOR the bill. Since
        this is only called if there is a majority for the bill, for_stances
        will always have a size greater than 1.        
        """
        stances = self._decision.for_stances
        stances.sort(key=lambda stance: stance.sort_key, reverse=True)
        return stances[0].importance

    def _get_FOR_MI_bill_level(self):
        """Returns the value of the most important FOR bill stance."""
        stances = self._bill.stances_for
        if not stances:
            return importance.Z
        stances.sort(key=lambda stance: stance.sort_key, reverse=True)
        return stances[0].importance

    def _explain(self):
        """Explains the Not Good Enough."""
        # Technically, the majority is FOR the bill but the decision is against
        # the bill. Hence, reverse them here so _eplain_simple_majority works
        # and then change it back.
        self._decision.result = outcomes.FOR
        self._explain_simple_majority()
        self._decision.result = outcomes.AGN

        msg = ("Even though the majority opinion favors this bill, the bill is too weak.\n" +
               "The importance of the agenda stances is greater than the bill stances.\n" +
               "Therefore, vote against the bill in protest.")
        logger.LOGGER.info(msg)

        mi_up_stance = self._decision.for_stances[0] if len(self._decision.for_stances) > 0 else None
        bill_up_stance = self._bill.stances_for[0] if len(self._bill.stances_agn) > 0 else None

        logger.LOGGER.info("Strong agenda stance:")
        logger.LOGGER.info(mi_up_stance)
        logger.LOGGER.info("Weak bill stance:")
        logger.LOGGER.info(bill_up_stance)

