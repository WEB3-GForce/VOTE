"""
   Simple strategy: always vote along party lines
   Republicans will support president and democrats will
   oppose the president.
   *** need to change for change in White House ***
"""

def strategy_party(decision, strategy):

    pres_pos = DBBill.getById(decision.bill).presidents_position
    party    = DBMember.getById(decision.member).party
    
    if party == "REP":
        choice = pres_pos
    else: # party == "DEM"
        choice = "AGN" if pres_pos == "FOR" else "FOR"
    
    set_decision_outcome(decision, choice, strategy)
