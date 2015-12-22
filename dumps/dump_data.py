from pymongo import MongoClient
from bson.json_util import dumps
from pol.database import *

for COLLECTION in collection_list:
    with open(COLLECTION.name + '.txt', 'w') as f:
        for data in COLLECTION.find({}):
            for key in ["stances", "stance_for", "stance_agn", "relations"]:
                if key in data and data[key]:
                    print data[key][0].__dict__
                    data[key] = [inst.__dict__ for inst in data[key]]
            try:
                f.write(dumps(data) + '\n')
            except TypeError:
                print data
                exit(0)
