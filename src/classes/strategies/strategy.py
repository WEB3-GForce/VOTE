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

from src.classes.printable_object import PrintableObject

class Strategy(PrintableObject):
    """"This is the parent class for all strategies. It defines an interface
    that all subclasses are expected to implement and abide by. Subclasses will
    implement the specific strategy logic.
    
    A Strategy provides a means for determining how a member will vote on a
    given bill. It takes in a Decision object and then uses the statistics
    within the object to determine how the member will vote. It applies specific
    heuristics to calculate this result. If successful, the Strategy records the
    predicted vote and the reason for this vote in the Decision object it
    is passed.
    
    Attributes:
        decision: The Decision object representing the decision the strategy is
            trying to compute
        success: Whether or not this Strategy was successful in computing a
            result for the Decision object
    """

    def __init__(self, decision):
        """Constructs a new Strategy.
        
        Arguments:
            decision: The Decision object the Strategy will attempt to compute
                a result for.
        """
        self._decision = decision
        self._success = False

    def run(self):
        """Runs the strategy attempting to compute a result on the Decision
        object it was constructed with.
        
        Upon success, the strategy populates attributes of the Decision object
        such as result, strategy, and reason. Upon failure, it does not modify
        the object.
        
        Returns:
            True if successful, False otherwise.
        """
        raise NotImplementedError

    def explain(self):
        """Explains why the strategy decided on a specific side (FOR or AGN)
        for its Decision object.
        
        run() must be called first. If run() has not been called or the strategy
        failed to make a decision, this method will log a warning and nothing
        else.
        
        If it succeeds, it will log the rational for making the decision.
        """
        raise NotImplementedError
