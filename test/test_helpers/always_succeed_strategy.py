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

from src.classes.stance import Stance
from src.classes.strategies.strategy import Strategy
from src.constants import outcomes

class AlwaysSucceedStrategy(Strategy):
    """"A Strategy used in tests cases. It always produces a decision.
    """

    def run(self):
        stance = Stance()
        stance.issue = "Some Stance"
        stance.side = outcomes.FOR

        stance2 = Stance()
        stance2.issue = "Some Stance"
        stance2.side = outcomes.AGN

        stance3 = Stance()
        stance3.issue = "Another Stance"
        stance3.side = outcomes.FOR

        self._decision.strategy = "AlwaysSucceedStrategy"
        self._decision.reason = [stance, stance3, stance2]
        self._decision.downside = [stance2, stance, stance3, stance2]
        return True

    def explain(self):
        pass
