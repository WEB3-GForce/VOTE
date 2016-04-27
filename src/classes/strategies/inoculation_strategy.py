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

class InoculationStrategy(Strategy):
    """ From Professor Slade's Lisp code:

        ==================================================================
          8   Inoculation                            [C]  (INOCULATION)

              Remarks:       Decision which may prove to be unpopular later on.
                             Need to begin laying groundwork for defense early on.
              Rank:          "C"
              Test:          Low priority stances, pro or con.
        ==================================================================
        
    If groups a member cares about are divided on the issue (some groups are
    for while other groups are against), then the member will decide for the
    majority only if none of the groups care strongly about the bill.
    
    Note that the divided_groups mentioned above is different from split_groups,
    where an individual group is divided on the issue. In this strategy, some
    groups support FOR while others support AGN.
    """

    def __init__(self, decision, member, bill):
        """Constructs a new InoculationStrategy.
        
        Arguments:
            decision: The Decision object the Strategy will attempt to compute
                a result for.
            member: A Member object of the member who is deciding on the bill
            bill: A Bill object of the bill being decided upon.
        """
        super(InoculationStrategy, self).__init__(decision, member, bill)
        self._name = "Inoculation"

    def _run(self):
        """Implements the logic of InoculationStrategy."""
        if not self._decision.groups_for or not self._decision.groups_agn:
            return

        divided_groups = self._decision.groups_for + self._decision.groups_agn
        divided_groups.sort(key=lambda stance: stance.sort_key, reverse=True)

        result = self._majority()
        if result and divided_groups[0].importance <= importance.C:
            return self._set_decision(result)

    def _explain(self):
        """Explains the Change of Heart."""
        self._explain_simple_majority()
        msg = ("Important groups are on both sides of the issue.\n" +
               "However, their stances are not extremely important to them.\n" +
               "This may call for additional explaining later.")
        logger.LOGGER.info(msg)
        logger.LOGGER.info(outcomes.FOR)
        logger.LOGGER.info(self._decision.groups_for)
        logger.LOGGER.info(outcomes.AGN)
        logger.LOGGER.info(self._decision.groups_agn)
