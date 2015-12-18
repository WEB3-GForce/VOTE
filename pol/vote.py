from constants import *
from database import *
from decision import *
from member_stats import *

from member import Member


def vote(member_lname, bill_name):
    """Predicts how the specified member will vote on the given bill. This
    function is the standard way of calling VOTE from the commandline. It relies
    on a helper that takes actual DB objects.

    Keyword arguments:
        member_lname -- the last name of the member
        bill_name    -- the name of the bill
    
    Returns:
        A decision object containing the results of the decision.
    """
    member = get(MEMBER, {"lname" : member_lname.upper()})
    bill   = get(BILL, {"name" : bill_name.upper()})
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

    print "Initializing Decision..."

    if not member.stances:
        extract_voting_stances(member)

    decision.member = member._id
    decision.bill   = bill._id

    infer_rel_stances(decision)

    print "Analyzing alternative positions..."

    decision.for_stances = match_stances_for_agn(decision, "FOR")
    decision.agn_stances = match_stances_for_agn(decision, "AGN")

    print "Initialization complete."
    print Decision
    print member
    print bill

"""
    Infer Stances from relations
"""

def infer_rel_stances(decision):
    infer_member_rel_stances(decision.member)


def infer_member_rel_stances(mem_id):
    member = db(mem_id)
    if member.pro_rel_stances is None:
        print "Inferring Stances from relations of %s" % member.name
        member.get_relations_stances()
        print "Done"

"""
    Next-level
"""


def match_stances_for_agn(decision, side):

    print "Considering implications of vote %s on bill %s" % (side, decision.bill)

    sort_key = DB[decision.member].stance_sort_key

    if side == FOR:
        stances = match-stances(DB[decision.bill].for_stances, decision.member)

    else:
        stances = match-stances(DB[decision.bill].agn_stances, decision.member)

    print "Sorting stances based on %s order" % sort_key

    remove_old_votes(stances, decision.bill)
    stances.sort_key = sort_key

    print "Done"

def remove_old_votes(stances, bill_id):
    if not no_old_votes:
        stances = filter(lambda(st): st.reveal_source.id == bill_id, stances)
    return stances


def no_old_votes(flag):
    global no_old_votes
    no_old_votes = flag

"""
    match_stances will check personal stances, voting record stances,
    group
"""
def match_stances(stance_id, mem_id):
    print stance_id
    matches = map((lambda mem_stances: stance_id == mem_stance), [mem_id.credo + mem_id.stances + mem_id.pro_rel_stances])

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
