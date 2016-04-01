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
import itertools

from src.classes.stance import Stance
from src.constants import database as db_constants
from src.constants import importance
from src.constants import logger
from src.constants import outcomes
from src.database import queries
from src.database.pymongodb import PymongoDB
from src.util import util

def update_decision_metrics(decision):
    """Updates the decision object based on stances for and agn the decision.
    See the helper methods for more details.
    
    Briefly, the function calculates the norms for the issues that it
    considers, sorts the stances based on their source (group, member, bill),
    determines if the member, groups, or bill stances are split on the decision,
    and determines which side the different parties (group, member, bill)
    would support.    
    """
    _update_regular_stances(decision)
    _update_MI_stances(decision)


def _update_regular_stances(decision):
    """ Updates the various stances within decision. In particular, this
    function calculates norms, determines the stances groups have on the issue,
    and determines split groups, credos, voting records, etc.
    
    Arguments:
        decision: The decision object to update
    """
    fors = decision.for_stances
    agns = decision.agn_stances
    bill = PymongoDB.get_db().find_one(db_constants.BILLS,
        queries.bill_query(decision.bill))


    decision.for_norms = _check_norms(fors)
    decision.agn_norms = _check_norms(agns)

    if bill is None:
        logger.LOGGER.error("Decision bill not found.")
    else:
        decision.for_bill_norms = _check_norms(bill.stances_for)
        decision.agn_bill_norms = _check_norms(bill.stances_agn)


    decision.groups_for = _collect_groups(fors)
    decision.groups_agn = _collect_groups(agns)

    # Equality is defined by seeing if a stance has the same source as another.
    # This is needed to detect split groups. However, the stances are not
    # equal to each other in the normal sense. Hence, the intersection is done
    # twice to get all unique stances.
    eq_fun = lambda stance1, stance2: stance1.source == stance2.source
    for_intersect = util.intersect(decision.groups_for,
        decision.groups_agn, eq_fun)
    agn_intersect = util.intersect(decision.groups_agn,
        decision.groups_for, eq_fun)
    decision.split_group = for_intersect + agn_intersect

    for_bills = _collect_bills(fors)
    agn_bills = _collect_bills(agns)
    if for_bills and agn_bills:
        decision.split_record = for_bills + agn_bills

    for_credo = _collect_credo(fors)
    agn_credo = _collect_credo(agns)
    if for_credo and agn_credo:
        decision.split_credo = for_credo + agn_credo


def _check_norms(stances):
    """Filters a given list of stances to contain only those that are normative.
    
    Arguments:
        stances: the list of stances to filter.
        
    Returns:
        The filtered list with duplicates removed.
    """
    filter_fun = lambda stance: _normative_stance(stance)
    norms = filter(filter_fun, stances)
    return util.remove_duplicates(norms) if norms else []


def _normative_stance(stance):
    """Checks if a given stance is the normative stance on the issue (i.e. the
    way most people in the country feel about the issue).
    
    Argument:
        stance: the stance to check
        
    Returns:
        True if the stance is normative, False otherwise.
    """
    stance_issue = PymongoDB.get_db().find_one(db_constants.ISSUES,
        queries.issue_query(stance.issue))
    if stance_issue and stance_issue.norm:
        return stance.match(stance_issue.norm)
    return False


def _update_MI_stances(decision):
    """This function takes the stances for and against the decision and checks
    which side is the stronger one. It checks this for stances from groups, the
    member making the decision, the bill that will be decided upon, and the
    normative stances on the issues from decision.for_norms and
    decision.agn_norms.

    Arguments:
        decision: the decision object to update.        
    """
    decision.MI_stance = _MI_stances(decision)
    decision.MI_group = _MI_stances(decision, db_constants.GROUPS)
    decision.MI_credo = _MI_stances(decision, db_constants.MEMBERS)
    decision.MI_record = _MI_stances(decision, db_constants.BILLS)
    decision.MI_norm = _compare_stances(decision.for_norms, decision.agn_norms)


