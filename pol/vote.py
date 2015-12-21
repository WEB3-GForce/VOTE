from constants import *
from database import *
from decision import *
from member_stats import *
from utils import remove_duplicates

from member import Member


def vote(member_lname, bill_number):
    """Predicts how the specified member will vote on the given bill. This
    function is the standard way of calling VOTE from the commandline. It relies
    on a helper that takes actual DB objects.

    Keyword arguments:
        member_lname -- the last name of the member
        bill_number  -- the number of the bill
    
    Returns:
        A decision object containing the results of the decision.
    """
    member = get(MEMBER, {"lname" : member_lname.upper()})
    bill   = get(BILL, {"bnumber" : bill_number.upper()})

    if not member:
        print "Member not found in DB: %s" % member_lname
        return None
    if not bill:
        print "Bill not found in DB: %s" % bill_number
        return None

    return vote_helper(member, bill)


def vote_helper(member, bill):
    """A helper to vote, predicts how the specified member will vote on the
    given bill.

    Keyword arguments:
        member -- a Member object corresponding on the member who will vete
        bill   -- a Bill object of the bill to be voted on.
    
    Returns:
        A decision object containing the results of the decision.
    """
    
    decision = Decision()
    initialize_decision(decision, member, bill)
    return "DONE"

    update_decision_metrics(vote_decision)

    apply_decision_strategies(vote_decision)

    compare_with_real_vote(vote_decision)

    update_decision_dbase(vote_decision)

    if vote_decision.strategy:
       print vote_decision
    else:
        print "No decision"

    return vote_decision


def initialize_decision(decision, member, bill):
    """Initializes a decision object with basic info about the member and bill.
       Extracts stances for the member based on the bill and the member's
       relations.

       Keyword arguments:
            decision -- the decision object to initialize
            member   -- a Member object corresponding to the member who will vote
            bill     -- a Bill object of the bill to be voted on.
    
        Postcondition:
            The decision object has been updated.
    """

    print "Initializing Decision..."

    if not member.stances:
        extract_voting_stances(member)

    decision.member = member._id
    decision.bill   = bill._id

    infer_member_rel_stances(member)

    print "Analyzing alternative positions..."

    decision.for_stances = match_stances_for(member, bill)
    decision.agn_stances = match_stances_agn(member, bill)

    print "Initialization complete."
    print member
    print bill
    print decision


def infer_member_rel_stances(member):
    """Infers the stances that a member might have based on relationships with
       others.

       Keyword arguments:
            member   -- the member whose stances will be inferred
    
        Postcondition:
            The member's stances have been updated to include those from
            relationships.
    """
    if not member.pro_rel_stances:
        print "Inferring stances from relations of %s" % member.name
        get_relations_stances(member)
        print "Inferring stances from relations completed."


def match_stances_for(member, bill):
    """This function filters member stances by stances that are implied by
    voting for the bill.

       Keyword arguments:
            member   -- the member whose stances will be filtered
            bill     -- the bill whose stances will be used to filter the member
                        stances.
    
       Return:
            A list that contains only those member stances that would be implied
            by voting for the bill.
            
       Notes: 
            In other words, this function checks to see if the member has any
            reasons to vote for the bill.
    """
    print "Considering implications of voting FOR on bill %s" % bill.bnumber
    print "Matching member stances with bill stances."
    stances = match_stances(bill.stance_for, member)
    stances = match_stances_sort(member, bill, stances)
    print "Considering FOR implications completed."
    return stances


def match_stances_agn(member, bill):
    """This function filters member stances by stances that are implied by
    voting against the bill.

       Keyword arguments:
            member   -- the member whose stances will be filtered
            bill     -- the bill whose stances will be used to filter the member
                        stances.
    
       Return:
            A list that contains only those member stances that would be implied
            by voting against the bill.
            
       Notes: 
            In other words, this function checks to see if the member has any
            reasons to vote against the bill.
    """
    print "Considering implications of voting AGN on bill %s" % bill.bnumber
    print "Matching member stances with bill stances."
    stances = match_stances(bill.stance_agn, member)
    stances = match_stances_sort(member, bill, stances)
    print "Considering AGN implications completed."
    return stances


