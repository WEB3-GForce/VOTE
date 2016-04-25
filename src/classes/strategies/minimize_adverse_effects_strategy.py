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

class MinimizeAdverseEffectsStrategy(Strategy):
    """ From Professor Slade's Lisp code:
    
        ==================================================================
            10  Minimize adverse effects                [C]  (MINIMIZE-ADVERSE-EFFECTS)

              Remarks:       Adverse effects are less important than the benefits of the vote.
              Quote:         Nothing's perfect.  You have to break a few eggs to make
                                 omelets.
              Rank:          "C"
              Test:          The downside results are lower in importance than the upside.
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
        super(MinimizeAdverseEffectsStrategy, self).__init__(decision, member, bill)
        self._name = "Minimize Adverse Effects"

    def _run(self):
        """Implements the logic of Minimize Adverse Effects."""
        result = self._majority()
        if result:
            MI_upside_level = self._get_MI_level(result)
            MI_downside_level = self._get_MI_level(outcomes.OPPOSITE[result])
            if MI_upside_level > MI_downside_level:
                return self._set_decision(result)

    def _get_MI_level(self, result):
        """Returns the value of the most important stance on a given side.
        
        Arguments:
            result: The side to get the most important stances from.
            
        Returns:
            The importance of the most important stance on the given side of
            the bill.
        """
        stances = self._decision.for_stances
        if result == outcomes.AGN:
            stances = self._decision.agn_stances

        if not stances:
            return importance.Z

        stances.sort(key=lambda stance: stance.sort_key, reverse=True)
        return stances[0].importance

    def _explain(self):
        """Explains the Minimize Adverse Effects."""
        self._explain_simple_majority()
        result = self._decision.result
        opposite = outcomes.OPPOSITE[result]
        msg = "The high priority %s stance is more important than the high priority %s stance" % (result, opposite)
        logger.LOGGER.info(msg)

        mi_for = self._decision.for_stances[0] if len(self._decision.for_stances) > 1 else None
        mi_agn = self._decision.agn_stances[0] if len(self._decision.agn_stances) > 1 else None

        logger.LOGGER.info(result)
        print_mi = mi_for if result == outcomes.FOR else mi_agn
        logger.LOGGER.info(print_mi)

        logger.LOGGER.info(opposite)
        print_mi = mi_for if opposite == outcomes.FOR else mi_agn
        logger.LOGGER.info(print_mi)