def _MI_stances(decision, db_source=None):
    """Updates a specific MI_stance such as MI_stance or MI_group. It take the
    for and agn stances for the decision, filters them by the appropriate
    database, and then calls compare_stances to determine which side is
    strongest.

    Arguments:
        decision: the decision object to update
        db_source: the name of the database to filter stances by. 
        
    Returns:
        A list showing the side that is stronger. It is of the form:
            
            [[FOR|AGN], List_Of_Compelling_Stances_From_Winning_Side]
    """
    fors = decision.for_stances
    agns = decision.agn_stances

    if db_source is not None:
        fors = _collect_source_type(db_source, fors)
        agns = _collect_source_type(db_source, agns)
    return _compare_stances(fors, agns)


def _collect_source_type(db, stances):
    """Filters a list of stances based on the database they are derived from.
    
    Arguments:
        db: the source database to match
        stances: the list of stances to filter.
        
    Returns:
        The filtered list.
    """
    filter_fun = lambda stance : stance.source_db == db
    return filter(filter_fun, stances)

# Extensions to collect_source_type. Simple lambdas that collect from a
# particular DB like groups
_collect_groups = lambda stances: _collect_source_type(db_constants.GROUPS, stances)
_collect_credo = lambda stances: _collect_source_type(db_constants.MEMBERS, stances)
_collect_bills = lambda stances: _collect_source_type(db_constants.BILLS, stances)


def _compare_stances(fors, agns):
    """This functions compares the stances to see which side has the most
    compelling reasons. It does so by checking which side has the largest number
    and most important stances supporting it.
    
    Arguments:
        fors: the list of stances supporting the bill to decide on
        agns: the list of stances against the bill to decide on
                    
    Returns:
        A list containing the strongest arguments for or against the bill.
        Returns an empty list if both sides are equally compelling.

    Notes:
        Both lists are first sorted by importance. Then, it goes through and
        compares each stance.
            
        If one list runs out before the other, the longest list is considered
        to have the most compelling stances.
            
        If one list is found to have a stance of stronger importance than
        the other on a give iteration of the for loop, that list is
        considered to be the most important and is chosen.
    """
    fors.sort(key=lambda stance: stance.sort_key, reverse=True)
    agns.sort(key=lambda stance: stance.sort_key, reverse=True)

    # base_stance is used in the enum. Once an array runs out of stances,
    # this will be mapped to be compared to the stances in the other list. Since
    # Z is not an importance actually assigned in the DB, this is guaranteed to
    # fail so that the longer list will be detected as the winner.
    #
    # The sort key is also needed to properly set the default. It will take the
    # source key from whichever array will last longer. This will ensure that
    # the stance is less than the next key it will be compared to.
    temp_stance = None
    if fors and len(fors) > len(agns):
        temp_stance = fors[0]
    elif agns and len(agns) > len(fors):
        temp_stance = agns[0]

    base_stance = Stance()
    base_stance.importance = importance.Z
    base_stance.sort_key = temp_stance._sort_key if temp_stance else None

    enum = enumerate(itertools.izip_longest(fors, agns, fillvalue=base_stance))
    for index, (a_for, an_agn) in enum:
        if a_for.sort_key > an_agn.sort_key:
            return [outcomes.FOR, _remove_less_important(fors[index:])]
        if an_agn.sort_key > a_for.sort_key:
            return [outcomes.AGN, _remove_less_important(agns[index:])]
    return []


def _remove_less_important(stances):
    """Removes all stances that are not as important as the first stance in the
    list.

    Arguments:
        stances: the stances to purge
                    
    Returns:
        The new stances list that contains only stances that are greater than or
        equal to the importance of the first stance in the original list.              
    """
    filter_fun = lambda stance : stance.sort_key >= stances[0].sort_key
    return filter(filter_fun, stances)
