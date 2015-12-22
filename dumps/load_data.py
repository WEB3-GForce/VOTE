from pymongo import MongoClient
from bson.json_util import loads
import pol.database as db

for COLLECTION in db.collection_list:
    result = []
    for data in open('mongo_dumps/' + COLLECTION.name + ".txt").read().splitlines():
        result.append(loads(data))

    for hash_data in result:
        if not COLLECTION.find_one({"_id": hash_data["_id"]}):
            COLLECTION.insert(hash_data)
        else:
            COLLECTION.update({"_id": hash_data["_id"]}, hash_data)
