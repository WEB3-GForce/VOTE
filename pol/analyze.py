# sourced from pol/analyze.lisp
#
# Copyright © 2015 krishpop <krishnan1994@gmail.com>
#
# Distributed under terms of the MIT license.

bill_total, mem_total, mem_results, billid_results = {}, {}, {}, {}

def analyze_decisions(*opts, deep=False):
    options = opts[0]
    bills = list(get_node(options, "bill")) if options else db_all("bill")
    billids = [bill.id for bill in bills]
    members = list(get_node(options, "member")) if options else db_all("member")
    memids = [mem.id for mem in members]
    strats = [strategy.test_code for strategy in db_all("strategy")]
    deep_levels = ('a', 'b', 'c', 'd')
    decisions  = db_all("decision").deeper_analysis() if deep else db_all("decisions")

    # initializes property lists for FOR/AGN tallies
    global bill_total, mem_total
    bill_total["for"], mem_total["for"], bill_total["agn"], mem_total["agn"] = 0, 0, 0, 0

    global mem_results, billid_results
    for memid in memids:
        mem_results[mem_id]["for"] = 0
        mem_results[mem_id]["agn"] = 0
    for billid in billids:
        billid_results[billid]["for"] = 0
        billid_results[billid]["agn"] = 0

    # initializes property lists for strategies

    for strat in strats:
        bill_total[strat] = 0
        mem_total[strat] = 0
        for billid in billids:
            billid_results[billid][strat] = 0
        for memid in memids:
            mem_results[memid][strat] = 0

    # initialize property lists for deep analysis levels
    # ...

    # count apportioned strats
    print "Processing decisions"
    for decision_id in decisions:
        strat = decision_id.strategy
        level = decision_id.deeper_analysis
        side = decision_id.side
        billid = decision_id.bill
        memid = decision_id.member
        billid_results[billid][strat] += 1
        bill_total[strat] += 1
        mem_results[memid][strat] += 1
        mem_total[strat] += 1
        # tally for/agn
        billid_results[billid][side] += 1
        bill_total[side] += 1
        mem_results[memid][side] += 1
        mem_total[side] += 1

    print_results(billids, memids, strats, decisions)

def print_results(billids, memids, strats, decisions):
    grand_total = sum(map(lambda strat: strat_results[strat]["bill_total"], strats))

    # Print results.
    print "Results"
    print "=" * 30, '\n'

    strat_list = [strat.index() for strat in strats]
    print_formatted("Bill/Strategy.", *strat_list)

    for billid in billids:
        billid_results_list = [billid_results[billid][strat] for strat in strats]
        print_formatted(get_node(billid, "bill"), *billid_results_list)

    # Print bill totals.
    bill_total_list = [bill_total[strat] for strat in strats]
    print_formatted("Bill Totals.", *bill_total_list)

    # Print members.
    print_formatted("Member/Strategy.", *strat_list)
    for memid in memids:
        mem_results_list = [mem_results[memid][strat] for strat in strats]
        member_name = str.upper(get_node(memid, "member").lname)
        print_formatted(member_name, *mem_results_list)

    # print member_totals
    mem_total_list = [mem_total[strat] for strat in strats]
    print_formatted("Member Totals.", *mem_total_list)


# Procedures to compare predicted vote with real vote

def compare_with_real_vote(decision):
    if set_real_vote(decision):
        return set_score(decision)
    else:
        return not_a_test_vote()


def set_real_vote(decision):
    memid = decision.member
    billid = decision.bill
    names = synonyms(billid)
    votes = member_votes(memid)
    decision.real_vote = find_real_vote(names, votes)


def find_real_vote(names, votes=None):
    if not votes:
        return None
    elif len(set(names).intersection(votes[0])):
        return votes[0][1]
    else:
        return find_real_vote(names, vote[1:])

def set_score(decision):
    result = decision.result
    real_vote = decision.real_vote
    if not real_vote:
        return None
    else:
        if result == real_vote:
            decision.score =  '+'
        elif real_vote in ["for", "agn"]:
            decision.score = '-'
        else:
            decision.score = '?'


def tally_scores():
    correct_for, correct_agn, wrong_for, wrong_agn = 0, 0, 0, 0
    for decision in db_all(decisions):
        if decision.score == '+':
            if decision.result = "for":
                correct_for += 1
            elif decison.result == "agn":
                correct_agn += 1
        elif decision.score == '-':
            if decision.result = "for":
                wrong_for += 1
            elif decison.result == "agn":
                wrong_agn += 1
    print_scores(correct_for, correct_agn, wrong_for, wrong_agn)


def print_scores(correct_for, correct_agn, wrong_for, wrong_agn):
    correct = correct_for + correct_agn
    wrong = wrong_for + wrong_agn
    total = correct + wrong
    print "{0:>15} {1:>5} {2:>5}".format("Percentage", "For", "Agn")
    print "{0:<10} {1:>5} {2:>5} {3:>5}".format("Correct:", str(correct/float(total)), str(correct_for), str(correct_agn))
    print "{0:<10} {1:>5} {2:>5} {3:>5}".format("Wrong:", str(wrong/float(total)), str(wrong_for), str(wrong_agn))
    print "T{0:<10} {1:>5}".format("Total", total)


def tally_da_scores():
    tally_scores()


def print_formatted(header, *args):
    print_string = "{0:<25}"
    for i in xrange(1, len(args) + 1):
        print_string += " {" + str(i) + ":>11}"
    print print_string.format(header, *args)
