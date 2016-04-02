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

from src.constants import database as db_constants
from src.constants import logger
from src.database import queries
from src.database.pymongodb import PymongoDB
from src.util import util

def normative_stance(stance):
    """Checks if a given stance is the normative stance on the issue (i.e. the
    way most people in the country feel about the issue).
    
    Argument:
        stance: the stance to check
        
    Returns:
        True if the stance is normative, False otherwise.
    """
    stance_issue = PymongoDB.get_db().find_one(db_constants.ISSUES,
        queries.issue_query(stance.issue))
    if not stance_issue:
        logger.LOGGER.error("Issue not found: " + str(stance.issue))
    if stance_issue and stance_issue.norm:
        return stance.match(stance_issue.norm)
    return False


def collect_normative_stances(stances):
    """Filters a given list of stances to contain only those that are normative.
    
    Arguments:
        stances: the list of stances to filter.
        
    Returns:
        The filtered list with duplicates removed.
    """
    filter_fun = lambda stance: normative_stance(stance)
    norms = filter(filter_fun, stances)
    return util.remove_duplicates(norms) if norms else []
