"""
   support code for the shifting alliances decision strategy
"""

def divided_groups(decision):
    member = DBMember.getById(decision.member)
    no_credo = decision.MI_credo is None
    beliefs = member.credo
    
    fors = remove_intersection(decision.group_for, decision.group_agn, stance_relation_alikev?)
    
    agns = remove_intersection(decision.group_agn, decision.group_for, stance_relation_alikev?)
    
    fors.sort()
    agns.sort()
    
    if fors and agns and no_credo and beliefs:
        resolve_credo_conflicts(decision)

def equal_stance_rel_import?(stance1, stance2):
    return stance_rel_import(stance1) == stance_Rel_import(stance2)

def stance_rel_import(stance):
    relation = DBRelation.getById(stance.relation)
    return relation.importance

def stance_relation_alikev?(stance1, stance2):
    relation1 = DBRelation.getById(stance1.relation)
    relation2 = DBRelation.getById(stance2.relation)
    relation_alikev?(relation1, relation2)

def resolve_credo_conflicts(decision):
    member = DBMember.getById(decision.member)
    beliefs = member.credo
    
    fors = remove_intersection(decision.group_for, decision.group_agn, stance_relation_alikev?)
    
    agns = remove_intersection(decision.group_agn, decision.group_for, stance_relation_alikev?)
    
    for_conflicts = find_credo_conflicts(beliefs, fors)
    agn_conflicts = find_credo_conflicts(beliefs, agns)
    
    if for_conflicts and agn_conflcits:
        print "Conflicts with BOTH sides. No decision."
        return
    
    elif for_conflicts:
        print "Conflict with FOR Groups: %s" % for_conflicts
        return "AGN"

    else agn_conflicts:
        print "Conflict with AGN groups: %s" % agn_conflicts
        return "FOR"
    else: # No conflicts with either
        return

def find_credo_conflicts(beliefs, stance_list):
    result = []
    for stance in stance_list
        answer = find_credo_stance_conflicts(stance, beliefs)
        if answer not None:
            result += answer
    return result        

def find_credo_stance_conflicts(stance beliefs):
    groupid = DBRelation.getById(stance.relation).group
    if groupid:
        group = DBGroup.getById(groupid)
        find_stance_conflicts(beliefs, group.stances)

# I am concerned. Stance1 and stance2 don't seem like lists but
# regular stances. I may be wrong, but worth checking out.
def find_stance_conflicts(stance1 stance2)
    find_intersection(stance1, stance2, stance_opposite?)

def find_intersection(list1, list2, equal_fun):
    filter_fun = lambda item : any(equal_fun(item, element) for element in l2)
    return filter(filter_fun, list1)

def stance_opposite?(stance1, stance2):
    issue1 = DBIssue.getById(stance1.issue)
    issue2 = DBIssue.getById(stance2.issue)
    return issue1 == issue2 and stance1.side != stance2.side
