import copy

"""  
    This routine will analyze a bill-remarks phrase and produce the likely issue outcomes pro/con for the bill.

    word-list is a sequence of words.  returns list of issues that match.
"""

def match_with_issues(word_list)
    if word_list is None:
        return
    
    result = []

    for word in word_list:
        match = match_one_word_with_issues(word)
        
        if match:
            result.append(match)            

# Initialize table of stop words -- not to be indexed
stop_words = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'jr', 'sr', 'dr', 'phd', 'mr', 'mrs', 'ms', 'col', 'maj', 'a.', 'b.', 'c.', 'd.', 'e.', 'f.', 'g.', 'h.', 'i.', 'j.', 'k.', 'l.', 'm.', 'n.', 'o.', 'p.', 'q.', 'r.', 's.', 't.', 'u.', 'v.', 'w.', 'x.', 'y.', 'z.', 'jr.', 'sr.', 'dr.', 'ph.d.', 'mr.', 'mrs.', 'ms.', 'col.', 'maj.', 'the', 'of', 'and', 'to', 'on', 'no', 'for', 'with', 'committee', 'government', 'american', 'if', 'one', 'an', 'at', 'support', 'proposal', 'program', 'in', 'as', 'ban', 'case', 'use', 'act', 'department', 'amendment', 'us']   

bill_stop_table = dict((word,True) for word in stop_words)

opposition_words = ['prohibiting', 'prohibition', 'striking', 'limit', 'opposition', 'oppose', 'bar', 'against']

opposition_table = dict((word,True) for word in opposition_words)

def match_one_word_with_issues(word)
    if bill_stop_table.has_key(word.lower()) or word.isdigit():
        return None
    return DBIssue.getByName(word.upper())

def most_frequent(word_list):
    return max(set(word_list), key=word_list.count)
    
def process_punctuation(str):
    punctuation = [".", ",", "?", "$", "(", ")", "\'", "\"", "`"]
    processed = [" *period* ", " *comma* ", " *question* ",
       " *dollar* ", " *lparen* ", " *rparen *", " * quote * ",
       " * quote * ", " * quote * "]
    
    for punctuation, result in zip(punctuation, processed):
        str.replace(punctuation, result)

def split_words(string):
    processed_string = process_punctuation(string)
    return processed_string.split(" ")

def extract_bill_issues(word_list):
    result = double_match_with_issues(word_list)
    
    if result is None or result == []:
        resuls = match_with_issues(word_list)

    return most_frequent(result)

def infer_bill_stances(billid, ):
    bill = DBBill.getById(billid)
    word_list = split_words(bill.remarks)
    issues = extract_bill_issues(word_list)
    opp = opposing_issue?(word_list)
    
    stance_for = []
    stance_agn = []
    for issue in issues:
        stance_for.append(get_norms_or_new_stances(issue, opp))
        stance_agn.append(for_to_agn_stance(stance_for[-1]))

    bill.inferred_stance_for = stance_for
    bill.inferred_stance_agn = stance_agn
    return {"FOR": stance_for, "AGN": stance_agn}

# Maybe store in DB?
def get_norms_or_new_stances(issueid, oppose_flag):
    issue = DBIssue.getById(issueid)
    norm = issue.norm
    
    stance = DBStance.getById(norm)
    if stance is None:
        # Check how to create new stances in db. Check
        # later if means source is bill.
        stance = Stance(issue=issue.synonyms[0], side="PRO",
            importance="B", source="bill")
    
    if oppose_flag:
        stance = for_to_agn_stance(stance)
    return stance

def opposing_issue?(word_list)
    if word_list is None:
        return False
    
    for word in word_list:
        if word.isdigit():
            continue
        if opposition_table.has_key(word):
            return True
    return False

# Maybe store in DB?
def for_to_agn_stance(stance):
    new_stance = copy.deep(stance)
    opposite_issue = DBIssue.getById(stance.issue).opposite

    if opposite_issue is not None:
        new_stance.issue = opposite_issue

    else:
        new_stance.side = "CON" if new_stance.side == "PRO" else "PRO"
    
    return new_stance

def double_match_with_issues(word_list):
    if word_list is None:
        return
    
    word = match_one_word_with_issues(word_list[0])
    double_match_words(word, word_list[1:])

def double_match_words(word, word_list):

    if word_list is None:
        return
    
    # Note: Variable name is word but seems to actually be an
    # issue object
    results = []
    for each_word in word_list:
        next_word = match_one_word_with_issues(each_word)
        for next in next_word:
            match = []
            if next in word:
                match.append(next)
    
        if match:
            results += match

        word = next_word

    return results

