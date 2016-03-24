from member import Member
from database import *
from constants import *

"""
    This file contains various functions useful for acquiring statistics about
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
       
       WARNING:
            This erases any stances already contained by the member.
    """

    print "Extracting stances based on voting record of %s..." % member.name
    print "Erasing old stances..."
    
    member.stances = []
    for vote in member.votes:
        member.stances += extract_vote_stance(vote)

    print "Extracting stances completed."
    return

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

    bill_pointer = vote[0]
    for_or_agn   = vote[1]

    # Check if the name used in vote is the name of the bill, bill number, or
    # a synonym
    query = {"$or": [{"name": bill_pointer}, 
             {"synonyms": { "$in" : [ bill_pointer ] }},
             {"bnumber" : bill_pointer} ] }
    bill = get(BILL, query) 
    if not bill:
        print "WARNING Bill not found: %s" % bill_pointer
        return []

    if for_or_agn == FOR:
        return bill.stance_for
    elif for_or_agn == AGN:
        return bill.stance_agn
    else:
        print "ERROR extracting stance. Expected FOR or AGN. Received %s" % for_or_agn
        return []

def get_relations_stances(member):
    """This function looks through the member's relationships and extracts stances
       the member might hold by association. The member opposes what his enemies
       like and supports what his friends support.
       
       Keyword arguments:
            member -- the member to examine
        
       Postcondition
           member.pro_rel_stances contains all the stances the member's friends
           support while member.con_rel_stances contains all the stances the
           member's enemies support.
    """
    results = []
    for relation in member.relations:
        # Check if the relation group is identified by name or id or synonym.
        query = {"$or": [{"name": relation.group}, 
                         {"synonyms": { "$in" : [ relation.group ]}},
                         {"_id" : relation.group}] }
        group = get(GROUP, query)

        if not group:
            print "ERROR group not found: %s" % relation.group
            continue
            
        print "Inferring stances from group: %s" % group.name
        for stance in group.stances:
            stance.relation = relation
            results.append(stance)

    pro_stance = lambda stance : "PRO" == stance.relation.side
    con_stance = lambda stance : "CON" == stance.relation.side
    member.pro_rel_stances = filter(pro_stance, results)
    member.con_rel_stances = filter(con_stance, results)