def match_stances_sort(member, bill, stances):
    """This is a helper function for the two functions above. It sorts the
    matched stances list and removes old voting data if necessary.

       Keyword arguments:
            member   -- the member whose stances were filtered
            bill     -- the bill whose stances were used to filter the member
                        stances.
            stances  -- the filtered stances
    
       Return:
            A sorted list with the old votes removed
    """
    sort_key = member.stance_sort_key or EQUITY
    print "Sorting stances based on %s order." % sort_key

    for stance in stances:
        stance.set_sort_key(sort_key)

    stances = remove_old_votes(stances, bill)
    stances.sort(key=lambda stance: stance.get_sort_key)
    return stances


def is_bill_source(stance, bill):
    """Used as a filter function, determines if a stance's source is a given bill.

       Keyword arguments:
            stance   -- the stance to check the source of
            bill     -- the potential source of the stance.
    
        Postcondition:
            Whether the bill is the stance's source. Since bills can be referenced
            by a synonym, name, bill number, or Mongo id, all are checked.
    """   
    return (stance.source == bill._id or stance.source == bill.name or
            stance.source == bill.bnumber or stance in bill.synonyms)


def remove_old_votes(stances, bill):
    """Filters stances to contain only stances that come from the bill.

       Keyword arguments:
            stances   -- the list of stances to purge
            bill      -- the bill whose stances will be kept
    
        Return:
            The newly filtered stances list. If the flag no_old_votes is set,
            then the stances will be filtered so that only stances from the bill
            itself are used. If it is not set, all stances are used.
    """   
    if no_old_votes:
        filter_fun = lambda stance : is_bill_source(stance, bill)
        stances = filter(filter_fun, stances)
    return stances


# This flag is used in remove_old_votes. This is used to determine whether the
# function should filter stances such that only stances that originate from the
# bill are kept.
no_old_votes = True


def no_old_votes(flag):
    """ Sets the no_old_votes flag."""
    global no_old_votes
    no_old_votes = flag


def match_stances(stances, member):
    """Filters the member's stances keeping only those that match a stance in
       stances. The member's stances consist of personal stances (member.credo),
       voting record stances (member.stances), and group stances
       (member.pro_rel_stances)
    
       Keyword arguments:
            stances   -- the list of stances to filter the member stances by
            member    -- the member whose stances will be filtered.
    
        Return:
            A list of all member stances found in stances. The list has
            duplicates removed.
    """
    matches = []
    member_stances = member.credo + member.stances + member.pro_rel_stances
    for stance in stances:
        filter_fun = lambda member_stance : stance.match(member_stance)
        matches += filter(filter_fun, member_stances)
    return remove_duplicates(matches)


"""
    Apply decision strategies
"""


def apply_decision_strategies(decision):

   print "Applying Decision Strategies"
   strategies = DB[ALL_STRATEGIES]
   apply_strats(decision, strategies)


def apply_strats(decision, strategies):

    for strategy in strategies:

        strategy_code = strategy.test_code

        print "Trying decision strategy: %s" % strategy.name

        if strategy_code(decision, strategy):

            print "Success"

            decision.reason = group_reasons(decision.reason)
            decision.downside = group_reasons(decision.reason)
            return decision

        else:
             print "%s Failed" % strategy


"""
    Group reasons:
    Take the list of stances and group together the stances on the same issue
"""

def group_reasons(stance_list):
    if stance_list == None:
        return None
    else:
        return sort(stance_list)


"""
    Batch processing and analysis:

    There are three ways of invoking VOTE-ALL

    vote-all() : process all members on all bills
    vote-all(member_name = name) : process all bills for given member
    vote-all(bill_name = bill) : process all members for given bill
"""

def vote_all(member_name = None, bill_name = None):
    if member_name:
        member_ids = [DBMembers.getEntryByName(member).id]
    else:
        member_ids = [member.id for member in DBMember.GetAll()]

    if bill_name:
        bill_ids = [bill.id for bill in DBBill.getEntryByName(bill_name)]
    else:
        bill_ids = [bill.id for bill in DBBill.GetAll()]
        
    for memberid in members:
        for billid in bill_ids:
            vote(memberid, billid)
