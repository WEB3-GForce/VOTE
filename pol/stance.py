from printable_object import PrintableObject
from constants import *

"""
File Generated by Lisp2Python Translator
"""

class Stance(PrintableObject):

    """"
    A class that represents a particular stance.
    """

    def __init__(self, **entries):

        """
        Constructs a new Stance object.

        source            -- particular instance of member, bill, issue, group
        source_db         -- db of source" 
        source_structure  -- ?" 
        relation          -- ?" 
        issue             -- stance issue" 
        issue_structure   -- ?" 
        importance        -- stance importance A, B, C, D" 
        side              -- stance side pro or con" 
        sort_key          -- ?" 
        siblings          -- related stances must be stance-alikev?

        return            -- returns nothing
        """
        self.source = None
        self.source_db = None
        self.source_structure = None
        self.relation = None
        self.issue = None
        self.issue_structure = None
        self.importance = None
        self.side = None

        # Never use sort key directly but use get_sort_key
        self.sort_key = None
        self.siblings = None
        self.__dict__.update(entries)


    def get_sort_key(self):
        """Returns the sort_key if defined or the importance otherwise.
           IMPORTANT: Call this instead of self.sort_key."""
        return self.sort_key or self.importance


    def set_sort_key(self, keyword):
        """Sets the sort key based on the keyword. See below for comments on
           what each means.
        
           Keyword arguments:
                keyword -- the keyword that defines how stances will be sorted
        
           Postcondition:
                The stance has been updated to reflect the keyword
        """    
        stance_import = self.importance
        rel_import = B
        if self.relation:
            rel_import = self.relation.importance
        
        if keyword == LOYALTY:
            # For loyalty, the importance of the source relation of the stance is
            # valued more by a member, then stance importance.
            self.sort_key = [rel_import, stance_import]
        elif keyword == EQUITY:
            # For equity, a stance importance is valued more by the member and
            # then the importance of the relation from which this stance was
            # taken from
            self.sort_key = [stance_import, rel_import]
        else:
            print "ERROR in setting source key for stance. Unknown keyword: %s" % keyword


    def match(self, stance2):
        """Determines if another stance matches this stance.
        
           Keyword arguments:
                stance2 -- the other stance to check for equality with
        
           Returns:
                True if the stances match, False otherwise. As long as the issue
                and side are the same, the stances are said to match
                partially. If they also have the same importance, it is a total
                match. For now, both cases result in true.
        """    
        match_issue  = (self.issue == stance2.issue)
        match_side   = (self.side == stance2.side)
        match_import = (self.importance == stance2.importance)
        
        if match_issue and match_side and match_import:
            # Complete match
            return True
        elif match_issue and match_side:
            # Partial match
            return True
        else:
            return False
        

