import operator

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

def firm_decision(decision, side, reasons, old_downside, strat):
    bill = DBBill.getById(decision.bill)
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
    
    firm_dicision(decision, result, reason, downside, strat)

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
    for_stances = decision.for_Stances
    agn_stances = decision.agn_stances
    
    if not for_stances and agn_stances:
        return firm_decision(decision, "AGN", agn_stances, [], strat)
    if not agn_stances and for_stances:
        return firm_decision(decision, "FOR", for_stances, [], strat)
    else:
        return None
