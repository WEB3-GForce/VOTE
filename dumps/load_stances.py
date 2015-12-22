import json
import pol.database as db
from pol.stance import Stance
from pol.group import Group


def load_member_stances():
    bill_stances = json.load(open("lisp_dumps/bill_stances.json"))["stances"]

    for stance in bill_stances:
        bill_syn = stance["name"].upper()
        for_stances = []
        for for_stance in stance["for"]:
            for_stances.append(Stance(**for_stance))
        agn_stances = []
        for agn_stance in stance["agn"]:
            agn_stances.append(Stance(**agn_stance))
        for_encoded = map(db.encode_classes, for_stances)
        agn_encoded = map(db.encode_classes, agn_stances)
        # finds bill by synonym name and sets stances for and agn
        db.BILL.update_one({"synonyms": bill_syn}, {"$set": {"stance_for": for_encoded, "stance_agn": agn_encoded}})


def load_groups():
    groups = json.load(open("lisp_dumps/group.json"))["groups"]
    for hash_data in groups:
        try:
            group = Group(**hash_data)
        except TypeError:
            print hash_data
            return
        if not db.GROUP.find_one(hash_data):
            db.GROUP.insert(group.__dict__)
        else:
            db.GROUP.update(hash_data, group.__dict__)


def load_group_stances():
    group_stances = json.load(open("lisp_dumps/group_stances.json"))
    for group_syn in group_stances:
        stances = []
        for hash_data in group_stances[group_syn]:
            stances.append(Stance(**hash_data))
        stances_encoded = map(db.encode_classes, stances)
        query = {"$or": [{"name": group_syn},
            {"synonyms": group_syn}
        ]}
        db.GROUP.update_one(query, {"$set": {"stances": stances_encoded}})

# load_groups()
load_group_stances()
