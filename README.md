# VOTE
Translation of Professor Slade's VOTE system from Lisp to Python

## Requirements

- Python 2.7
- [pymongo](http://api.mongodb.org/python/current/installation.html) >= 3.2
- [MongoDB](https://docs.mongodb.org/v3.0/installation/) 3.0.7 (for Mac, just run '[brew](http://brew.sh) install mongodb' in Terminal)

## Running the code

1. Open the Python 2 interpreter from the top level directory
2. Run "from src.scripts.database import load_data"
3. Run "load_data.load_data()"
4. Run "from src.vote import vote"
5. Run "vote.vote_all()" to see the outcome of all of the members voting on all bills
6. Run "vote.vote('JORDAN', 'HR-4264')" to see what a specific member would vote on a specific bill.

### List of [sample members](https://github.com/WEB3-GForce/VOTE/blob/master/database/dev/members.txt):
- John Smith ("SMITH")
- Jane Jordan ("JORDAN")
- John Doe ("DOE")

### List of [sample bills](https://github.com/WEB3-GForce/VOTE/blob/master/database/dev/bills.txt):
- AMD
- HR-4800
- HR-4264
- HR-777

### Screenshots (examples)
![screenshot 1](https://raw.githubusercontent.com/WEB3-GForce/VOTE/master/screenshot1.png)


![screenshot 2](https://raw.githubusercontent.com/WEB3-GForce/VOTE/master/screenshot2.png)


