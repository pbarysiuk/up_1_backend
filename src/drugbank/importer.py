import json
import os
# import gc

from src.shared import database

dirname = os.path.dirname(__file__)
drugbank_dir = os.path.join(dirname, '../../drugbank_docs')


def get_drug(data):
    output = dict()
    props = ["drugbank_id", "name", "drug_interactions", "targets", "food_interactions", "calculated_properties",
             "experimental_properties", "clinical_description", 'carriers', 'enzymes', 'synonyms']
    for prop in props:
        output[prop] = data[prop]
    return output


def execute():
    db = database.get_connection()
    db.drugs.drop()
    for filename in os.listdir(drugbank_dir):
        try:
            file_path = os.path.join(drugbank_dir, filename)
            import_drug(db.drugs, file_path)
        except:
            print(filename)
    return "Import Done"


def import_drug(collection, file_path: str):
    file = open(file_path)
    data = json.load(file)
    collection.insert_one(get_drug(data))
    file.close()
    # gc.collect()


def targets():
    db = database.get_connection()
    db.targets.drop()
    db.targets.create_index("name", unique=True)

    for filename in os.listdir(drugbank_dir):
        file_path = os.path.join(drugbank_dir, filename)
        try:
            parse_drug_target(db.targets, file_path)
        except:
            print("Import target failed: {}".format(filename))
    return "Import Done"


def parse_drug_target(collection, file_path):
    file = open(file_path)
    data = json.load(file)
    if "targets" not in data:
        return
    for tg in data["targets"]:
        import_target(collection, tg)
    file.close()
    # gc.collect()


def import_target(collection, tg):
    if "polypeptides" not in tg or not len(tg["polypeptides"]):
        return

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
    key = {'name': tg["name"]}
    collection.update_one(key, {"$set": target}, upsert=True)
    # gc.collect()
    # db.targets.insert_one(target)
