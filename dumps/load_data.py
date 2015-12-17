from pymongo import MongoClient
from bson.json_util import loads
import pol.database as db

# import members
members = []
for mdata in open("member.txt").read().splitlines():
    members.append(loads(mdata))

for member_data in members:
    if not db.MEMBER.find({"_id": member_data["_id"]}):
        db.MEMBER.insert(member_data)
    else:
        db.MEMBER.update({"_id": member_data["_id"]}, member_data)

# import groups
groups = []
for gdata in open("group.txt").read().splitlines():
    groups.append(loads(gdata))

for group_data in groups:
    if not db.GROUP.find({"_id": group_data["_id"]}):
        db.GROUP.insert(group_data)
    else:
        db.GROUP.update({"_id": group_data["_id"]}, group_data)
