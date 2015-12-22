from pymongo.son_manipulator import SONManipulator
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
GROUP    = DB.groups
BILL     = DB.bill
ISSUE    = DB.issue
RELATION = DB.relation #(don't need relation table)
# STANCE   = DB.stance #(don't need stance table)
STRATEGY = DB.strategy
DECISION = DB.decision

# List of all the collections
collection_list = [MEMBER, GROUP, BILL, ISSUE, RELATION, STRATEGY, DECISION]

# Maps the names of the collections to their corresponding object
# class
collection_to_class_map = {"member" : Member, "groups" : Group, "bill": Bill, "issue" : Issue, "relation": Relation, "stance": Stance, "strategy": Strategy, "decision" : Decision}

# Performs a query on the collection and then converts it into
# an object of the corresponding class.
def get(collection, query):
    data_hash = collection.find_one(query)
    collection_class = collection_to_class_map[collection.name]

    if data_hash:
        return collection_class(**data_hash)
    return None

# Prints out all the decisions in the decision DB.
def print_all(collection):
    collection_class = collection_to_class_map[collection.name]

    for data_hash in collection.find({}):
        print collection_class(**data_hash)

# This encoding is used to encode any Relation or Stance objects stored directly
# in mongo.
def encode_classes(value):
    if isinstance(value, Stance):
        return {"_type" : "Stance", "x" : value.__dict__}
    elif isinstance(value, Relation):
        return {"_type" : "Relation", "x" : value.__dict__}
    else:
        return None

# This function is used to encode Relation or Stance objects stored in a list.
def list_encoding(list_value):
    if type(list_value) == list:
        return map(list_encoding, list_value)
    custom = encode_classes(list_value)
    return custom if custom else list_value

# This decoding is used to decode any Relation or Stance objects stored directly
# in mongo.
def decode_classes(value):
    if not isinstance(value, dict):
        return None
    if "_type" in value and value["_type"] == "Stance":
        return Stance(**value["x"])
    if "_type" in value and value["_type"] == "Relation":
        return Relation(**value["x"])
    else:
        return None

# This function is used to decode Relation or Stance objects stored in a list.
def list_decoding(list_value):
    if type(list_value) == list:
        return map(list_decoding, list_value)
    custom = decode_classes(list_value)
    return custom if custom else list_value

# Transform automatically transforms Stance and Relation objects.
# http://api.mongodb.org/python/current/examples/custom_type.html
class Transform(SONManipulator):
    def transform_incoming(self, son, collection):
        for (key, value) in son.items():
            custom = encode_classes(value)
            if custom:
                son[key] = custom
            if isinstance(value, list):
                son[key] = map(list_encoding, value)
            elif isinstance(value, dict): # Make sure we recurse into sub-docs
                son[key] = self.transform_incoming(value, collection)
        return son


    def transform_outgoing(self, son, collection):
        for (key, value) in son.items():
            if isinstance(value, list):
                son[key] = map(list_decoding, value)
            if isinstance(value, dict):
                custom = decode_classes(value)
                if custom:
                    son[key] = custom
                else: # Again, make sure to recurse into sub-docs
                    son[key] = self.transform_outgoing(value, collection)
        return son

DB.add_son_manipulator(Transform())
