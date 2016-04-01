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


def remove_duplicates(the_list):
    return list(set(the_list))