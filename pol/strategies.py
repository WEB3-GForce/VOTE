import operator
import pol.database as db
from pol.decision import *

"""
      As of 9/25/90

      0   Popular decision                        [A]  @@@(POPULAR)
      1   Inconsistent constituency               [B]  @@@(INCONSISTENT-CONSTITUENCY)
      2   Non-partisan decision                   [B]  @@@(NON-PARTISAN)
      3   Not constitutional                      [B]  @@@(NOT-CONSTITUTIONAL)
      4   Unimportant Bill                        [B]  @@@(UNIMPORTANT-BILL)
      5   Balance the books                       [C]  @@@(BALANCE-THE-BOOKS)
      6   Best for the country                    [C]  @@@(BEST-FOR-THE-COUNTRY)
      7   Minimize adverse effects                [C]  @@@(MINIMIZE-ADVERSE-EFFECTS)
      8   Not good enough                         [C]  @@@(NOT-GOOD-ENOUGH)
      9   Partisan Decision                       [C]  @@@(PARTISAN)
      10  Shifting alliances                      [C]  @@@(SHIFTING-ALLIANCES)
      11  Simple consensus                        [C]  @@@(SIMPLE-CONSENSUS)
      12  Normative decision                      [D]  @@@(NORMATIVE)
      13  Simple Majority                         [D]  @@@(SIMPLE-MAJORITY MAJORITY)
  *   14  Deeper analysis                         [E]  @  (DEEPER-ANALYSIS)
      15  No decision                             [F]  @ @(NO-DECISION)
      16  Change of heart                         [X]  @@@(CHANGE-OF-HEART)
      17  Innoculation                            [X]  @@@(INNOCULATION)
      18  It couldn't pass                        [X]  @@@(IT-COULD-NOT-PASS)
      19  Mixed constituency                      [X]   @@(MIXED-CONSTITUENCY)
      20  Unpopular decision                      [X]   @@(UNPOPULAR)

"""

def flatten(a_list):
    return [item for sublist in a_list for item in sublist]

# ------------------------------------------------------------------
#  firm-decision  sets final outcome of decision structure
# ------------------------------------------------------------------

# TODO: check collect_bills correctly defined
def firm_decision(decision, side, reasons, old_downside, strat):
    bill = db.get(db.BILL, {"_id": decision.bill})
    filter_fin = lambda stance : stance.source == bill.id
    downside = filter(filter_fun, flatten(old_downside))
    record = collect_bills(downside)

    decision.result = side
    decision.reason = reasons
    decision.strategy = strat

    if record:
        decision.downside_record = record
        decision.downside = remove_intersection(downside, record, operator.eq)

    else:
        decision.downside = downside

    return decision

# TODO
def set_decision_outcome(decision, result, strat):
    if result == "FOR":
        reason = decision.for_stances
        dowside = decision.agn_stances
    elif result == "AGN":
        reason = decision.agn_stances
        downside = decision.for_stances
    else:
        print "Reason expected to be FOR or AGN. Got: %s" % reason
        return

    return firm_dicision(decision, result, reason, downside, strat)

"""
==================================================================
      0   Popular decision                        [A] @(POPULAR)

  Remarks:       Vote is consistent with major constituencies.
  Quote:         I just try to vote my district.
                 I was sent to Washington to represent the way people back home feel.
                 This is what the vast majority want.
                 I owe it to my constiuents if they feel that strongly about it. [Delegate stance]
  Rank:          "A"
  Test:          All stances on one side of bill.
  Test-code:     STRAT-POPULAR
  Example:       (VOTE 'BRUCE 'PLANT-CLOSING)
==================================================================
"""

def strat_popular(decision, strat):
    for_stances = decision.for_stances
    agn_stances = decision.agn_stances

    if not for_stances and agn_stances:
        return firm_decision(decision, "AGN", agn_stances, [], strat)
    elif not agn_stances and for_stances:
        return firm_decision(decision, "FOR", for_stances, [], strat)
    else:
        return None


"""
==================================================================
      1   Inconsistent constituency               [B] @(INCONSISTENT-CONSTITUENCY)
    Same group on both sides of issue
==================================================================
"""

