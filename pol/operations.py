# sourced from pol/operations.lisp
#
# Copyright 2015 krishpop <krishnan1994@gmail.com>
#
# Distributed under terms of the MIT license.

from functools import singledispatch

# to implement a generic function, use singledispatch
# see https://www.python.org/dev/peps/pep-0443/
@singledispatch
def synonyms(self):
    pass


@singledispatch
def english_short(obj):
    return None

@singledispatch
def set_isa_sort(self):
    pass


@singledispatch
def set_date_sort(self):
    pass


@singledispatch
def set_alpha_sort(self):
    pass


# from issue
@singledispatch
def get_stances(self, side):
    pass


# from stance
@singledispatch
def get_sort_key(self, keyword):
    pass


@singledispatch
def isa(self):
    return self.isa


@singledispatch
def reveal_group(self):
    pass


@singledispatch
def reveal_issue(self):
    return None


@singledispatch
def match(alpha, beta):
    return alpha == beta


# from stance
@singledispatch
def reveal_source(self):
    pass


"""
Data dependenices:

Decision may change if any of the following chage:
    issue_norm
    group_stances
    bill_importance
    bill_stance_for
    bill_stance_agn
    member_credo
    member_votes (member_stances)
    member_relations (member_pro_rel_stances member_con_rel_stances)

    Additions to the database will not directly affect prior decisions.
    Only when changes are made to items that were used in the original
    decision, e.g., issues, groups, bills, and members.

returns list of selectors that may affect a decision
"""

@singledispatch
def decision_dependencies(self):
    return None
