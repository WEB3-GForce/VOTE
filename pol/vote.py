import copy

from constants import *
from database import *
from decision import *
from decision_stats import *
from member_stats import *
from utils import remove_duplicates

from member import Member

# Future note for expansion. Lname is a proper identifier for now. Change once
# there are multiple members with the same last name.
def vote(member_lname, bill_number):
    """Predicts how the specified member will vote on the given bill. This
    function is the standard way of calling VOTE from the commandline. It relies
    on a helper that takes actual DB objects.

    Keyword arguments:
        member_lname -- the last name of the member
        bill_number  -- the number of the bill

    Returns:
        A decision object containing the results of the decision.
    """
    member = get(MEMBER, {"lname" : member_lname.upper()})
    bill   = get(BILL, {"bnumber" : bill_number.upper()})

    if not member:
        print "Member not found in DB: %s" % member_lname
        return None
    if not bill:
        print "Bill not found in DB: %s" % bill_number
        return None

    return vote_helper(member, bill)


def vote_helper(member, bill):
    """A helper to vote, predicts how the specified member will vote on the
    given bill.

    Keyword arguments:
        member -- a Member object corresponding on the member who will vete
        bill   -- a Bill object of the bill to be voted on.

    Returns:
        A decision object containing the results of the decision.
    """

    print "Calculating vote for %s on bill %s..." % (member.name, bill.bnumber)

    decision = Decision()
    initialize_decision(decision, member, bill)

    print "Updating decision metrics..."
    update_decision_metrics(decision)
    print "Update completed."

    update_decision_metrics(decision)

    apply_decision_strategies(decision)

    compare_with_real_vote(decision)

    update_decision_dbase(decision) # insert into database

    if decision.strategy:
       print decision
    else:
        print "No decision"

    return decision

def save(decision):
    """Save the decision to the DB."""

    print "Saving the decision to the database."
    if DECISION.insert(copy.deepcopy(decision.__dict__)):
        print "Decision saved."
    else:
        print "ERROR decision not saved."


def initialize_decision(decision, member, bill):
    """Initializes a decision object with basic info about the member and bill.
       Extracts stances for the member based on the bill and the member's
       relations.

       Keyword arguments:
            decision -- the decision object to initialize
            member   -- a Member object corresponding to the member who will vote
            bill     -- a Bill object of the bill to be voted on.

        Postcondition:
            The decision object has been updated.
    """

    print "Initializing decision..."

    if not member.stances:
        extract_voting_stances(member)

    decision.member = member._id
    decision.bill   = bill._id

    infer_member_rel_stances(member)

    print member

    print "Analyzing alternative positions..."

    decision.for_stances = match_stances_for(member, bill)
    decision.agn_stances = match_stances_agn(member, bill)

    print "Initialization complete."


def infer_member_rel_stances(member):
    """Infers the stances that a member might have based on relationships with
       others.

       Keyword arguments:
            member   -- the member whose stances will be inferred

        Postcondition:
            The member's stances have been updated to include those from
            relationships.
    """
    if not member.pro_rel_stances:
        print "Inferring stances from relations of %s..." % member.name
        get_relations_stances(member)
        print "Inferring stances from relations completed."


def match_stances_for(member, bill):
    """This function filters member stances by stances that are implied by
    voting for the bill.

       Keyword arguments:
            member   -- the member whose stances will be filtered
            bill     -- the bill whose stances will be used to filter the member
                        stances.

       Return:
            A list that contains only those member stances that would be implied
            by voting for the bill.

       Notes:
            In other words, this function checks to see if the member has any
            reasons to vote for the bill.
    """
    print "Considering implications of voting FOR on bill %s..." % bill.bnumber
    print "Matching member stances with bill stances..."
    stances = match_stances(bill.stance_for, member)
    stances = match_stances_sort(member, bill, stances)
    print "Considering FOR implications completed."
    return stances


def match_stances_agn(member, bill):
    """This function filters member stances by stances that are implied by
    voting against the bill.

       Keyword arguments:
            member   -- the member whose stances will be filtered
            bill     -- the bill whose stances will be used to filter the member
                        stances.

       Return:
            A list that contains only those member stances that would be implied
            by voting against the bill.

       Notes:
            In other words, this function checks to see if the member has any
            reasons to vote against the bill.
    """
    print "Considering implications of voting AGN on bill %s..." % bill.bnumber
    print "Matching member stances with bill stances..."
    stances = match_stances(bill.stance_agn, member)
    stances = match_stances_sort(member, bill, stances)
    print "Considering AGN implications completed."
    return stances


def match_stances_sort(member, bill, stances):
    """This is a helper function for the two functions above. It sorts the
    matched stances list and removes old voting data if necessary.

       Keyword arguments:
            member   -- the member whose stances were filtered
            bill     -- the bill whose stances were used to filter the member
                        stances.
            stances  -- the filtered stances

       Return:
            A sorted list with the old votes removed
    """
    sort_key = member.stance_sort_key or EQUITY
    print "Sorting stances based on %s order..." % sort_key

    for stance in stances:
        stance.set_sort_key(sort_key)

    stances = remove_old_votes(stances, bill)
    stances.sort(key=lambda stance: stance.get_sort_key)
    return stances


