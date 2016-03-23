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

from src.database import vote_transform

class VoteCursor(object):
    """ A simple wrapper class over the Pymongo Cursor from a Pymongo Collection
    find() call. It translates data from the cursor before returning it to
    the user.
    """

    def __init__(self, cursor):
        self._cursor = cursor
        self._transformer = vote_transform.VoteTransform()

    def __iter__(self):
        return self

    def __next__(self):
        document = self._cursor.next()
        return self._transformer.transform_outgoing(document)

    def next(self):
        return self.__next__()
