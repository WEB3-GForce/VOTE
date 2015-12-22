# VOTE
Translation of Professor Slade's VOTE system from Lisp to Python

Status: [ not started :black_medium_square: | completed :white_check_mark: | in progress :speech_balloon:]

| File | Status |
|------|--------|
|analyze|:white_check_mark:|
|anal2|:white_check_mark:|
|anal3|:white_check_mark:|
|cg|:white_check_mark:|
|mem_anal|:white_check_mark:|
|operations|:white_check_mark:|
|parse|:white_check_mark:|
|party_strat|:white_check_mark:|
|protocol|:white_check_mark:|
|remove|:white_check_mark:|
|shift|:white_check_mark:|
|strats|:white_check_mark:|
|utils|:white_check_mark:|

### In progress / to-do:

- database
  - adding member, stances, bills, relations, and groups :white_check_mark:
- proofing the code ~ trying to run the entire system
- make sure the following functions work:

```python
initialize_decision(decision, member, bill)

update_decision_metrics(decision)

apply_decision_strategies(decision)

compare_with_real_vote(decision)

update_decision_dbase(decision) # insert into database
```

- proof all of the existing code
- add pretty print to analyze
- files to complete
  - vote.py
  - strategies.py
     - majority
     - consensus
     - strat_simple_consensus
     - strat_popular
     - firm decision
     - decision outcome
     - strat_simple_majority
  - decision.py
- readme
- initialize_db.py
- requirements to install ~
- project summary
  - explanation of what we did ~ translation, database, making vote work
