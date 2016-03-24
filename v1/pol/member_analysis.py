"""
  This file contains procedures for analyzing members' stances and
  voting records.  There are two main routines: mdiff and consistent?

 ---------------------------------------------------
   (mdiff mem1 mem2)
 ---------------------------------------------------
 compare the voting records of two members.

"""

def mem_diff(memberid1, memberid2):
    member1 = DBMember.getById(memberid1)
    member2 = DBMember.getById(memberid2)
    votes1 = member1.votes
    votes2 = member2.votes
    votes1.sort()
    votes2.sort()
    print_diffs(member1.name, member2.name, votes1, votes2)

def print_diffs(member1_name, member2_name, votes1, votes2):
    if votes1 is None:
        print "No voting record for", member1_name
        return
    if votes2 is None:
        print "No voting record for", member2_name
    diff_match(member1_name, member2_name, votes1, votes)

def diff_match(member1_name, member2_name, votes1, votes2):

    print "Bill\t%s\t%s" % (member1_name, member2_name)

    for vote1, vote2 in zip(votes1, votes2):
        if vote1 == vote2:
            continue
        elif vote1[0] == vote2[0]:
            print "%s\t%s\t%s" % (vote1[0], vote1[1], vote2[1])
        else:
            print "%s\t%s\t%s" % (vote1[0], vote1[1], "NA")
            print "%s\t%s\t%s" % (vote2[0], "NA", vote2[1])


"""
---------------------------------------------------
   (consistent? mem)   ---------------------------------------------------
   detect inconsistencies in a member's relations, credo,
   and voting record
"""

def consistent(memberid):
    member = DBMember.GetById(memberid)
    # This should set member.stances
    member.extract_voting_stances()
    infer_member_rel_stances(memberid)
    member.credo.sort()
    member.stances.sort()
    member.pro_rel_stances.sort()

    print "Printing out inconsistances in member's relations, crdeo, and voting record."

    print "Member: %s" % member.name

    filter_stances(member.credo, member.stances)
    filter_stances(member.credo, member.pro_rel_stances)
    filter_stances(member.stances, member.pro_rel_stances)

def filter_stances(stance_list1, stance_list2):
    for stanceid1, stanceid2 in zip(stance_list1, stance_list2):
        stance1 = DBStance.getStance(stanceid1)
        stance2 = DBStance.getStance(stanceid2)

        if (stance1.issue == stance2.issue and
            stance1.side != stance2.side):
           print "%s\n%s" % (stance1, stance2)
