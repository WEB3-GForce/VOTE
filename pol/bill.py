from printable_object import PrintableObject

class Bill(PrintableObject):

    """
    The Bill class represents bills that Congress is considering. Congressmen
    and Congresswomen will vote for these bills either for or against them.
    """

    def __init__(self, **entries):
    
        """
        Construct a new Bill object.

        name                    -- The name of the bill.
        english_name            -- The name of the bill in English.
        french_name             -- The name of the bill in French.
        bill_number             -- The number of the bill.
        date_of_vote            -- The date when this bill will be voted upon.

        vote_tally              -- A list with the number of votes for and against
                                   the bill; the list is of the form
                                   [#_of_votes_for, #_of_votes_against].

        presidents_position     -- The President's position on the bill, either
                                   FOR or AGAINST.

        majority_factor         -- The number of votes needed for the bill to pass
        importance              -- The intrinsic importance of the bill.

        stance_for              -- What voting for this bill would imply about 
                                   what the Congressman or -woman supports.

        stance_against          -- What voting against this bill would imply 
                                   about what the Congressman or -woman supports.

        inferred_stance_for     -- What voting for this bill would imply about 
                                   the what the Congressman or -woman supports.
                                   This is inferred from remarks about the bill.

        inferred_stance_against -- What voting against this bill would imply
                                   about the what the Congressman or -woman
                                   supports. This is inferred from remarks
                                   about the bill.

        synonyms                -- A list of synonyms for the bill (AKA related
                                   topics).
        notes                   -- This is a list of remarks about the bill.
        remarks                 -- textual comments
        return                  -- returns nothing.
        """
        self.name = None
        self.english_name = None
        self.french_name = None
        self.bill_number = None
        self.date_of_vote = None
        self.vote_tally = []
        self.presidents_position = None
        self.majority_factor =  None
        self.importance = None
        self.stance_for = []
        self.stance_against = []
        self.inferred_stance_for = []
        self.inferred_stance_against = []
        self.synonyms = []
        self.notes = []
        self.remarks = None
        self.__dict__.update(entries)
