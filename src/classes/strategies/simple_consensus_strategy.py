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

class SimpleConsensusStrategy(Strategy):
    """ From Professor Slade's Lisp code:
    
        ==================================================================
            15  Simple consensus                        [C] @ (SIMPLE-CONSENSUS)

              Status:        "Active"
              Date-open:     Thursday, May 11, 1989
              Symbol:        STRATEGY.1018
              Name:          "Simple consensus"
              Sort-key:      "CSimple consensus"
              Synonyms:      (SIMPLE-CONSENSUS)
              Isa-depth:     ""
              Remarks:       The most important issues/groups/norms etc. concur.

              Rank:          "C"
              Test:          Check all most important features

              Test-code:     STRAT-SIMPLE-CONSENSUS
        ==================================================================        

    As the "Remarks" above say, the strategy checks if sources of different
    stances (the member's credo, the member's voting record, groups the member
    has positive relations with) all agree on how to vote on the bill.
    """

    def __init__(self, decision, member, bill):
        """Constructs a new SimpleConsensusStrategy.
        
        Arguments:
            decision: The Decision object the Strategy will attempt to compute
                a result for.
            member: A Member object of the member who is deciding on the bill
            bill: A Bill object of the bill being decided upon.
        """
        super(SimpleConsensusStrategy, self).__init__(decision, member, bill)
        self._name = "Simple Consensus"

    def _run(self):
        """Implements the logic of Simple Consensus."""
        result = self._consensus()
        if result:
            return self._set_decision(result)

    def _explain(self):
        """Explains the Simple Consensus decision."""
        self._explain_simple_consensus()
