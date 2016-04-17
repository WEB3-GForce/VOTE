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

class NotConstitutionalStrategy(Strategy):
    """ From Professor Slade's Lisp code:
    
        ==================================================================
          3   Not constitutional                      [B]  (NOT-CONSTITUTIONAL)

          Remarks:       Vote against a measure that would be struck down by
                         the Supreme Court.
          Rank:          "B"
        ==================================================================
        
    If there is a consensus against the bill and the bill is unconstitutional,
    vote AGN the bill. This means that the decision's AGN stances has a stance
    FOR the constitution.
    
    Attributes:
        _CONSTITUTION: The name of the issue Constitution
        _non_constitutional_stances: A list of stances on the Constitution issue
            that would support voting against the bill
    """

    def __init__(self, decision, member, bill):
        """Constructs a new NotConstitutionalStrategy.
        
        Arguments:
            decision: The Decision object the Strategy will attempt to compute
                a result for.
            member: A Member object of the member who is deciding on the bill
            bill: A Bill object of the bill being decided upon.
        """
        super(NotConstitutionalStrategy, self).__init__(decision, member, bill)
        self._name = "Not Constitutional"

        # The identifier for the constitution
        self._CONSTITUTION = "Constitution"
        self._non_constitutional_stances = []

    def _run(self):
        """Implements the logic of Not Constitutional."""
        constitution = PymongoDB.get_db().find_one(db_constants.ISSUES,
            queries.issue_query(self._CONSTITUTION))

        if not constitution:
            logger.LOGGER.warning("Constitution issue not found in DB.")
            return

        result = self._consensus()
        filter_fun = lambda stance : queries.is_issue_identified(stance.issue, constitution)
        self._non_constitutional_stances = filter(filter_fun, self._decision.agn_stances)
        if result == outcomes.AGN and self._non_constitutional_stances:
            return self._set_decision(outcomes.AGN)

    def _explain(self):
        """Explains the Not Constitutional decision."""
        self._explain_simple_consensus()
        logger.LOGGER.info("There are constitutional grounds for opposing this bill:")
        logger.LOGGER.info(self._non_constitutional_stances)
