from printable_object import PrintableObject
from database import *
from constants import *
from utils import *

def update_decision_metrics(decision):
    """Updates the decision object based on stances for and against the decision.
    See the code for more details.
    
        Briefly, the function calculates the norms for the issues that it
    considers, sorts the stances based on their source (group, member, bill),
    determines if the member, groups, or bill stances are split on the decision,
    and determines which side the categories (group, member, bill) would support.    
    """

    fors   = decision.for_stances
    agns   = decision.agn_stances
    bill   = get(BILL, {"_id" : decision.bill})

    if not bill:
        print "ERROR bill not found for decision metrics update."
        return False

    decision.number_for = len(fors)
    decision.number_agn = len(agns)

    decision.for_bnorms = check_norms(bill.stance_for)
    decision.agn_bnorms = check_norms(bill.stance_agn)

    decision.for_norms = check_norms(fors)
    decision.agn_norms = check_norms(agns)

    # Interestingly, the documentation seems to suggest this is a list of groups.
    # The code from decision.lisp seems to suggest this is a list of stances.
    # I will stick with the code for now till I have further clarification.
    decision.group_for = collect_groups(fors)
    decision.group_agn = collect_groups(agns)

    # split_groups also seems to have the similar problem. I solved this by
    # seeing if there are stances in both the FOR and AGN list that have the same
    # group. If so, the group is split on the issue. I then include all stances
    # by that group in this variable.
    eq_fun = lambda x, y: x.source == y.source
    decision.split_group = find_intersection(decision.group_for, decision.group_agn, eq_fun)

    decision.split_record = None
    for_bills = collect_bills(fors)
    agn_bills = collect_bills(agns)

    # Lisp syntax from decision.lisp would have just assigned this as
    # the agn_bills. I decided to assign it to for_bills + agn_bills to be able
    # to show all data. I think the code simply does a nil check on this value,
    # so the difference should not matter.
    if for_bills and agn_bills:
        decision.split_record = for_bills + agn_bills

    decision.split_credo = None
    for_credo = collect_credo(fors)
    agn_credo = collect_credo(agns)

    # The same above holds for split_credo
    if for_credo and agn_credo:
        decision.split_credo = for_credo + agn_credo

    update_MI_stances(decision)
    decision.no_update = None


def update_MI_stances(decision):
    """This function takes the decisions for and against the decision and checks
    which side is the stronger one. It checks this for stances from groups, the
    member making the decision, the bill that will be decided upon, and the
    normative stances on the issues from decision.for_norms and decision.agn_norms.

        Keyword arguments:
            decision -- the decision object to update.
        
        Postcondition:
            The MI_stances for the decision have been updated.
    """
    decision.MI_stance = MI_stances(decision)
    decision.MI_group  = MI_stances(decision, GROUP.name)
    decision.MI_credo  = MI_stances(decision, MEMBER.name)
    decision.MI_record = MI_stances(decision, BILL.name)
    decision.MI_norm   = compare_stances(decision.for_norms, decision.agn_norms)


def MI_stances(decision, db_source=None):
    """Updates a specific MI_stance such as that for the group, member, bill,
    or for all stances. It take the for and agn stances for the decision, filters
    them by the appropriate database, and then calls compare_stances to determine
    which side is strongest.

        Keyword arguments:
            decision  -- the decision object to update
            db_source -- the name of the database; will be used to filter stances
                         so that they only come from that db. 
        
        Returns:
            A list showing the side that is stronger. It is of the form:
            
            [[FOR|AGN], List_Of_Compelling_Stances_From_Winning_Side]
    """
    fors = decision.for_stances
    agns = decision.agn_stances

    if db_source:
        fors = collect_source_type(db_source, fors)
        agns = collect_source_type(db_source, agns)
    return compare_stances(fors, agns)


def collect_groups(stances):
    """Filters the given list of stances to contain only those that were derived
    from a group.
    
        Keyword arguments:
            stances -- the list of stances to filter.
        
        Returns:
            The filtered list.
    """
    return collect_source_type(GROUP.name, stances)


