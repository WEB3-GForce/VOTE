# VOTE
Translation of Professor Slade's VOTE system from Lisp to Python

## Requirements

- Python 2.7
- [pymongo](http://api.mongodb.org/python/current/installation.html) >= 3.2
- [MongoDB](https://docs.mongodb.org/v3.0/installation/) 3.0.7 (for Mac, just run '[brew](http://brew.sh) install mongodb' in Terminal)

## Running the code

1. Open the Python 2 interpreter from the pol folder
2. Run "execfile('init_vote.py')"
3. Run "vote_all()" to see the outcome of all of the members voting on all bills
4. Run "vote('PARRIS', 'HR-4264')" to see what a specific member would vote on a specific bill.
5. Run "print_all(COLLECTION)" to view a collection in the database.
  - collection list: [MEMBER, BILLS, GROUPS, ISSUES] 

### List of completed members:
- Robert William Kastenmeier ("KASTENMEIER")
- Timothy Peter Johnson ("JOHNSON")
- Stan Parris ("PARRIS")

### List of [completed bills](https://github.com/WEB3-GForce/VOTE/blob/master/dumps/lisp_dumps/bill.txt):
- AMD
- HR-4800
- HR-4264
- S-557
- HR-3

### Screenshots (examples)
![screenshot 1](https://raw.githubusercontent.com/WEB3-GForce/VOTE/master/screenshot-1.png)
![screenshot 2](https://raw.githubusercontent.com/WEB3-GForce/VOTE/master/screenshot-2.png)

File translation from Lisp repo to Python

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
