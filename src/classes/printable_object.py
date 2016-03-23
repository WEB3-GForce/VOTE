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

class PrintableObject(object):
    """The parent class for all objects in VOTE.
    
    This class defines generic methods such as __str__ that will be used by all
    classes.
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
        for variable in self.__dict__.keys():
            result += "\t{0}: {1}\n".format(variable, self.__dict__[variable])
        return result
