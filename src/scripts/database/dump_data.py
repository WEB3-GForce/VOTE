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
import os
from bson import json_util
from src.config import config
from src.constants import config as config_constants
from src.constants import database as db_constants
from src.database.pymongodb import PymongoDB


def dump_data():
    """Dumps the current data from the database into json files."""

    config_db = config.CONFIG[config_constants.DATABASE]
    DATABASE_PATH = "%s/../../../database/%s" % (os.path.dirname(__file__),
        config_db)

    DB = PymongoDB.get_db()

    print "Dumping %s database data" % config_db
    print "Target Directory: %s" % DATABASE_PATH
    print "Running..."

    for collection_name in db_constants.DB_COLLECTIONS:
        file_name = "%s/%s.txt" % (DATABASE_PATH, collection_name)
        with open(file_name, 'w') as dump_file:
            for data in DB.DB[collection_name].find({}):
                dump_result = json_util.dumps(data, indent=4, sort_keys=True)
                dump_file.write(dump_result + '\n')
        print collection_name + " dumped."

    print "Finished."

if __name__ == "__main__":
    dump_data()
