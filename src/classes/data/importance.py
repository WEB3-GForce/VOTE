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

class _Importance(object):
    """Denotes how important stances, relations, etc. are.
    
    Entities in VOTE (such as groups and members) hold stances on various
    issues. These stances are of various degrees of importance. Rather than
    using a quantitative score, VOTE uses a qualitative score.
    
    There are four levels of importance: A, B, C, and D. There is also an
    additional level called Z that is lower than all others just in case an
    extra level is needed for house keeping or other initialization.
    
    This class is private and should not be used. Instead, use the objects
    defined below. However, feel free to use the comparators defined.
    
    A brief word about the comparators: A is greater in importance than B,
    C is less in importance than B, etc. The underlying value used for
    importance is a string. How strings define the comparators is different
    ("A" < "B"), so new comparison functions are defined to ensure that the
    comparison semantics for Importance holds.
    
    Attributes:
        value: The string value of the importance such as "A" or "B". Always
            uppercase.
    """

    def __init__(self, entries=None):
        self.value = "Z"

        if entries is not None:
            self.__dict__.update(entries)

    def __eq__(self, object2):
        return self.value == object2.value

    def __ne__(self, object2):
        return self.value != object2.value

    def __gt__(self, object2):
        return self.value < object2.value

    def __lt__(self, object2):
        return self.value > object2.value

    def __ge__(self, object2):
        return self.value <= object2.value

    def __le__(self, object2):
        return self.value >= object2.value

    def __str__(self):
        return self.value

    def most_important(self):
        return self == A


# The following are constants representing the different levels of importance.
# Use these in code.
A = _Importance({"value" : "A"})
B = _Importance({"value" : "B"})
C = _Importance({"value" : "C"})
D = _Importance({"value" : "D"})

Z = _Importance({"value" : "Z"})
