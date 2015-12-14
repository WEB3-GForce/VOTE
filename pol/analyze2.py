"""
    Like VOTE-ALL, ANALYZE-SCORES has optional arguments

    Prints out statistics about decision dbase.
    (analyze-decisions 'deep) uses only deep-analysis decisions

    Arguments:

        members = A list of the names of teh members of congress
        whose decisions will be analyzed. If the empty list is
        given, it will analyze all members.

"""
BILL_TOTAL = "bill-total"
MEMBER_TOTAL = "member-total"
STRATEGY_TOTAL = "strategy-total"

class Stances(object):
    FOR_POS = "FOR+"
    FOR_NEG = "FOR-"
    AGN_POS = "AGN+"
    AGN_NEG = "AGN-"

def has_decision_score(decision):
    return decision.score

def has_deeper_analysis(decision):
    return decision.deeper_analysis

def initialize_hash():
    return {Stances.FOR_POS:0, Stances.FOR_NEG:0, Stances.AGNR_POS:0, Stances.AGN_NEG:0, "RIGHT":0, "WRONG":0, "NA":0}

# Note determine what you are storing here whether in members
# whether members is a name or a DB entry
def valid_decision(decision, members, bill_ids):
    return decision.member in members and decision.bill in bill_ids


def analyze_score(member=None, bill=None, deep=None):
    if member:
        members = [DBMembers.getEntryByName(member)]
    else:
        member_records = DBMembers.getAll()

    if bill:
        bill_ids = [bill.id for bill in DBBill.getEntryByName(bill)]
    else:
        bill_ids = [decision.bill for decision in decisions]
        bill_ids = list(set(bill_ids)

    if deep:
        decisions = filter(has_deeper_analysis, DBDecision.GetAll())
    else:
        decisions = filter(has_decision_score, DBDecision.GetAll())

    analyze_score_helper(member_records, decisions, bill_ids)


def analyze_score_helper(members, decisions, bill_ids):

    global BILL_TOTAL, MEMBER_TOTAL, STRATEGY_TOTAL

    final_decisions = []
    for decision in decisions:
        if valid_decision(decision, members, bill_ids):
            new_decisions.append(decision)

    results = {}
    results[BILL_TOTAL]     = initialize_hash()
    results[MEMBER_TOTAL]   = initialize_hash()
    results[STRATEGY_TOTAL] = initialize_hash()

    print "Initializing..."

    for decision in final_decisions:
        results[decision.bill]   = initialize_hash()
        results[decision.member] = initialize_hash()
        results[decision.strat]  = initialize_hash()

   print "Processing decisions..."

   for decision in final_decisions:
        if decision.score and decision.result:
            stat = (decision.result + decision.score).upper()
            results[decision.bill][stat] += 1
            results[decision.member][stat] += 1
            results[BILL_TOTAL][stat] += 1
            results[MEMBER_TOTAL][stat] += 1
            results[STRATEGY_TOTAL][stat] += 1


def print_score(results, members, decisions, bill_ids):

    global BILL_TOTAL, MEMBER_TOTAL, STRATEGY_TOTAL

    stats_header = ["Right%", "Wrong%", Stances.FOR_POS, Stances.AGNR_POS, Stances.FOR_NEG, Stances.AGN_NEG]

    grand_total = sum(results[BILL_TOTAL].values())

    print_aggregate_score(bill_ids)

    print "Score Results:"
    print_formatted("Bill", *stats_header)

    for billid in bill_ids:

        bill = DBBill.getBillById(billid)
        stats_list = right_wrong(results[billid])
        print_formatted(bill.bill_number, *stats_list)


    stats_list = right_wrong(results[BILL_TOTAL])
    print_formatted("Bill Totals.", *stats_list)


    print_formatted("Member.", *stats_header)

    for member in members:
        stats_list = right_wrong(results[member])
        print_formatted(member.lname.capitalize(), *stats_list)

    stats_list = right_wrong(results[MEMBER_TOTAL])
    print_formatted("Member Totals.", *stats_list)


    print_formatted("Strategy & Rank.", *stats_header)

    #See how strategy names are stored in a decision.
    for strategy in DBStrategy.getAll():
        stats_list = right_wrong(results[strategy.name])
        print_formatted(strategy.name + " "+ strategy.rank, *stats_list)


    stats_list = right_wrong(results[STRATEGY_TOTAL])
    print_formatted("Strategy Totals.", *stats_list)


    print "Total decisions: %s." %grand_total

def right_wrong(results_stats):

    for_pos = results_stats[Stances.FOR_POS]
    for_neg = results_stats[Stances.FOR_NEG]
    agn_pos = results_stats[Stances.AGN_POS]
    agn_neg = results_stats[Stances.AGN_NEG]
    right = for_pos + agn_pos
    wrong = for_neg + agn_neg
    total = (right + wrong) *1.0
    percent_right = (right/total) * 100
    percent_wrong = (wrong/total) * 100
    return [for_pos, for_neg, agn_pos, agn_neg, right, wrong, total, percent_right, percent_wrong]

def print_aggregate_scores(results, bill_ids):

    print_formatted("Bills", "FOR", "AGN", "DIF", "Predicted", "Real", "Right/Wrong")

    for billid in bill_ids:
        print_one_aggregate_score(results, billid)

    right = results["RIGHT"]
    wrong = results["WRONG"]
    total = right + wrong
    percent_right = (right/(total*1.0)) *100
    na = results["NA"]

    print "Aggregate correct: %s out of %s. %s percent." % (right, total, percent_right)

    if na > 0:
        print "%s Hypothetical Votes not included." % na

def print_one_aggregate_score(results, billid):

    for_total = results[billid][Stance.FOR_POS] + results[billid][Stance.FOR_NEG]
    agn_total = results[billid][Stance.AGN_POS] + results[Stance.billid][AGN_NEG]
    diff = abs(for_total - agn_total)

    bill = DBBill.getById(billid)

    real_outcome = get_real_outcome(bill)

    predicted_outcome = get_predicted_outcome(bill, for_total, agn_total)

    if real_outcome is None:
        vote_accurate = "NA"
    elif real_outcome == predicted_outcome:
        vote_accurate = "RIGHT"
    else:
        vote_accurate = "WRONG"

    results[vote_accurate] += 1

    print_formatted(bill.bill_number, for_total, agn_total, diff,
                    predicted_outcome, real_outcome, vote_accurate)


real_outcome_map = {"PASSED": "FOR", "ADOPTED": "FOR",
    "APPROVED": "FOR", "FAILED" : "AGN", "REJECTED": "AGN"}

def get_real_outcome(bill):

   global real_outcome_map

   tally = bill.vote_tally
   if tally is None:
    return None

   return real_outcome_map[bill.vote_tally[0].upper()]


def get_predicted_outcome(for_total, agn_total):

    factor = bill.majority_factor

    if factor is None:
        factor = 1

    if for_total >= agn_total * factor:
        return "FOR"
    else:
        return "AGN"

def print_formatted(*args):
    print '{0:<25} {1:>11} {2:>11} {3:>11} {4:>11} {5:>11} {6:>15}'.format(*args)

def analye_all():
    analyze_decisions()
    tally_scores()
    tally_da_scores()
    analyze_scores()
    analyze_decisions(deep=True)

