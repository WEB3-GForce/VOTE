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
from src.constants import logger

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
    
    Child classes should override the _run() and _explain() methods. They should
    also override __init__(...) to specify there own name. However, they are
    expected to keep the signature of __init__(...) exactly the same.
    
    Attributes:
        _name: The string name of this strategy
        _decision: The Decision object representing the decision the strategy is
            trying to compute
        _member: A Member object that represents the member who is making the
            decision
        _bill: A bill object that represents the bill being voted upon.
        _success: Whether or not this Strategy was successful in computing a
            result for the Decision object
    """

    def __init__(self, decision, member, bill):
        """Constructs a new Strategy.
        
        Arguments:
            decision: The Decision object the Strategy will attempt to compute
                a result for.
            member: A Member object of the member who is deciding on the bill
            bill: A Bill object of the bill being decided upon.
        """
        self._name = "Strategy"
        self._decision = decision
        self._member = member
        self._bill = bill
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
        self._run()

        if(self._success):
            logger.LOGGER.info("%s succeeded." % self._name)
            logger.LOGGER.info("%s will vote %s bill %s" %
                (self._member.full_name, self._decision.result,
                 self._bill.bill_number))
        else:
            logger.LOGGER.info("%s failed." % self._name)
        return self._success

    def _run(self):
        """This private method actually computes a possible decision. It should
        be overridden by child classes.
        """
        raise NotImplementedError

    def explain(self):
        """Explains why the strategy decided on a specific side (FOR or AGN)
        for its Decision object.
        
        run() must be called first. If run() has not been called or the strategy
        failed to make a decision, this method will log a warning and nothing
        else.
        
        If run() succeeds, it will log the rational for making the decision.
        """
        if not self._success:
            logger.LOGGER.info("%s failed to produce a decision." % self._name)
            return
        logger.LOGGER.info("Explaining decision...")
        self._explain()

    def _explain(self):
        """This private method actually logs the explanation. It should be
        overridden by child classes.
        """
        raise NotImplementedError