def is_bill_source(stance, bill):
    """Used as a filter function, determines if a stance's source is a given bill.

       Keyword arguments:
            stance   -- the stance to check the source of
            bill     -- the potential source of the stance.

        Postcondition:
            Whether the bill is the stance's source. Since bills can be referenced
            by a synonym, name, bill number, or Mongo id, all are checked.
    """
    return (stance.source == bill._id or stance.source == bill.name or
            stance.source == bill.bnumber or stance in bill.synonyms)


def remove_old_votes(stances, bill):
    """Filters stances to contain only stances that come from the bill.

       Keyword arguments:
            stances   -- the list of stances to purge
            bill      -- the bill whose stances will be kept

        Return:
            The newly filtered stances list. If the flag no_old_votes is set,
            then the stances will be filtered so that only stances from the bill
            itself are used. If it is not set, all stances are used.
    """
    if no_old_votes:
        filter_fun = lambda stance : is_bill_source(stance, bill)
        stances = filter(filter_fun, stances)
    return stances


# This flag is used in remove_old_votes. This is used to determine whether the
# function should filter stances such that only stances that originate from the
# bill are kept.
no_old_votes = True


def no_old_votes(flag):
    """ Sets the no_old_votes flag."""
    global no_old_votes
    no_old_votes = flag


def match_stances(stances, member):
    """Filters the member's stances keeping only those that match a stance in
       stances. The member's stances consist of personal stances (member.credo),
       voting record stances (member.stances), and group stances
       (member.pro_rel_stances)

       Keyword arguments:
            stances   -- the list of stances to filter the member stances by
            member    -- the member whose stances will be filtered.

        Return:
            A list of all member stances found in stances. The list has
            duplicates removed.
    """
    matches = []
    member_stances = member.credo + member.stances + member.pro_rel_stances
    for stance in stances:
        filter_fun = lambda member_stance : stance.match(member_stance)
        matches += filter(filter_fun, member_stances)
    return remove_duplicates(matches)


def apply_decision_strategies(decision):
    """Applies strategies to make the decision. Tries all possible strategies
    in the database and stops at the first one that succeeds.

       Keyword arguments:
            decision   -- the object that will store the decision

        Return:
            The decision object passed into the function updated with the decision.
    """

    print "Applying decision strategies..."

    # In the future, define a specific order for how to apply
    # strategies. For now, just run them in whatever order
    # Mongo gives them.
    for strategy_hash in STRATEGY.find({}):

        strategy = Strategy(**strategy_hash)

        # See if the name of the strategy function is defined
        # globally.
        # Dangerous. If database is corrupted, could lead to
        # calling strange things. For future, create a hash
        # that limits the options.
        strategy_function = globals()[strategy.test_code]

        print "Trying decision strategy: %s" % strategy.name

        if strategy_function and strategy_code(decision, strategy):
            member = get(MEMBER, {"_id" : decision.member})
            bill   = get(BILL,   {"_id" : decision.bill})
            print "Success!"
            print "DECISION: %s will vote %s on bill %s" % (member.name, decision.result, bill.bnumber)

            # This prints more information about the decision.
            # Proof this code and add when ready.
            #strategy_protocol = globals()[strategy.protocol]
            #if strategy_protocol:
            #   strategy_protocol(decision)

            decision.reason = group_reasons(decision.reason)
            decision.downside = group_reasons(decision.downside)
            return decision

        elif not strategy_function:
            print "ERROR strategy code not found."
        else:
             print "%s failed." % strategy.name


def group_reasons(stances):
    """Groups together the stances list so that the stances that match each other
    via their stance.match function will be next to each other.

       Keyword arguments:
            stances   -- the list of stances to sort into groups

        Return:
            The new stance list sorted into groups.
    """
    result = []

    while stances:

        key = stances[0]
        left = []
        result.append(key)

        for stance in stances[1:]:
            if key.match(stance):
                result.append(stance)
            else:
                left.append(stance)

        stances = left

    return result


def get_members(member_name=None):
    """Retrieves the members for vote_all. If the name is specified, the specific
    member is looked up in the DB. If the name is not specified or the member
    was not found, an iterator over a search for all members is returned.

       Keyword arguments:
            member_name   -- the name of the member to get.

        Return:
            An iterator for all members who will vote.
    """
    member = None
    if member_name:
        member = get(MEMBER, {"lname" : member_lname.upper()})

    if member:
        return [member]
    else:
        return MEMBER.find({})


def get_bills(bill_number=None):
    """Retrieves the bills for vote_all. If the bill_number is specified, it
    returns a list of the specified bill. If not or the bill is not found, it
    returns an iterator over all the bills in the database.

       Keyword arguments:
            bill_number   -- the number of the bill to retrieve.

        Return:
            An iterator for all bills that will be voted upon.
    """
    bill = None
    if bill_number:
        bill = get(BILL, {"bnumber" : bill_number.upper()})

    if bill:
        return [bill]
    else:
        return BILL.find({})


def vote_all(member_lname = None, bill_number = None):
    """Run the vote program for all members on all bills.

       Keyword arguments:
            member_lname  -- optional, the last name of the member to simulate
            bill_number   -- optional, the bill number of the bill to decide on

        Postcondition:
            The decisions have been made and the database updated approriately

        Note:
            There are multiple ways to call this function

            vote-all()                   : process all members on all bills
            vote-all(member_name = name) : process all bills for given member
            vote-all(bill_name = bill)   : process all members for given bill
    """
    for member_hash in get_members(member_lname):
        for bill_hash in get_bills(bill_number):
            member = Member(**member_hash)
            bill   = Bill(**bill_hash)
            vote_helper(member, bill)
            print "\n"
