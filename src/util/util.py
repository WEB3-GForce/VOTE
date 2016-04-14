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

#-----------------------------------------------------------------------------#
#                             Generic List Methods                            #
#-----------------------------------------------------------------------------#

def intersection(list1, list2, equal_fun):
    """Returns the intersection of two lists
    
    Arguments:
        list1: The first list of the intersection
        list2: The second list of the intersection
        equal_fun: The function for testing equality between two elements in the
            lists
    
    Returns:
        The intersection of the lists
    """
    filter_fun = lambda item : any(equal_fun(item, element) for element in list2)
    return filter(filter_fun, list1)
    return [element for element in list1 if element in list2]


def difference(list1, list2, equal_fun):
    """Returns the difference of two lists
    
    Arguments:
        list1: The first list of the difference
        list2: The second list of the difference
        equal_fun: The function for testing equality between two elements in the
            lists
    
    Returns:
        The difference of list1 from list2
    """
    filter_fun = lambda item : not any(equal_fun(item, element) for element in list2)
    return filter(filter_fun, list1)
    return [element for element in list1 if element in list2]

def remove_duplicates(the_list):
    """Removes duplicates from a list. This is done by turning the list to a
    set and then back to a list.
    
    Arguments:
        the_list: the input list
        
    Returns:
        the original list with duplicate values removed.
    """
    return list(set(the_list))

def flatten(a_list):
    """Takes a list of lists and flattens it into a single list.
    
    Arguments:
        a_list: The list to flatten
    
    Returns:
        The flattened list
    """
    return [item for sublist in a_list for item in sublist]

#-----------------------------------------------------------------------------#
#                             Stance List Methods                             #
#-----------------------------------------------------------------------------#

def remove_less_important_stances(stances):
    """Removes all stances that are not as important as the first stance in the
    list. The stances list is first sorted so that the first stance is the most
    important.

    Arguments:
        stances: the stance list to purge
                    
    Returns:
        The new stance list that contains only stances that are greater than or
        equal to the importance of the first stance in the original list.              
    """
    sort_key_fun = lambda stance: stance.sort_key
    sorted_stances = sorted(stances, key=sort_key_fun, reverse=True)
    filter_fun = lambda stance : stance.sort_key >= sorted_stances[0].sort_key
    return filter(filter_fun, sorted_stances)


def collect_source_db_type(db, stances):
    """Filters a list of stances based on the database they are derived from.
    
    Arguments:
        db: the source database to match
        stances: the list of stances to filter.
        
    Returns:
        The filtered list.
    """
    filter_fun = lambda stance : stance.source_db == db
    return filter(filter_fun, stances)

# Extensions to collect_source_type. Simple lambdas that collect from a
# particular DB like groups
collect_group_stances = lambda stances: collect_source_db_type(db_constants.GROUPS, stances)
collect_credo_stances = lambda stances: collect_source_db_type(db_constants.MEMBERS, stances)
collect_bill_stances = lambda stances: collect_source_db_type(db_constants.BILLS, stances)
