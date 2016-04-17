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

from src.classes.strategies.inconsistent_constituency_strategy import InconsistentConstituencyStrategy
from src.classes.strategies.nonpartisan_decision_strategy import NonPartisanDecisionStrategy
from src.classes.strategies.popular_decision_strategy import PopularDecisionStrategy

# Maps the name of a strategy to the class that represents the strategy
STRATEGY_HASH = {"Popular Decision" : PopularDecisionStrategy,
                 "Inconsistent Constituency" : InconsistentConstituencyStrategy,
                 "Non-partisan Decision" : NonPartisanDecisionStrategy}