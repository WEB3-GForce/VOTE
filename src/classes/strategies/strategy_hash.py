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

from src.classes.strategies.balance_the_books_strategy import BalanceTheBooksStrategy
from src.classes.strategies.best_for_the_country_strategy import BestForTheCountryStrategy
from src.classes.strategies.could_not_pass_strategy import CouldNotPassStrategy
from src.classes.strategies.change_of_heart_strategy import ChangeOfHeartStrategy
from src.classes.strategies.inconsistent_constituency_strategy import InconsistentConstituencyStrategy
from src.classes.strategies.inoculation_strategy import InoculationStrategy
from src.classes.strategies.minimize_adverse_effects_strategy import MinimizeAdverseEffectsStrategy
from src.classes.strategies.not_good_enough_strategy import NotGoodEnoughStrategy
from src.classes.strategies.not_constitutional_strategy import NotConstitutionalStrategy
from src.classes.strategies.nonpartisan_decision_strategy import NonPartisanDecisionStrategy
from src.classes.strategies.simple_consensus_strategy import SimpleConsensusStrategy
from src.classes.strategies.simple_majority_strategy import SimpleMajorityStrategy
from src.classes.strategies.popular_decision_strategy import PopularDecisionStrategy
from src.classes.strategies.unimportant_bill_strategy import UnimportantBillStrategy


# Maps the name of a strategy to the class that represents the strategy
STRATEGY_HASH = {"Popular Decision" : PopularDecisionStrategy,
                 "Inconsistent Constituency" : InconsistentConstituencyStrategy,
                 "Non-partisan Decision" : NonPartisanDecisionStrategy,
                 "Not Constitutional" : NotConstitutionalStrategy,
                 "Unimportant Bill" : UnimportantBillStrategy,
                 "Balance the Books" : BalanceTheBooksStrategy,
                 "Best for the Country" : BestForTheCountryStrategy,
                 "Change of Heart" : ChangeOfHeartStrategy,
                 "Inoculation" : InoculationStrategy,
                 "Could Not Pass" : CouldNotPassStrategy,
                 "Minimize Adverse Effects" : MinimizeAdverseEffectsStrategy,
                 "Not Good Enough" : NotGoodEnoughStrategy,
                 "Simple Consensus" : SimpleConsensusStrategy,
                 "Simple Majority" : SimpleMajorityStrategy}
