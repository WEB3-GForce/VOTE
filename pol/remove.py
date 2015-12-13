def stance_equal?(stance1, stance2):
    return (stance_alikev?(stance1, stance2) and
           stance1.importance == stance2.importance)

# Might have to look a little more about how to determine
# if issues or groups are equivalent with the new DB.
def stance_alikev?(stance1, stance2):
    issue1 = DBIssue.getById(stance1.issue)
    issue2 = DBIssue.getById(stance2.issue)
    return (issue1 == issue2 and stance1.side == stance2.side)
    
def relation_alikev?(relation1, relation2):
    group1 = DBGroup.getById(relation1.issue)
    group2 = DBGroup.getById(relation2.issue)
    return (group1 == group2 and relation1.side == relation2.side)
    
