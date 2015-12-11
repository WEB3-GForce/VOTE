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
    return {Stances.FOR_POS:0, Stances.FOR_NEG:0, Stances.AGNR_POS:0, Stances.AGN_NEG:0}

def prune_decisions(main_function):

    return main_function

def analyze_score():
    member_records = DBMembers.getAll()
    decisions = filter(has_decision_score, DBDecision.GetAll())
    bill_ids = [decision.bill for decision in decisions]
    bill_ids = list(set(bill_ids)
    analyze_score(member_records, decisions, bill_ids)

def analyze_member_score(member):
    members = [DBMembers.getEntryByName(member)]
    decisions = filter(has_decision_score, DBDecision.GetAll())
    bill_ids = [decision.bill for decision in decisions]
    bill_ids = list(set(bill_ids)
    analyze_score(members, decisions, bill_ids)

def analyze_bill_score(bill):
    member_records = DBMembers.getAll()
    decisions = filter(has_decision_score, DBDecision.GetAll())
    bill_ids = [DBBill.getEntryByName(bill)]
    analyze_score(member_records, decisions, bill_ids)

def analyze_score_deep():
    member_records = DBMembers.getAll()
    decisions = filter(has_deeper_analysis, DBDecision.GetAll())
    bill_ids = [decision.bill for decision in decisions]
    bill_ids = list(set(bill_ids)
    analyze_score(member_records, decisions, bill_ids)

def valid_decision(decision, members, bill_ids)
    return decision.member in members and decision.bill in bill_ids

def analyze_score(members, decisions, bill_ids):

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
          
    
        
