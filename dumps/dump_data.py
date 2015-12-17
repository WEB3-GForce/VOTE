from pymongo import MongoClient
from bson.json_util import dumps
from pol.database import *

for COLLECTION in collection_list:
    with open(COLLECTION.name + '.txt', 'w') as f:
        for data in COLLECTION.find({}):
            f.write(dumps(data) + '\n')
