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
from src.constants import database as db_constants
from src.constants import logger
from src.constants import outcomes
from src.database.pymongodb import PymongoDB
from src.database import queries

class BestForTheCountryStrategy(Strategy):
    """ From Professor Slade's Lisp code:
    
        ==================================================================
          6   Best for the country                    [C]  (BEST-FOR-THE-COUNTRY)

          Remarks:       Take the broad view, over parochial interests.
          Quote:         The needs of the country, in this case, must come first.
          Rank:          "C"
          Test:          National interest in conflict with local interest.
        ==================================================================
        
    If there is a consensus on the bill and the country as a whole is in line
    with the consensus, vote with the consensus. If the country is split on
    the decision, fail.

    Attributes:
        _COUNTRY: The name of the group Country that represents the country as
            a whole
        _country_stances: A list of stances that the group Country has on the
            bill
    """

    def __init__(self, decision, member, bill):
        """Constructs a new BestForTheCountryStrategy.
        
        Arguments:
            decision: The Decision object the Strategy will attempt to compute
                a result for.
            member: A Member object of the member who is deciding on the bill
            bill: A Bill object of the bill being decided upon.
        """
        super(BestForTheCountryStrategy, self).__init__(decision, member, bill)
        self._name = "Best for the Country"

        # The identifier for the group Country
        self._COUNTRY = "Country"
        self._country_stances = []

    def _run(self):
        """Implements the logic of Best for the Country."""
        result = self._consensus()

        country = PymongoDB.get_db().find_one(db_constants.GROUPS,
            queries.group_query(self._COUNTRY))

        if not country:
            logger.LOGGER.warning("Country group not found in DB.")
            return

        filter_fun = lambda stance: queries.is_group_identified(stance.source, country)

        country_for = filter(filter_fun, self._decision.groups_for)
        country_agn = filter(filter_fun, self._decision.groups_agn)

        if result == outcomes.FOR and country_for and not country_agn:
            self._country_stances = country_for
            self._set_decision(result)
        elif result == outcomes.AGN and country_agn and not country_for:
            self._country_stances = country_agn
            self._set_decision(result)

    def _explain(self):
        """Explains the Best for the Country decision."""
        self._explain_simple_consensus()
        logger.LOGGER.info("The country as a whole has a stance %s this bill:" % self._decision.result)
        logger.LOGGER.info(self._country_stances)

