from member import Member
from database import *
from constants import *

"""
    This file contains various functions useful for aquiring statistics about
    members such as extracting stances from voting records and relations with
    others.
"""

def extract_voting_stances(member):
    """Extracts stances the member holds based on voting history.
    
       Keyword arguments:
            member -- the member to extract stances for

       Postcondition:
            All stances for the member have been extracted. The results are
            NOT saved to the database. The caller must do so.
    """

    print "Extracting stances based on voting record of %s..." % member.name

    member.stances = []
    for vote in member.votes:
        result = extract_vote_stance(vote)
        member.stances.append(result)


# Private
def extract_vote_stance(vote):
    """Helper to extract_voting_stances. Extracts a stance the member holds
       based on voting for a particular bill. It checks the bill and returns
       the stances that can be assumed from voting for or against it.
       
        Keyword arguments:
            vote -- a vote from member.votes
        
        Return
            A list containing all stances to be inferred from the vote.
    """
    print "Extracting stances from vote: %s" % vote

    bill_name    = vote[0]
    for_or_agn   = vote[1]

    bill = get(BILL, {"name": bill_name})    
    if not bill:
        print "WARNING Bill not found: %s" % bill_name
        return []

    if for_or_agn == FOR:
        return bill.stance_for
    elif for_or_agn == AGN:
        return bill.stance_agn
    else:
        print "ERROR extracting stance. Expected FOR or AGN. Received %s" % for_or_agn
        return []

def get_relations_stances(member):

    results = []
    for relationid in member.relations:
        relation = DBRelation.getById(relationid)
        groupid = relation.group

        group = DBGroup.getById(groupid)

        for stanceid in group.stances:
            stance = DBRelation.getById(stanceid)
            stance.relation = relation
            results.append(stance)

    pro_stance = lambda stance : "PRO" == stance.relation.side
    con_stance = lambda stance : "CON" == stance.relation.side
    member.pro_rel_stances = filter(pro_stance, results)
    member.con_rel_stances = filter(con_stance, results)
