from pymongo import MongoClient

# MongoClient and database
CLIENT = MongoClient()
DB = CLIENT.vote

# Collections for all the objects
MEMBER = DB.member
GROUP  = DB.group
BILL   = DB.bill
ISSUE  = DB.issue
RELATION = DB.relation
