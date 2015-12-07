import decision
from decision import Decision

def vote(member_id, bill_id):
    vote_decision = Decision()

    initialize_decision(vote_decision, member_id bill_id)

    update_decision_metrics(vote_decision)

    apply_decision_strategies(vote_decision)

    compare_with_real_vote(vote_decision)

    update_decision_dbase(vote_decision)

    if vote_decision.strategy:
       print vote_decision
    else:
        print "No decision"

    return vote_decision


def initialize_decision(decision, member_id, bill_id):

    decision.member = member_id
    decision.bill    = bill_id

    print Decision

    rel_stances(decision)

    print "Analyzing alternative positions"

    decision.for_stances = match_stances_for_agn(decision, FOR)

    decision.agn_stances = match_stances_for_agn(decision, AGN)

"""
    Infer Stances from relations
"""

def infer_rel_stances(decision):
    mem_id = decision.member
    infer_member_rel_stances(mem_id)


def infer_member_rel_stances(mem_id):
    member = db(mem_id)
    if member.pro_rel_stances == None:

"""
    Next-level
"""


def match_stances_for_agn(decision, side):

    print "Considering implications of vote %s on bill %s" % (side, decision.bill)

    sort_key = DB[decision.member].stance_sort_key

    if side = FOR:
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
    global no_old_votes = flag

"""
    match_stances will check personal stances, voting record stances,
    group
"""
def match_stances(stance_id, mem_id):
    print stance_id
    matches = map((lambda mem_stances: stance_id == mem_stance), mem_id.credo + mem_id.stances + mem_id.pro_rel_stances])

"""
    Apply decision strategies
"""


def apply_decision_strategies(decision):

   print "Applying Decision Strategies"
   strategies = DB[ALL_STRATEGIES]
   apply_strats(decision, strategies)


def apply_strats(decision, strategies)

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
        # return all bills for member to database
    elif bill_name:
        # return all members for given bill to database
    else:
        # return all members on all bills to database
