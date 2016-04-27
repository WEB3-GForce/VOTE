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

class SimpleMajorityStrategy(Strategy):
    """ Checks to see if there is a simple majority on the bill (whether there
    are more stances FOR or AGN the bill) and decides with the majority.
    """

    def __init__(self, decision, member, bill):
        """Constructs a new SimpleMajorityStrategy.
        
        Arguments:
            decision: The Decision object the Strategy will attempt to compute
                a result for.
            member: A Member object of the member who is deciding on the bill
            bill: A Bill object of the bill being decided upon.
        """
        super(SimpleMajorityStrategy, self).__init__(decision, member, bill)
        self._name = "Simple Majority"

    def _run(self):
        """Implements the logic of Simple Majority."""
        result = self._majority()
        if result:
            return self._set_decision(result)

    def _explain(self):
        """Explains the Simple Majority decision."""
        self._explain_simple_majority()
