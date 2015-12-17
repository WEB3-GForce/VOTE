from pymongo import MongoClient
from bson.json_util import loads
import pol.database as db

# import members
members = []
for mdata in open("member.txt").read().splitlines():
    members.append(loads(mdata))

for member_data in members:
    if not db.MEMBER.find(member_data):
        db.MEMBER.insert(members)

# import groups
groups = []
for gdata in open("group.txt").read().splitlines():
    groups.append(loads(gdata))

for group_data in groups:
    if not db.GROUP.find(group_data):
        db.GROUP.insert(groups)
