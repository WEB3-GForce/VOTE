from pymongo import MongoClient
from bson.json_util import loads
from pol.database import DB
from pol.database import collection_list
import sys
from pol.member import Member
from pol.group import Group
from pol.bill import Bill
from pol.issue import Issue
from pol.relation import Relation
from pol.stance import Stance
from pol.strategy import Strategy
from pol.decision import Decision

# Run this command as follows:
#
# python load_file.py DATABASE_TO_ADD_TO FILE_TO_LOAD_FROM
#
# It reads in a list of json hashes and adds them to the
# specified database.

def main():
    filter_fun = lambda x: x.name
    collection_names = map(filter_fun, collection_list)

    class_names = {"member" : Member, "group" : Group, "bill": Bill, "issue" : Issue, "relation": Relation, "stance": Stance, "strategy": Strategy, "decision" : Decision}

    dbName = sys.argv[1]
    fileName = sys.argv[2]

    if dbName not in collection_names:
        print "Database is not defined"
        return

    COLLECTION = DB[dbName]

    result = loads(open(fileName).read())

    for hash_data in result:
        an_object = class_names[dbName](**hash_data)

        if not COLLECTION.find_one(hash_data):
            COLLECTION.insert(an_object.__dict__)
        else:
            COLLECTION.update(hash_data, an_object.__dict__)

if __name__ == "__main__":
    main()
