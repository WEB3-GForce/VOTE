# sourced from pol/protocol.lisp
#
# Copyright 2015 krishpop <krishnan1994@gmail.com>
#
# Distributed under terms of the MIT license.

from utils import *

def protocol_popular(decision):
    result = decision.result
    reasons = decision.reason
    print "All stances are {0} this bill:".format(result), "\n"
    #pretty_print(reasons)
    print reasons
    print "There are no reasons to vote {0} this bill.".format(opposite_result(result))


def protocol_non_partisan(decision):
    credo = decision.mi_credo
    credo_side = credo[0]
    credo_stance_list = credo[1:]
    opposing_groups = decision.group_agn if credo_side == "for" else decision.group_for
    party = "republicans" if decision.member == "rep" else "democrats"
    party_stance = filter(lambda stance: party == stance.source, opposing_groups)
    print "The member's party {0} has a stance {1} this bill:".format(party, opposite_result(credo_side))
    pretty_print(party_stance)
    print "While the member has a strong personal stance {0} the bill:".format(credo_side)
    pretty_print(credo_stance_list)


def protocol_not_constitutional(decision):
    protocol_simple_consensus(decision)
    print "There are constitutional grounds for opposing this bill:"
    pretty_print(filter(lambda stance: stance.reveal_issue == get_node("constitution", issue), decision.agn_stances))


def protocol_unimportant_bill(decision):
    protocol_simple_consensus(decision)
    print "And this bill has a low level of importance {0}".format(decision.bill.importance)


def protocol_inconsistent_constituency(decision):
    protocol_simple_consensus(decision)
    groups = decision.split_group
    print "The same group {0} has stances on both sides of this bill: {1:>15}".format(len(groups), groups)


def protocol_balance_the_books(decision):
    protocol_simple_majority(decision)
    print "The record supports positions on both sides of the bill: {0:>15}".format("FOR:")
    pretty_print(collect_bills(decision.for_stances))

    print "{0:>15}".format("AGN:")
    pretty_print(collect_bills(decision.agn_stances))


def protocol_best_for_the_country(decision):
    protocol_simple_consensus(decision)
    result = decision.result
    country = get_node("country", group)
    decision_group = decision.group_for if result == "for" else decision.group_agn
    country_stance = filter(lambda st: country == st.reveal_source, decision_group)

    print "The country as a whole has a stance {0} this bill:".format(result)
    pretty_print(country_stance)


def protocol_minimizing_adverse_effects(decision):
    protocol_simple_majority(decision)
    result = decision.result
    mi_for = sort(decision.for_stances)[0]
    mi_agn = sort(decision.agn_stances)[0]
    print "The high priority {0} stance is more important than the high priority {1} stance".format(result, opposite_result(result))
    print "{0:15>}".format(result)
    print_mi = mi_for if result == "for" else mi_agn
    pretty_print(print_mi)
    print "{0: 15>}".format(opposite_result(result))
    print_mi = mi_for if result == "agn" else mi_agn
    pretty_print(print_mi)


def protocol_not_good_enough(decision):
    protocol_simple_majority(decision)
    print """Even though the majority opinion favors this bill, the bill is too weak. \
    The importance of the agenda stances is greater than the bill stances.\
    Therefore, decide to vote against the bill in protest."""

    mi_up_stance = sort(decision.for_stances)[0]
    bill_up_stance = sort(decision.bill.stance_for)[0]
    print "{0:<15}Strong agenda stance: ".format(mi_up_stance)
    print "{0:<15}Weak bill stance: ".format(bill_up_stance)


def protocol_partisan(decision):
    protocol_simple_majority(decision)
    result = decision.result
    pro_stances = decision.for_stances if results == "for" else decision.agn_stances
    con_rel_stances = decision.con_rel_agn_stances if results == "for" else decision.con_rel_for_stances
    print "Voting {0} this bill also thwarts the opposition, for whom this bill is of greater importance:{1:>15}: ".format(result, "Our side")
    pretty_print(pro_stances)
    print "Their side:"
    prett_print(con_rel_stances)


def protocol_shifting_alliances(decision):
    result = decision.result
    fors = filter(lambda item: stance_relation_alikev(item, decision.group_agn), decision.group_for)
    agns = filter(lambda item: stance_relation_alikev(item, decision.group_for), decision.group_agn)
    print "There is no credo stance involved in this vote. There are groups on either side of this bill:{0:>15}".format("FOR:")
    prett_print(fors)
    print "{0:>15}".format("AGN:")
    pretty_print(agns)
    print "The member has belief conflicts with the {0} group (noted above), so the decision is with the {1} group.".format(opposite-result(result), result)


def protocol_simple_consensus(decision):
    result = decision.result
    print "Found a consensus {0} this bill".format(result)
    print "The most important stances are all {0} this bill:".format(result)
    pairs = [[decision.MI_group, "Group"], [decision.MI_credo, "Credo"], [decision.MI_record, "Record"], [decision.MI_norm, "Norm"]]
    for pair in pairs:
        slot = pair[0]
        string = pair[1]
        if slot:
            print "{0:<20}".format(string)
            #pretty_print(slot)
            print slot


def protocol_normative(decision):
    for_norms = decision.for_bnorms
    agn_norms = decision.agn_bnorms
    result = decision.result
    print "Public opinion norms are all {0} this bill:".format(result)
    pretty_print(for_norms if result == "for" else agn_norms)
    print "There are no norms {0} this bill".format(opposite_result(result))


def protocol_simple_majority(decision):
    result = decision.result
    print "Found a simple majority {0} this bill.".format(result)
    print_majority_stances(decision, result)
    print_majority_stances(decision, opposite_result(result))


def print_majority_stances(decision, result):
    stances = decision.for_stances if result == "FOR" else decision.agn_stances
    count = len(stances)
    print "There {0} {1} {2} stance{3}: {3:>28}".format("are" if count > 1 or count == 0 else "is", count, result, "s" if count > 1 or count == 0 else "", count)
    #pretty_print(stances)
    print stances


def protocol_no_decision(decision):
    print "VOTE has failed to arrive at a decision"
