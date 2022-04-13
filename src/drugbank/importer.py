import json
import os

from src.shared import database


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


def targets():
    db = database.get_connection()
    dirname = os.path.dirname(__file__)
    drugbank_dir = os.path.join(dirname, '../../drugbank_docs')
    db.targets.drop()
    for filename in os.listdir(drugbank_dir):
        file_path = os.path.join(drugbank_dir, filename)
        file = open(file_path)
        data = json.load(file)
        if "targets" not in data:
            continue
        for tg in data["targets"]:
            if "polypeptides" not in tg or not len(tg["polypeptides"]):
                continue

            amino_acid_sequence = "-"
            gene_sequence = "-"
            if "amino_acid_sequence" in tg["polypeptides"][0] \
                    and tg["polypeptides"][0]["amino_acid_sequence"] is not None:
                amino_acid_sequence = tg["polypeptides"][0]["amino_acid_sequence"].split("\n", 1)[1].replace("\n", "")

            if "gene_sequence" in tg["polypeptides"][0] \
                    and tg["polypeptides"][0]["gene_sequence"] is not None:
                gene_sequence = tg["polypeptides"][0]["gene_sequence"].split("\n", 1)[1].replace("\n", "")

            target = {
                "name": tg["name"],
                "amino_acid_sequence": amino_acid_sequence,
                "gene_sequence": gene_sequence
            }
            db.targets.insert_one(target)
        file.close()
    db.targets.create_index("name", unique=True, dropDups=True)
    return "Import Done"
