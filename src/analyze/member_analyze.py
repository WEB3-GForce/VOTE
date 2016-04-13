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
from src.analyze import stance_analyze
from src.database.pymongodb import PymongoDB
from src.database import queries
from src.constants import database as db_constants
from src.constants import logger
from src.constants import outcomes

def extract_voting_stances(member):
    """Extracts stances the member holds based on voting history.

    After the method executes, all stances for the member have been extracted.
    The results are NOT saved to the database. The caller must do so.
    
    WARNING: This erases any stances already contained by the member.

    Arguments:
        member: the member to extract stances for
    """

    logger.LOGGER.info("Extracting stances based on voting record of %s..."
        % member.full_name)
    logger.LOGGER.info("Erasing old stances...")

    member.stances = []
    for vote in member.voting_record:
        member.stances += _extract_single_voting_stance(vote)

    logger.LOGGER.info("Extracting voting stances completed.")

def _extract_single_voting_stance(vote):
    """Helper to extract_voting_stances. Extracts a stance the member holds
    based on voting for a particular bill. It checks the bill and returns
    the stances that can be inferred from voting for or against it.
       
    Arguments:
        vote: a vote from member.voting_record
        
    Return
        A list containing all stances to be inferred from the vote.
    """
    logger.LOGGER.info("Extracting stances from vote: %s" % vote)

    # Check if the name used in vote is the name of the bill, bill number, or
    # a synonym
    bill_identifier = vote.data
    query = queries.bill_query(bill_identifier)
    bill = PymongoDB.get_db().find_one(db_constants.BILLS, query)
    if bill is None:
        logger.LOGGER.error("Bill not found: %s" % bill_identifier)
        return []

    if vote.outcome == outcomes.FOR:
        return bill.stances_for
    elif vote.outcome == outcomes.AGN:
        return bill.stances_agn
    else:
        msg = "Bad Bill outcome. Expected FOR or AGN. Received %s" % vote.outcome
        logger.LOGGER.error(msg)
        return []

def infer_relations_stances(member):
    """This function looks through the member's relations and extracts stances
    the member might hold by association. The member opposes what his enemies
    like and supports what his friends support.
       
    Upon completion of this method, member.pro_rel_stances contains all the
    stances the member's friends support while member.con_rel_stances contains
    all the stances the member's enemies support.
       
    Arguments:
        member: the member to examine
    """
    logger.LOGGER.info("Inferring stances from relations of %s..."
        % member.full_name)

    results = []
    for relation in member.relations:
        results += _infer_single_relation_stances(relation)

    pro_stance = lambda stance : outcomes.PRO == stance.relation.side
    con_stance = lambda stance : outcomes.CON == stance.relation.side
    member.pro_rel_stances = filter(pro_stance, results)
    member.con_rel_stances = filter(con_stance, results)

    logger.LOGGER.info("Inferring relation stances completed.")

def _infer_single_relation_stances(relation):
    """A helper method for extract_relations_stances(). It queries the database
    for an individual group a member has relations with and extracts stances
    from it.
    
    Arguments:
        relation: the relationship to examine (identifies a group)
    
    Returns:
        A list of all stances extracted from the relation
    """
    results = []
    # Check if the relation group is identified by name or id or synonym.
    query = queries.group_query(relation.group)
    group = PymongoDB.get_db().find_one(db_constants.GROUPS, query)

    if group is None:
        logger.LOGGER.error("Group not found: %s" % relation.group)
        return results

    logger.LOGGER.info("Inferring stances from group: %s" % group.name)
    for stance in group.stances:
        stance.relation = relation
        results.append(stance)

    return results


def match_stances(member, bill, side):
    """This function filters the member's stances by the stances that are
    implied by voting for a given side of a bill. In other words, it determines
    which stances a member has that might suggest that the member would vote
    for the given side of the bill.

    Arguments:
        member: the member whose stances will be filtered
        bill: the bill whose stances will be used to filter the member stances
        side: the side of the bill to examine (e.g. FOR or AGN)

    Return:
        A list that contains only those member stances that are the same as
        those implied by voting on the given side of the bill.
    """
    logger.LOGGER.info("Considering implications of voting %s bill %s..." %
        (side, bill.bill_number))
    logger.LOGGER.info("Matching member stances with bill stances...")

    stances = []
    if side == outcomes.FOR:
        stances = _match_stances_helper(member, bill.stances_for)
    elif side == outcomes.AGN:
        stances = _match_stances_helper(member, bill.stances_agn)
    else:
        logger.LOGGER.error("Invalid side to match: %s" % side)

    stance_analyze.sort_stances(stances, member)
    logger.LOGGER.info("Considering %s implications completed." % side)
    return stances

def _match_stances_helper(member, stances):
    """Filters the member's stances keeping only those that match a stance in
    stances. The member's stances consist of personal stances (member.credo),
    voting record stances (member.stances), and group stances
    (member.pro_rel_stances)

    Arguments:
        member: the member whose stances will be filtered.
        stances: the list of stances to filter the member stances by
        
    Returns:
        The list of filtered stances.
    """
    member_stances = member.credo + member.stances + member.pro_rel_stances

    filter_fun = lambda member_stance : (
        any(stance.match(member_stance) for stance in stances))
    return filter(filter_fun, member_stances)
