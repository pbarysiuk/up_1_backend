import os
import csv
import sys

from src.shared.database import Database


def execute():
    maxInt = sys.maxsize
    csv.field_size_limit(maxInt)

    dirname = os.path.dirname(__file__)
    db_file = os.path.join(dirname, './UNPD_DB.csv')

    dbConnection = Database()
    db = dbConnection.db
    db.natural_products.drop()
    with open(db_file, 'rt') as f:
        reader = csv.reader(f)
        header = True
        columns = []
        for row in reader:
            if header:
                for i, col in enumerate(row):
                    columns.append(col)
                header = False
            else:
                element = {}
                for i, col in enumerate(row):
                    element[columns[i]] = col
                db.natural_products.insert_one(element)
    return "Done!"
