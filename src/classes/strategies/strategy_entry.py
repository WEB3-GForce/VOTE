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

from src.classes.printable_object import PrintableObject

class StrategyEntry(PrintableObject):
    """"This class represents the control data for a particular strategy and is
    stored in the database. In short, it identifies a particular strategy that
    vote should try to run. It specifies whether vote should run the strategy
    and (if so) whether it should run this strategy before or after other
    strategies.
    
    It is important to note that the database for strategies does not contain
    the Strategy class. Rather, it contains this class: StrategyEntry
    
    Attributes:
        name: The name of the strategy
        rank: The rank of the strategy, determines the order in which the
            strategy will be run. The lower the number, the higher the rank. In
            other words, 0 is the highest rank and will be run first. The
            default is set to a relatively low rank (1000)
        active: Whether the strategy should be run. By default, strategies
            are not active.
    """

    def __init__(self, entries=None):
        """Constructs a new StrategyEntry based upon a dictionary of attributes.
        
        Initializes the instance variables to default values and then updates
        them with the entries provided in the hash.
        
        Arguments:
            entries: The hash of the attribute values of the form
                {"name" : "some_name", "rank" : 0,
                ...}
        """
        self.name = ""
        self.rank = 1000
        self.active = False

        if entries is not None:
            self.__dict__.update(entries)
