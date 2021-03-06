from printable_object import PrintableObject

"""
File Generated by Lisp2Python Translator
"""

class Member(PrintableObject):

    """"
    A class that represnts a particular member.
    """

    def __init__(self, **entries):

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
        self.name = None
        self.fname = None
        self.lname = None
        self.english_short = None
        self.notes = []
        self.gender = None
        self.votes = []
        self.new_votes = []
        self.stances = []
        self.issues = []
        self.credo = []
        self.groups = []
        self.relations = []
        self.pro_rel_stances = []
        self.con_rel_stances = []
        self.stance_sort_key = None
        self.district = None
        self.term_start = None
        self.term_end = None
        self.party = None
        self.committees = None
        self.__dict__.update(entries)
