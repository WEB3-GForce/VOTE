# sourced from pol/anal3.lisp
#
# Copyright 2015 krishpop <krishnan1994@gmail.com>
#
# Distributed under terms of the MIT license.

def tally_party(party):
    correct_for, correct_against, wrong_for, wrong_against = 0, 0, 0, 0
    for decision in DBDecisions.getall():
        if party == decision.member.party:
            if decision.score == '+':
                if decision.result == "for":
                    correct_for += 1
                elif decision.result == "agn":
                    correct_agn += 1
            elif decision.score == '-':
                if decision.result == "for":
                    wrong_for += 1
                elif decision.result == "agn":
                    wrong_agn += 1
    print_scores(correct_for, correct_against, wrong_for, wrong_against)

