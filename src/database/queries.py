

def bill_query(bill_identifier):
    return {"$or": [{"name": bill_identifier},
                    {"synonyms": { "$in" : [ bill_identifier ] }},
                    {"bill_number" : bill_identifier},
                    {"_id" : bill_identifier}] }

def group_query(group_identifier):
    return  {"$or": [{"name": group_identifier},
                     {"synonyms": { "$in" : [ group_identifier ]}},
                     {"_id" : group_identifier}] }