def collect_credo(stances):
    """Filters the given list of stances to contain only those that were derived
    from a member.
    
        Keyword arguments:
            stances -- the list of stances to filter.
        
        Returns:
            The filtered list.
    """
    return collect_source_type(MEMBER.name, stances)


def collect_bills(stances):
    """Filters the given list of stances to contain only those that were derived
    from a bill.
    
        Keyword arguments:
            stances -- the list of stances to filter.
        
        Returns:
            The filtered list.
    """
    return collect_source_type(BILL.name, stances)


def collect_source_type(db, stances):
    """Filters a given list of stances based on the database they are derived
    from.
    
        Keyword arguments:
            db      -- the source database to match
            stances -- the list of stances to filter.
        
        Returns:
            The filtered list.
    """
    filter_fun = lambda stance : stance.source_db == db
    return filter(filter_fun, stances)


def check_norms(stances):
    """Filters a given list of stances to contain only those that are normative.
    In other words, only those stances that are generally held by the public
    wll be kept.
    
        Keyword arguments:
            stances -- the list of stances to filter.
        
        Returns:
            The filtered list with duplicates removed.
    """
    filter_fun = lambda stance: normative_stance(stance)
    norms = filter(filter_fun, stances)
    return remove_duplicates(norms) if norms else []
        

def compare_stances(fors, agns):
    """This functions compares the stances to see which side has the more
    compelling reasons. It does so by checking which side has the largest number
    of most important stances supporting it.
    
        Keyword arguments:
            fors -- the list of stances supporting the bill to decide on
            agns -- the list of stances against the bill to decide on
                    
        Returns:
            A list containing the strongest arguments for or against the bill.
            Returns an empty list if both sides are equally compelling.

        Note on aglorithm:
            Both lists are first sorted by importance. Then, it goes through and
            compares each stance.
            
            If one list runs out before the other, the longest list is considered
            to have the most compelling stances.
            
            If one list is found to have a stance of stronger importance than
            the other on a give iteration of the for loop, that side is
            considered to be the most important and is chosen.
        
        Notes to consider:
            
            Consider how to handle this when the sort key is based on EQUITY
            or LOYALTY. Stances are not sorted by strict stance importance, but
            are sorted properly based on those definitions. Hence, it could be
            that there are some "A" stances later on but that aren't considered
            as valuable based on the current support.
            
            This might also change how remove_less_important works. However,
            just keep this simplified version for now.
    """
    fors.sort(key=lambda stance: stance.get_sort_key())
    agns.sort(key=lambda stance: stance.get_sort_key())

    for a_for, an_agn in map(None, fors, agns):
        if not a_for and not an_agn:
            return None
        elif not a_for:
            return [AGN, remove_less_important(agns)]
        elif not an_agn:
            return [FOR, remove_less_important(fors)]
        elif greater_than_importance(a_for.importance, an_agn.importance):
            return [FOR, remove_less_important(fors)]
        elif less_than_importance(a_for.importance, an_agn.importance):
            return [AGN, remove_less_important(agns)]
        else:
            continue
    return []

def remove_less_important(stances):
    """Removes all stances that are not as important as the first stance in the
    list.

        Keyword arguments:
            stances -- the stances to purge
                    
        Returns:
            The purged stances list that contains all stances that are greater
            than or equal to importance of the first stance in the original
            list.
              
       Precondition:
            The first item in the stance is the most important. Preferably, the
            list is sorted.
    """
    filter_fun = lambda stance : greater_than_or_equal_importance(stance.importance, stances[0].importance)
    return filter(filter_fun, stances)


def normative_stance(stance):
    """Checks if a given stance is the normative stance on the issue (aka the
    way most people in the country feel about the issue).
    
       Keyword arguments:
           stance -- the stance to check
        
       Returns:
           True if the stance is normative, false otherwise.
    """
    query = {"$or": [{"name": stance.issue}, 
                     {"synonyms": { "$in" : [ stance.issue ] }}
                    ]
            }
    stance_issue = get(ISSUE, query)
    if stance_issue and stance_issue.norm:
        return stance.match(stance_issue.norm)
    return False
