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

from src.classes.bill import Bill
from src.classes.decision import Decision
from src.classes.group import Group
from src.classes.issue import Issue
from src.classes.member import Member
from src.classes.relation import Relation
from src.classes.stance import Stance
from src.classes.strategies.strategy_entry import StrategyEntry
from src.classes.data.importance import _Importance
from src.classes.data.result_data import ResultData

# The following are the names of databases that can be used.

# PROD is the production database and should be used only when VOTE is running
# live.
PROD = "prod"

# This database is used for integration tests. This data should mirror the
# structure of production data.
STAGING = "staging"

# The test database should be used only for unit-tests and other smaller tests.
TEST = "test"

# The development database can be used for experimenting with vote in the
# command line.
DEV = "dev"

# This is a list of all the database types used for error checking.
DB_TYPES = [PROD, STAGING, TEST, DEV]

# This is a list of the custom classes the DB supports.
DB_CUSTOM_CLASSES = [Bill, Group, Issue, Member, Relation, Stance, Decision,
                     StrategyEntry, _Importance, ResultData]

# DB entries are returned as {"_id" : ..., "_type": ..., ...}
# where "_id" is the id of the entry in the DB, "_type" is the custom class
# type, and the last ... represents more data.
ENTRY_TYPE = "_type"
ENTRY_ID = "_id"

# The following are the names of the different databases collections.
MEMBERS = "members"
GROUPS = "groups"
BILLS = "bills"
ISSUES = "issues"
STRATEGIES = "strategies"
DECISIONS = "decisions"

DB_COLLECTIONS = [MEMBERS, GROUPS, BILLS, ISSUES, STRATEGIES, DECISIONS]