def strat_inconsistent_constituency(decision, strat):
    source_conflicts = decision.split_group
    result = consensus(decision)

    if not source_conflicts:
        return None
    elif result:
        return set_decision_outcome(decision, result, strat)
    else:
        return None

def majority(decision):
    fors = decision.number_for if decision.number_for else len(decision.stance_for)
    agns = decision.number_agn if decision.number_agn else len(decision.stance_agn)

    if fors > agns:
        return "FOR"
    elif agns > fors:
        return "AGN"
    else:
        return None

def consensus(decision):
    filter_fun = lambda lst : lst[0]
    MI = map(filter_fun, collect_MI(decision))

    if len(remove_duplicates(MI)) == 1 :
        return MI[0]
    else:
        return None

def collect_MI(decision):
    result = [decision.MI_stance, decision.MI_group, decision.MI_credo, decision.MI_record, decision.MI_norm]

    filter_fun = lambda x : x != []
    return filter(filter_fun, result)


"""
==================================================================
      2   Non-partisan decision                   [B]  (NON-PARTISAN)

  Remarks:       Vote of conscience or credo that violates party line.  Not a district vote.
  Quote:         Sometimes party loyalty demands too much. (JFK)
  Rank:          "B"
  Test:          Major conflict between credo and party stances.
==================================================================
"""
#  The vote is a matter of conscience.
#  The credo position is in conflict with a party position.
#  The credo position is very important.

