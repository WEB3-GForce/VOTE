from printable_object import PrintableObject

"""
File Generated by Lisp2Python Translator
"""

class Member(PrintableObject):

    """"
    A class that represnts a particular member.
    """

    def __init__(self, name, fname, lname, english_short, notes, gender, votes,
                 new_votes, stances, issues, credo, groups, relations,
                 pro_rel_stances, con_rel_stances, stance_sort_key, district,
                 term_start, term_end, party, committees):

        """
        Constructs a new Member object.

        name            -- name of member
        fname           -- first name symbol for member
        lname           -- last name symbol for member
        english_short   -- short version of name
        notes           -- list of remarks
        gender          -- male or female
        votes           -- past voting record -- list of bill/vote pairs
        new_votes       -- test votes -- list of bill/vote pairs
        stances         -- stances extracted from votes
        issues          -- list of issues of importance to this member
        credo           -- list of stances personal to this member
        groups          -- list of groups of importance to this member
        relations       -- list of relations with groups
        pro_rel_stances -- list of stances inferred from pro relationships
        con_rel_stances -- list of stances inferred from con relationships
        stance_sort_key -- Symbol LOYALTY or EQUITY used for setting priorities
        district        -- name of district from which elected
        term_start      -- year elected to Congress
        term_end        -- year left Congress
        party           -- political party affiliation
        committees      -- list of committees on which member serves

        return          -- returns nothing
        """
        self.name = name
        self.fname = fname
        self.lname = lname
        self.english_short = english_short
        self.notes = notes
        self.gender = gender
        self.votes = votes
        self.new_votes = new_votes
        self.stances = stances
        self.issues = issues
        self.credo = credo
        self.groups = groups
        self.relations = relations
        self.pro_rel_stances = pro_rel_stances
        self.con_rel_stances = con_rel_stances
        self.stance_sort_key = stance_sort_key
        self.district = district
        self.term_start = term_start
        self.term_end = term_end
        self.party = party
        self.committees = committees

    def extract_voting_stances():
        print "Extracting stances based on voting record of %s" % self.name
        
        self.stances = []
        for vote in member.votes:
            result = self.extract_vote_stance(vote)
            self.stances.append(result)
            

    def extract_vote_stance(vote):
        bill_id = vote[0]
        for_or_agn = vote[1]
        
        bill = DBBill.GetById(bill_id)
        
        if for_or_agn == "FOR":
            return bill.stance_for
        elif for_or_agn == "AGN":
            return bill.stance_agn
        else:
            print "ERROR in EXTRACT STANCE: Expected FOR or AGN. Not %s" % for_or_agn
            

    def get_relations_stances():
        
        results = []
        for relationid in self.relations:
            relation = DBRelation.getById(relationid)
            groupid = relation.group
            
            group = DBGroup.getById(groupid)
            
            for stanceid in group.stances:
                stance = DBRelation.getById(stanceid)
                stance.relation = relation
                results.append(stance)
                
        pro_stance? = lambda stance : "PRO" == stance.relation.side
        con_stance? = lambda stance : "CON" == stance.relation.side
        member.pro_rel_stances = filter(pro_stance?, stances)
        member.con_rel_stances = filter(con_stance?, stances)
        
