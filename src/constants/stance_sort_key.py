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

# The following are stance sort keys that can be used.

# For equity, the importance of the stance itself is the primary sort key and
# the importance of the source relation of the stance is the secondary key.
EQUITY = "EQUITY"

# For loyalty, the importance of the source relation of the stance is the
# primary sort key. The importance of the stance itself is a secondary sort key.
LOYALTY = "LOYALTY"

# This is a list of all the acceptable stance sort keys
SORT_KEY_LIST = [EQUITY, LOYALTY]