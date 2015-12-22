def isa_side(side):
    side.upper() in ["PRO", "CON"]
    
def other_side(side):
    other_hash = {"PRO" : "CON", "CON":"PRO"}
    return other_hash[side.upper]

def isa_importance(importance):
    importance.upper() in ["A", "B", "C", "D"]

# IN python "A" < "B" returns True. However, we want the
# reverse since "A" is more important than "B"
def greater_than_or_equal_importance(imp1, imp2):
    return imp1 <= imp2

def greater_than_importance(imp1, imp2):
    return imp1 < imp2

def less_than_importance(imp1, imp2):
    return imp1 > imp2

def most_important(importance):
    return importance == "A"

def opposite_result(result):
    other_result = {"FOR" : "AGN", "AGN":"FOR"}
    return other_result[result]

# Typecheck will not be handled. DB will be handled by Mongo

# The utility procedures from utils.lisp can all be easily done in # python by built in procedures.
# For simplicty, a few have been defined here.

def find_intersection(list1, list2, equal_fun):
    """Returns the intersection of list1 and list2 using equal_fun to test for
    equality"""
    filter_fun = lambda item : any(equal_fun(item, element) for element in list2)
    return filter(filter_fun, list1)

def remove_duplicates(the_list):
    return list(set(the_list))
