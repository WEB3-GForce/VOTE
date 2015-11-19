class PrintableObject(object):
    """
    This is the parent object for all objects in VOTE. This defines a generic
    __str__ method for nice printing of objects.
    """

    def __repr__(self):
        """Creates a representation of the object for an interactive prompt."""
        return self.__str__()

    def __str__(self):
        """
            Creates a string of the object consisting of the class name,
            instance variable names, and instance variable parameters.
        """
        result = "{0}:\n".format(self.__class__.__name__)
               
        instance_variables = self.__dict__.keys()
        instance_variables.sort()
        
        for variable in instance_variables:
            result += "\t{0}: {1}\n".format(variable, self.__dict__[variable])
        return result
