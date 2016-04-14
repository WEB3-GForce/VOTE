"""
    VOTE - A decision program for predicting votes in Congress.
    Copyright (C) 2016 William Edward Bailey, III (WEB3 or WEBIII):
      https://github.com/WEB3-GForce
    Based on Stephen Slade's Ph.D Thesis:
      zoo.cs.yale.edu/classes/cs458/materials/RealisticRationality.pdf

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from src.analyze import decision_analyze
from src.analyze import member_analyze
from src.analyze import stance_analyze
from src.classes.decision import Decision
from src.classes.strategies import strategy_hash
from src.constants import database as db_constants
from src.constants import logger
from src.constants import outcomes
from src.database.pymongodb import PymongoDB
from src.database import queries

def vote(member_identifier, bill_identifier):
    """Predicts how the specified member will vote on the given bill.

    Arguments:
        member_identifier: A value that identifies the member such as full_name
            or database id. Make sure the value uniquely identifies the member
            in the database.
        bill_identifier: A value that identifies the bill such as bill_number or
            database id. Make sure the value uniquely identifies the bill in the
            database.

    Returns:
        A decision object containing the results of the decision on the vote
    """

    member = PymongoDB.get_db().find_one(db_constants.MEMBERS,
        queries.member_query(member_identifier))
    bill = PymongoDB.get_db().find_one(db_constants.BILLS,
        queries.bill_query(bill_identifier))

    if not member:
        logger.LOGGER.error("Member not found in DB: %s" % member_identifier)
        return None
    if not bill:
        logger.LOGGER.error("Bill not found in DB: %s" % bill_identifier)
        return None

    return _vote_helper(member, bill)


def vote_all(member_identifier=None, bill_identifier=None):
    """Run the vote program for all members on all bills. The function has
    optional parameters to run on specific members or bills. For example, by
    specifying member_identifier, the function can simulate all decisions that
    particular member would make on all bills. By specifying bill_identifier,
    the function can simulate the decisions that all members would make on that
    particular bill. If the arguments are left as None, all members and all
    bills will be used.

    Arguments:
        member_identifier: optional, an identifier such as full_name of the
            member to simulate
        bill_identifier: optional, the bill identifier of the bill to decide on

    Usage Examples: 
        vote_all()                   : process all members on all bills
        vote_all(member_name = name) : process all bills for given member
        vote_all(bill_name = bill)   : process all members for a given bill
    """
    for member in _get_members(member_identifier):
        for bill in _get_bills(bill_identifier):
            _vote_helper(member, bill)


def _get_members(member_identifier=None):
    """Retrieves the members for vote_all. If member_identifier is specified,
    the specific member is looked up in the DB. If the name is not specified or
    the member was not found, a cursor for a Pymongo find request is returned.

    Arguments:
        member_identifier: the identifier of the member to retrieve.

    Returns:
        Either an array with the member specified in member_identifier or an
        iterator for all members who will vote.
    """
    member = None
    if member_identifier:
        member = PymongoDB.get_db().find_one(db_constants.MEMBERS,
            queries.member_query(member_identifier))

    if member:
        return [member]
    else:
        if member_identifier:
            logger.LOGGER.error("Bill not found: %s" % member_identifier)
        return PymongoDB.get_db().find(db_constants.MEMBERS)


def _get_bills(bill_identifier=None):
    """Retrieves the bills for vote_all. If the bill_identifier is specified, it
    returns a list of the specified bill. If not, it returns an iterator over
    all the bills in the database.

    Arguments:
        bill_identifier: an identifier for the bill to retrieve.

    Returns:
        Either an array with the bill specified by bill_identifier or an
        iterator for all bills that will be voted upon.
    """
    bill = None
    if bill_identifier:
        bill = PymongoDB.get_db().find_one(db_constants.BILLS,
            queries.bill_query(bill_identifier))

    if bill:
        return [bill]
    else:
        if bill_identifier:
            logger.LOGGER.error("Bill not found: %s" % bill_identifier)
        return PymongoDB.get_db().find(db_constants.BILLS)


def _vote_helper(member, bill):
    """A helper to vote, predicts how the specified member will vote on the
    given bill.

    Arguments:
        member: a Member object representing the member who will vote
        bill: a Bill object representing the bill to be voted upon

    Returns:
        A decision object containing the results of the decision on the vote
    """
    logger.LOGGER.info("Predicting how %s will vote on bill %s..." %
        (member.full_name, bill.bill_number))

    decision = Decision()
    _initialize_decision(decision, member, bill)
    decision_analyze.update_decision_metrics(decision)

    _apply_decision_strategies(member, bill, decision)

    if decision.strategy:
        _save(decision)
    return decision


def _initialize_decision(decision, member, bill):
    """Initializes a decision object with information about the member and bill.
    Extracts stances for the member based on the bill and the member's 
    relations.

     Arguments:
        decision: the decision object to initialize
        member: a Member object corresponding to the member who will vote
        bill: a Bill object of the bill to be voted on.
    """

    logger.LOGGER.info("Initializing decision...")

    decision.member = member._id
    decision.bill = bill._id

    if not member.stances:
        member_analyze.extract_voting_stances(member)

    if not member.pro_rel_stances:
        member_analyze.infer_relations_stances(member)

    logger.LOGGER.info("Analyzing alternative positions...")

    decision.for_stances = member_analyze.match_stances(member, bill, outcomes.FOR)
    decision.agn_stances = member_analyze.match_stances(member, bill, outcomes.AGN)

    logger.LOGGER.info("Initialization complete.")


def _save(decision):
    """Saves the decision to the DB.
    
    Arguments:
        decision: the decision to save
    """
    logger.LOGGER.info("Saving the decision to the database...")
    result = PymongoDB.get_db().insert_one(db_constants.DECISIONS, decision)
    if result:
        logger.LOGGER.info("Decision saved.")
    else:
        logger.LOGGER.error("ERROR decision not saved.")


def _retrieve_strategy_list():
    """ Queries the database and finds all StrategyEntry's that are active. It
    returns them in an array sorted by their rank. This list specifies the
    strategies that should be applied to the decision and their order.

    Returns:
        An array of StrategyEntry's in the database that are active sorted by
        rank.
    """
    strategy_entries = []
    for strategy_entry in PymongoDB.get_db().find(db_constants.STRATEGIES):
        if strategy_entry.active:
            strategy_entries.append(strategy_entry)

    sort_key_fun = lambda strat_entry: strat_entry.rank
    strategy_entries.sort(key=sort_key_fun)
    return strategy_entries


def _apply_decision_strategies(member, bill, decision):
    """Applies strategies to compute a result for the decision. Tries all
    active strategies in the database and stops at the first one that succeeds.

    Arguments:
        member: the Member voting on the bill
        bill: the Bill to be voted upon.
        decision: the object that represents the decision

        Return:
            True if a decision was made, false otherwise. Upon success, the
            decision object has been updated appropriately.
    """
    logger.LOGGER.info("Applying decision strategies...")
    strategy_entries = _retrieve_strategy_list()
    for strategy_entry in strategy_entries:

        logger.LOGGER.info("Trying decision strategy: %s" % strategy_entry.name)
        if not strategy_hash.STRATEGY_HASH.has_key(strategy_entry.name):
            logger.LOGGER.error("No such strategy exists.")
            continue

        strategy_class = strategy_hash.STRATEGY_HASH[strategy_entry.name]
        strategy = strategy_class(decision, member, bill)
        result = strategy.run()
        if result:
            strategy.explain()
            stance_analyze.group_stances(decision.reason)
            stance_analyze.group_stances(decision.downside)
            return True

    logger.LOGGER.info("Failed to produce a decision.")
    return False
