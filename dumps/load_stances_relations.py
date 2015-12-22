import json
import pol.database as db
from pol.stance import Stance
from pol.group import Group


def load_bill_stances():
    bill_stances = json.load(open("lisp_dumps/bill_stances.json"))["stances"]
    # bill_stances is just a list
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
    print "bill_stances loaded!"


def load_groups():
    groups = json.load(open("lisp_dumps/group.json"))["groups"]
    # groups is just a list
    for hash_data in groups:
        group = Group(**hash_data)
        if not db.GROUP.find_one(hash_data):
            db.GROUP.insert(group.__dict__)
        else:
            db.GROUP.update(hash_data, group.__dict__)
    print "groups loaded!"


def load_group_stances():
    group_stances = json.load(open("lisp_dumps/group_stances.json"))
    # group_synonym used as key
    for group_syn in group_stances:
        stances = []
        for hash_data in group_stances[group_syn]:
            stances.append(Stance(**hash_data))
        stances_encoded = map(db.encode_classes, stances)
        query = {"$or": [{"name": group_syn},
            {"synonyms": group_syn}
        ]}
        db.GROUP.update_one(query, {"$set": {"stances": stances_encoded}})
    print "group stances loaded!"


def load_relations():
    member_relations = json.load(open("lisp_dumps/member_relations.json"))
    # member_name used as key
    for member_name in member_relations:
        relations = [db.Relation(**d) for d in member_relations[member_name]]
        relations_encoded = map(db.encode_classes, relations)
        db.MEMBER.update_one({"name": member_name}, {"$set": {"relations": relations_encoded}})
    print "member relations loaded"


def issue_norm_stance():
    for issue in db.ISSUE.find({}):
        if isinstance(issue["norm"], list):
            norm_dict = dict(zip(["side", "importance", "issue", "source_db"], issue["norm"] + ["issue"]))
            norm_stance = Stance(**norm_dict)
            encoded_stance = db.encode_classes(norm_stance)
            db.ISSUE.update(issue, {"$set": {"norm": encoded_stance}})
    print "converted norm stances to stance objects"

load_bill_stances()
load_groups()
load_group_stances()
load_relations()