def strat_non_partisan(decision, strat):
    member = DBMember.getById(decision.member)

    credo = decision.MI_credo
    credo_side = credo[0]
    credo_stance_list = credo[1]
    opposing_groups = decision.group_agn if credo_side == "FOR" else decision.group_for

    party = "Unknown Party Affiliation"
    if member.party == "REP":
        party = "REPUBLICANS"
    if member.party == "DEM":
        party = "Democrats"

    # Translate the following and add it to the if statement
    # below:

    # (member party (mapcar #'stance-source opposing-groups)
    #any(party == group.stance for group)

    credo_stance1 = DBStance.getById(credo_stance_list[0])

    if (credo and opposing_groups and credo_stance_list and
        most_important?(credo_stance1.importance):
        return set_decision_outcome(decision, credo_side, strat)
    else:
        return None

"""
==================================================================
      3   Not constitutional                      [B]  (NOT-CONSTITUTIONAL)

  Remarks:       Vote against a measure that would be struck down by
                 the Supreme Court.
  Rank:          "B"
==================================================================
"""

def strat_not_constitutional(decision, strat):
    constitution_issue = DBIssue.getByName("CONSTITUTION")
    filter_fun = lambda stance : DBStance.getById(stance).issue == constitution_issue

    result = consensus(decision)

    if result == "AGN" and filter(filter_fun, decision.agn_stances):

        reason = decision.agn_stances
        downside = decision.for_stances
        return firm_decision(decision, result, reason, downside, strat)

    else:
        return None

"""
==================================================================
      4   Unimportant Bill                        [B]   (UNIMPORTANT-BILL)

  Date-open:     Monday, May 22, 1989
  Symbol:        STRATEGY.681
  Name:          "Unimportant Bill"
  Sort-key:      "BUnimportant Bill"
  Synonyms:      (UNIMPORTANT-BILL)
  Isa-depth:     ""
  Remarks:       Not much riding on this bill.

  Quote:         [Morrison:] some things that are close calls are not treated
                 as close calls because they're not important enough.  I mean
                 its very different if there's enough riding -- either substantively
                 or politically -- on a vote.  You might have exactly the same
                 tensions among the various priorities if you were to pull
                 this up, but it might be about how you spend $100,000 and you
                 say, **** this.

  Rank:          "B"
  Test:          Importance of bill is minimal.
==================================================================
"""

def strat_unimportant_bill(decision, strat):
    result = consensus(decision)
    importance = DBBill.GetById(decision.bill).importance

    if result and importance == "C":
        return set_decision_outcome(decision, result, strat)
    else:
        return None

"""
==================================================================
      5   Balance the books                       [C]  (BALANCE-THE-BOOKS)

  Remarks:       Offset current vote with past or future votes.
  Quote:         I know you are upset with this vote, but I have always been there in the
                   past, and I shall be there in the future.
                 I will make it up to you.
                 (point to specific past votes)
  Rank:          "C"
==================================================================
"""

def strat_balance_the_books(decision, strat):
    result = majority(decision)
    split  = decision.split_record
    if result and split:
        return set_decision_outcome(decision, result, strat)
    else:
        return None

"""
==================================================================
      6   Best for the country                    [C]  (BEST-FOR-THE-COUNTRY)

  Remarks:       Take the broad view, over parochial interests.
  Quote:         The needs of the country, in this case, must come first.
  Rank:          "C"
  Test:          National interest in conflict with local interest.
==================================================================
"""

# relies on a group: country which has the broad issue agenda for
#  the whole country.  Each congressman has a positive relation with COUNTRY.

def strat_best_for_country(decision, strat):
    result = consensus(decision)
    country = DBGroup.GetByName("COUNTRY")

    # Translate the following once you know more about group_for.
    # Is it a stance object or group object?

    #(country-for (collect (decision-group-for decision)
                              #'(lambda (st) (eq country (reveal-source st)))))
    country_for = None
    # (country-agn (collect (decision-group-agn decision)
                              #'(lambda (st) (eq country (reveal-source st)))))
    country_agn = None

    if result == "FOR" and country_for and not country_agn:
        return set_decision_outcome(decision, result, strat)
    elif result == "AGN" and country_agn and not country_for:
        return set_decision_outcome(decision, result, strat)
    else:
        return None

"""
==================================================================
      7   Change of heart                         [C]  (CHANGE-OF-HEART)

  Remarks:       Reverse a credo/vote position on the record to accomodate
                 conflict in constituencies.
  Quote:         A foolish consistency is the hobgoblin of small minds.
  Rank:          "C"
  Test:          Credo importance is less than conflicting relation importance.
==================================================================
"""

def strat_change_of_heart(decision, strat):
    result = majority(decision)
    split  = decision.split_credo
    if result and split:
        return set_decision_outcome(decision, result, strat)
    else:
        return None

"""
==================================================================
      8   Inoculation                            [C]  (INOCULATION)

  Remarks:       Decision which may prove to be unpopular later on.
                 Need to begin laying groundwork for defense early on.
  Rank:          "C"
  Test:          Low priority stances, pro or con.
==================================================================
"""

def strat_inoculation(decision, strat):
    result = majority(decision)
    split_groups = decision.group_for and decision.group_agn
    importance_level = None
    # SAME ISSUE AS ABOVE. Check whether group_for is stances
    # or groups. Otherwise, stance-importance not defined.
    if split_groups:
        temp = decision.group_for + decision.group_agn
        temp.sort(key=lambda stance: stance.sort_key)
        importance_level = temp[0].importance

     if result and split_groups and less_than_importance?(importance_level1, "B"):
        return set_decision_outcome(decision, result, strat)
     else:
        return None

"""
==================================================================
      9   It couldn't pass                        [C]  (IT-COULD-NOT-PASS)

  Remarks:       Do not waste a vote on a symbolic measure.  Better to
                 build credibility and a consensus for the future.
  Quote:         Why waste a vote on a measure that has so little chance of passing.
  Rank:          "C"
  Test:          Bill has far higher importance (and low likelihood of passage)
                 but for issue stance consistent (but stronger than) with my own.
                 This is the flip side of not-good-enough.
==================================================================
"""

def strat_could_not_pass(decision, strat)
    result = majority(decision)
    billid = decision.bill
    if result == "AGN" and could_not_pass?(billid):
        return set_decision_outcome(decision, result, strat)
    else:
        return None

def might_pass?(billid):
    tally = DBBill.GetById(billid).vote_tally

    if tally:
        return approved?(billid) or vote_ratio(billid) > 1

def could_not_pass?(billid):
    tally = DBBill.GetById(billid).vote_tally
    if tally:
        return vote_ratio(billid) < 1

def vote_ratio(billid):
    tally = DBBill.GetById(billid).vote_tally
    fors = tally[0]
    agns = tally[1]

    if type(fors) != type(0) and type(agns) != type(0):
        return None

    # Simply let the ratio be fors if agn is 0 to avoid divide
    # by 0.
    if agn == 0:
        return fors

    if fors and agns:
        return fors/agns

def approved?(bill):
    tally = DBBill.GetById(billid).vote_tally
    return tally[0] in ["PASSED", "ADOPTED", "APPROVED"]

def rejected?(bill):
    tally = DBBill.GetById(billid).vote_tally
    return tally[0] in ["REJECTED", "FAILED"]

"""
==================================================================
      10  Minimize adverse effects                [C]  (MINIMIZE-ADVERSE-EFFECTS)

  Remarks:       Adverse effects are less important than the benefits of the vote.
  Quote:         Nothing's perfect.  You have to break a few eggs to make
                 omelets.
  Rank:          "C"
  Test:          The downside results are lower in importance than the upside.
==================================================================
"""

def strat_minimize_adverse_effects(decision, strat):
    result = majority(decision)
    if result:
        MI_up_level = get_MI_level(decision, result)
        MI_down_level = get_MI_level(decision, oposite_result(result))
        if greater_than_importance?(MI_up_level, MI_down_level):
            return set_decision_outcome(decision, result, strat)

    return None

def get_MI_level(decision, result):
    stances = None
    if result == "FOR":
        stances = decision.for_stances
    if result == "AGN"
        stances = decision.agn_stances

    if stances:
        stances.sort(key=lambda stance: stance.sort_key)
        return stances[0].importance
     else:
        return "D"

"""
==================================================================
      11  Mixed constituency                      [C]  (MIXED-CONSTITUENCY)

  Remarks:       E.g., rural/urban. can justify pro-rural vote to urbans by
                 pointing to other constituency, and vice-versa.
  Rank:          "C"
  Test:          District must be divided and there should be symmetry on stances.
==================================================================
"""

# note - same as balance the books ...


"""
==================================================================
      12  Not good enough                         [C]  (NOT-GOOD-ENOUGH)

  Remarks:       Bill importance is less than my own stances would call for.
                 For example, personal stance of A, bill importance of C.
  Quote:         I would have voted for a stronger bill.
                 This measure is a fraud.  It has no teeth in it.
  Rank:          "C"
  Test:          Compare importance of bill stance with own stances.  Check for disparity.
==================================================================
"""

def strat_not_good_enough(decision, strat):

    result = majority(decision)
    MI_up_level = None
    MI_bill_level = None
    if result:
        MI_up_level = get_MI_level(decision, result)
        MI_bill_level = get-MI-bill-level(decision, result)

    if result == "FOR" and greater_than_importance?(MI_up_level, MI_bill_level):
        return set_decision_outcome(decision, "AGN", strat)
    else:
        return None

def get_MI_bill_level(decision, result):
    bill = DBBill.GetById(decision.bill)
    stances = None
    if result == "FOR":
        stances = bill.stance_for
    if result = "AGN":
        stances = bill.stance_agn

     if stances:
        stances.sort(key=lambda stance: stance.sort_key)
        return stances[0].importance
     else:
        # In Python, "A" > None, but we want A to be of
        # higher importance. Hence, we use an importance
        # of "Z" that will be lower than all others.
        return "Z"

"""
==================================================================
      13  Partisan Decision                       [C]  (PARTISAN)

  Remarks:       Counter-planning vote against the opposing interests.
  Quote:         I could not let those rich Republicans tear this country apart.
                 I am not going to let those Democrats have their special interests tell
                   me what to do.
  Rank:          "C"
  Test:          Voting to deny something wanted by opposition.
==================================================================
"""

def start_partisan(decision, strat):
    result = majority(decision)
    if result:
        MI_up_level = get_MI_level(decision, result)
        update_con_rel_stances(decision)
        MI_con_rel_level = get_MI_con_rel_level(decision, opposite_result(result))

        if MI_con_rel_level and less_than_importance?(MI_up_level , MI_con_rel_level):
            return set_decision_outcome(decision, result, strat)

    return None

def update_con_rel_stances(decision):
    decision.con_rel_for_stances = match_con_rel_stances_for_agn(decision, "FOR")

    decision.con_rel_agn_stances = match_con_rel_stances_for_agn(decision, "AGN")
    return "DONE"

def get_MI_con_rel_level(decision, result):
    stances = []
    if result == "FOR":
        stances = decision.con_rel_for_stances
    elif result == "AGN":
        stances = decision.con_rel_agn_stances

    if stances:
        stances.sort(key = lambda stance: stance.sort_key)
        return stances[0].importance

# match-con-rel-stances will check
# con group/relationship stances
#

def match_con_rel_stances(stance_id, mem_id):
    print stance_id
    stance = DBStance.GetById(stance_id)
    member = DBMember.GetById(mem_id)
    filter_fun = lambda mem_stance : mem_stance.match?(stance)
    matches = filter(filter_fun, member.con_rel_stances)

    filter_fun = lambda element : element != []
    return filter(filter_fun, matches)

def match_con_rel_stances_for_agn(decision, side):

    member = DBMember.GetById(decision.member)
    bill = DBBill.GetById(decision.bill)

    print "Vote %s %s" % (side, bill.bnumber)
    print "Considering counter-planning implications of %s %s" % (side, bill.bnumber)
    print "Matching member con-rel stances with bill stances:"

    bill_stance = bill.stance_for

    if side == "AGN":
        bill_stance = bill.stance_agn

    sort_key = member.stance_sort_key or "EQUITY"

    stances = []
    for stance in bill_stance:
        stances += match_con_rel_stances(stance, decision.member)

    print "Sorting stances based on %s order..." % sort_key

    for stance in stances:
        stance.set_sort_key(sort_key)

    stances.sort(key=lambda stance: stance.sort_key)
    print "Done."
    print "Stances %s" %side
    print stances


"""
==================================================================
      14  Shifting alliances                      [C]  (SHIFTING-ALLIANCES)

  Remarks:       Conflict resolution through changing relations.
                 When two constituencies are in conflict, try to see if one is more
                 valuable or compatible than the other.  If so, shift their relative
                 importance by either lowering one or raising the other.
  Quote:         I am voting with my good friends in ().  I am sorry to disappoint
                 my many supporters in ().  They know that I have fought many fights
                 with them.
  Rank:          "C"
  Test:          Two constituencies in conflict.
                 Identify other important issue in which they disagree which is
                 important to me.  Pick the one that sides with me.
==================================================================
"""

def strat_shifting_alliances(decision, strat):
    result = divided_groups(decision)
    if result:
        return set_decision_outcome(decision, result, strat)
    else:
        return None

"""
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
"""

def strat_simple_consensus(decision, strat):
    result = consensus(decision)
    if result:
        return set_decision_outcome(decision, result, strat)
    else:
        return None

"""
==================================================================
    *   16  Deeper analysis                         [D+]   (DEEPER-ANALYSIS)

  Status:        "Active"
  Date-open:     Sunday, February 11, 1990
  Symbol:        STRATEGY.323
  Name:          "Deeper analysis"
  Synonyms:      (DEEPER-ANALYSIS)
  Isa-depth:     ""
  Remarks:       Consider the symbolic implication of the for/agn stances of the bill.

  Rank:          "D+"
  Test:          Find a consensus after expanding the bill-stance through inference.
==================================================================
"""

def strat_deeper_analysis(decision, strat):
    level = decision.deeper_analysis

    if level is None:
        new_analysis_level(decision)
        reanalyze_decision(decision)
        filter_fun = lambda strategy : not strategy.no_second_try
        strategies = DBStrategy.GetAll()
        return apply_strats(decision, filter(filter_fun, strategies)
    else:
        return strat_deeper_analysis2(decision, strat)

def strat_deeper_analysis2(decision, strat):
    level = new_analysis_level(decision)
    billid = decision.bill
    bill = DBBill.GetById(billid)
    old_bill_for_stances = bill.stance_for
    old_bill_agn_stances = bill.stance_agn

    filter_fun = lambda strategy : not strategy.no_second_try
    strategies = filter(filter_fun, DBStrategy.GetAll())

    new_bill_for_stance  = expand_stances(old_bill_for_stances, level)
    new_bill_agn_stances = expand_stances(old_bill_agn_stances, level)

    temp_for = remove_intersection(new_bill_for_stances, new_bill_agn_stances, stance_equal?)

    temp_agn = remove_intersection(new_bill_agn_stances, new_bill_for_stances, stance_equal?)

    new_bill_for_stance  = temp_for
    new_bill_agn_stances = temp_agn

    if level == "D":
        return None
    elif (len(new_bill_for_stances) > len(old_bill_for_stances) or
         len(new_bill_agn_stances) > len(old_bill_agn_stances)):
         print "Deeper Analysis results in new bill stances at level %s..." % level

         print_new_stances(new_bill_for_stances, old_bill_for_stances, "FOR")

         print_new_stances(new_bill_agn_stances, old_bill_agn_stances, "AGN")

         bill.stance_for = new_bill_for_stances
         bill.stance_agn = new_bill_agn_stances

         reanalyze_decision(decision)

         result = apply_strats(decision, strats)
         bill.stance_for = old_bill_for_stances
         bill.stance_agn = old_bill_agn_stances
         return result
    else:
        print "No Change at this level. Trying deeper Deeper Analysis"
        return strat_deeper_analysis(decision, strat)

def reanalyze_decision(decision):
    print "Re-Analyzing alternative positions"

    decision.for_stances = match_stances_for_agn(decision, "FOR")
    decision.agn_stances = match_stances_for_agn(decision, "AGN")
    decision.update_decision_metrics()

def new_analysis_level(decision):
    old_level = decision.deeper_analysis
    new_level = next_analysis_level(old_level)
    decision.deeper_analysis = new_level
    return new_level

def next_analysis_level(level):
    next_hash = {"X" : "A", "A": "B", "B":"C", "C":"D"}
    if not next_hash.has_key(level.upper()):
        return "X"
    return next_hash[level]

#  expand-stances infers as much as possible from a list of stances
#  with importance greater than or equal to given level
#------------------------------------------------------------------

def expand_stances(stance_list, level):
    new_stances = []
    for stance in stance_list:
        new_stances += expand_one_stance(stance, level)

    new_stances = stance_list + new_stances

    remove_duplicates(new_stances)


#  Expand the stances that are of importance greater than or equal
#  to the given level of importance.

def expand_one_stance(stance, level):
    side = stance.side
    issue = DBIssue.GetById(stance.issue)

    new_stances = []
    if side == "PRO":
        new_stances = issue.pro_stances
    elif side == "CON":
        new_stances = issue.con_stances

    filter_fun = lambda stance : greater_than_or_equal_importance?(stance.importance, level)
    return filter(filter_fun, new_stances)


def set_filter(set1, set2):
    filter_fun = lambda element : element in set2
    return filter(filter_fun, set1)

def strat_simple_majority(decision, strat):
    result = majority(decision)

    if result:
        return set_decision_outcome(decision, result, strat)
    else:
        return None

def print_new_stances(new, old, side):
    if len(new) > len(old):
        print "New %s stances resulting from deeper analysis: " % side

        for stance in remove_intersection(new, old, stance_equal?):
            print stance


"""
==================================================================
      17  Normative decision                      [D] @(NORMATIVE)

  Remarks:       Decision reflects normative opinion on relevant issues.
  Rank:          "D"
  Test:          Bill stances match normative stances for given issues.
  Test-code:     STRAT-NORMATIVE
==================================================================
"""

def strat_normative(decision, strat):
    for_norms = decision.for_bnorms
    agn_norms = decision.agn_bnorms

    if not for_norms and agn_norms:
        return firm_decision(decision, "AGN", agn_norms, [], strat)
    elif for_norms and not agn_norms:
        return firm_decision(decision, "FOR", for_norms, [], strat)
    else:
        return None

"""
==================================================================
      18  Unpopular decision                      [D]  (UNPOPULAR)

  Remarks:       Recognizes that vote will not play well with many constituents.
  Quote:         I know people will criticize me for this vote, but I had to do it.
                 I couldn't live with myself if I didn't.
                 I have to use my judgment.  You can express an opinion.  I have to make a decision. [Trustee]
                 I stand by my record.  I'm not going to change my principles.
                 I hope you appreciate that and will look at my record as a whole.
  Rank:          "D"
  Test:          Major conflicts among stances.
==================================================================
"""

"""
==================================================================
      19  No decision                             [E] @(NO-DECISION)
  Test-code:   STRAT-NO-DECISION
  Remarks:     No previous decision was triggered.
  Test:        Always true.
==================================================================
"""

def strat_no_decision(decision, strat):
    firm_decision(decision, None, [], [], strat)
