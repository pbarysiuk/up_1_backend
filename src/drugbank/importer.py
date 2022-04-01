import os
from src.shared import database

import json


def get_drug(data):
    output = dict()
    props = ["drugbank_id", "name", "drug_interactions", "targets", "food_interactions", "calculated_properties",
             "experimental_properties", "clinical_description", 'carriers', 'enzymes']
    for prop in props:
        output[prop] = data[prop]
    return output


def execute():
    db = database.get_connection()
    dirname = os.path.dirname(__file__)
    drugbank_dir = os.path.join(dirname, '../../drugbank_docs')
    db.drugs.drop()
    for filename in os.listdir(drugbank_dir):
        file_path = os.path.join(drugbank_dir, filename)
        file = open(file_path)
        data = json.load(file)
        db.drugs.insert_one(get_drug(data))
        file.close()
    return "Import Done"
