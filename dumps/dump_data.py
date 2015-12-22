from pymongo import MongoClient
from bson.json_util import dumps
from pol.database import *

for COLLECTION in collection_list:
    with open('test_folder/' + COLLECTION.name + '.txt', 'w') as f:
        for data in COLLECTION.find({}):
            for key in ["stances", "stance_for", "stance_agn", "relations", "norm"]:
                if key in data and isinstance(data[key], list):
                    data[key] = [inst.__dict__ for inst in data[key]]
                elif key in data and data[key]:
                    data[key] = data[key].__dict__
            f.write(dumps(data) + '\n')
