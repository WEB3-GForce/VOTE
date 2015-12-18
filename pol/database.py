from pymongo import MongoClient
from member import Member
from group import Group
from bill import Bill
from issue import Issue
from relation import Relation
from stance import Stance
from strategy import Strategy
from decision import Decision


# MongoClient and database
CLIENT = MongoClient()
DB = CLIENT.vote

# Collections for all the objects
MEMBER   = DB.member
GROUP    = DB.group
BILL     = DB.bill
ISSUE    = DB.issue
RELATION = DB.relation
STANCE   = DB.stance
STRATEGY = DB.strategy
DECISION = DB.decision

# List of all the collections
collection_list = [MEMBER, GROUP, BILL, ISSUE, RELATION, STANCE, STRATEGY, DECISION]

# Maps the names of the collections to their corresponding object
# class
collection_to_class_map = {"member" : Member, "group" : Group, "bill": Bill, "issue" : Issue, "relation": Relation, "stance": Stance, "strategy": Strategy, "decision" : Decision}

# Performs a query on the collection and then converts it into
# an object of the corresponding class.
def get(collection, query):
    data_hash = collection.find_one(query)
    collection_class = collection_to_class_map[collection.name]
    
    if data_hash:
        return collection_class(**data_hash)
    return None
