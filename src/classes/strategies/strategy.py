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
from src.classes.data import importance
from src.constants import logger
from src.constants import outcomes
from src.util import util

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

    ###########################################################################
    #                             Public Methods                              #
    ###########################################################################

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

    ###########################################################################
    #                  Methods Child Classes Should Overwrite                 #
    ###########################################################################

    def _run(self):
        """This private method actually computes a possible decision. It should
        be overridden by child classes.
        """
        raise NotImplementedError

    def _explain(self):
        """This private method actually logs the explanation. It should be
        overridden by child classes.
        """
        raise NotImplementedError


    ###########################################################################
    #                    Helper Methods Child Classes Can Use                 #
    ###########################################################################


    ###########################################################################
    #                            Finalizing the Decision                      #
    ###########################################################################

    def _finalize_decision(self, side, reasons, downside):
        """ A helper method, finalizes a given decision on a bill. It ensures
        that the outcome and reasons for a decision are updated in the decision
        object. It also sets the Strategy's private variable _success to True.
        
        Child classes can use this to finalize a decision they have made.
        
        Arguments:
            side: The decision on the bill either FOR or AGN
            reasons: a list of stances supporting the decision
            downside: a list of stances against the decision
        """
        self._success = True
        self._decision.result = side
        self._decision.reason = reasons
        self._decision.strategy = self._name

        # In Lisp code. Might not be needed now though.+
        # downside = util.flatten(downside)
        record = util.collect_bill_stances(downside)

        if record:
            self._decision.downside_record = record
            # Consider how to better compare
            eq_fun = lambda stance1, stance2: stance1.match(stance2)
            self._decision.downside = util.difference(downside, record, eq_fun)

        else:
            self._decision.downside = downside

    def _set_decision(self, result):
        """Sets the decision to be the given result (either FOR or AGN). This
        method then sets the reason and downside arrays and passes them to
        finalize_decision(...) to actually set self._decision.
        
        Arguments:
            result: The result of the decision either FOR or AGN
        """
        if result == outcomes.FOR:
            reason = self._decision.for_stances
            downside = self._decision.agn_stances
        elif result == outcomes.AGN:
            reason = self._decision.agn_stances
            downside = self._decision.for_stances
        else:
            logger.LOGGER.error("Result should be %s or %s. Got: %s" %
                (outcomes.FOR, outcomes.AGN, result))
            return

        self._finalize_decision(result, reason, downside)


    ###########################################################################
    #                          Majority/ Consensus                            #
    ###########################################################################

    def _majority(self):
        """Determines if there is a simple majority of stances either for or
        against the bill. It calculates the length of the for_stances and
        agn_stances to see which one is larger.
        
        Returns:
            outcomes.FOR if there are more FOR stances, outcomes.AGN if there
            are more AGN stances, None otherwise
        """
        fors = len(self._decision.for_stances)
        agns = len(self._decision.agn_stances)

        if fors > agns:
            return outcomes.FOR
        elif agns > fors:
            return outcomes.AGN
        else:
            return None

    def _consensus(self):
        """ Determines if there is a general consensus among different sources
        of stances. This function checks all the different MI_... stance lists
        that determine whether a given source of stances (like a credo or norms)
        is FOR or AGN the bill. 
        
        A consensus is met if all MI sources are either neutral or come down on
        the same side.
        
        Returns:
            outcomes.FOR if the sources agree on voting FOR the bill,
            outcomes.AGN if the sources agree on voting AGN the bill, None 
            otherwise.
        """

        MI_stances = [self._decision.MI_stance, self._decision.MI_group,
                      self._decision.MI_credo, self._decision.MI_record,
                      self._decision.MI_norm]

        # Removes MI sources that were never set.
        filter_fun = lambda x : x != None
        MI_stances = filter(filter_fun, MI_stances)

        # Maps MI_stances to be a list only of the outcomes.
        filter_fun = lambda result_data : result_data.outcome
        MI_stances = map(filter_fun, MI_stances)

        # Check to see if the sources are all in favor of one outcome.
        if len(util.remove_duplicates(MI_stances)) == 1 :
            return MI_stances[0]
        else:
            return None

    ###########################################################################
    #                            Explain Functions                            #
    ###########################################################################

    def _explain_simple_consensus(self):
        """ This is a helper method for explain. It is a general explanation
        for when a consensus is found and used to make a decision.
        """
        result = self._decision.result
        logger.LOGGER.info("Found a consensus %s this bill." % result)
        logger.LOGGER.info("The most important stances are all %s this bill:" % result)
        pairs = [["Group", self._decision.MI_group],
                 ["Credo", self._decision.MI_credo],
                 ["Record", self._decision.MI_record],
                 ["Norm", self._decision.MI_norm]]
        for pair in pairs:
            name = pair[0]
            result_data = pair[1]
            if result_data:
                logger.LOGGER.info(name)
                logger.LOGGER.info(result_data)

    def _explain_simple_majority(self):
        result = self._decision.result
        logger.LOGGER.info("Found a simple majority %s this bill." % self._decision.result)
        self._log_majority_stances(result)
        self._log_majority_stances(outcomes.OPPOSITE[result])

    def _log_majority_stances(self, result):
        stances = self._decision.for_stances
        if result == outcomes.AGN:
            stances = self._decision.agn_stances
        logger.LOGGER.info("Stances %s this bill: %d" % (result, len(stances)))
        logger.LOGGER.info(stances)
