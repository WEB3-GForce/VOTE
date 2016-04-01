"""
    VOTE - A decision program for predicting votes in Congress.
    Copyright (C) 2016 William Edward Bailey, III (WEB3 or WEBIII):
      https://github.com/WEB3-GForce
    Based on Stephen Slade's Ph.D Thesis:
      zoo.cs.yale.edu/classes/cs458/materials/RealisticRationality.pdf

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

def bill_query(bill_identifier):
    return {"$or": [{"name": bill_identifier},
                    {"synonyms": { "$in" : [ bill_identifier ] }},
                    {"bill_number" : bill_identifier},
                    {"_id" : bill_identifier}] }

def group_query(group_identifier):
    return  {"$or": [{"name": group_identifier},
                     {"synonyms": { "$in" : [ group_identifier ]}},
                     {"_id" : group_identifier}] }

def issue_query(issue_identifier):
    return  {"$or": [{"name": issue_identifier},
                     {"synonyms": { "$in" : [ issue_identifier ] }},
                     {"_id" : issue_identifier}
                    ]
            }